#!/usr/bin/env python3
"""Simple Python CLI to run Flyway (via Docker) for migrate / clean / undo.

Usage:
    python app.py up
    python app.py reset
    python app.py down [--force]
    
Also you can run the file and enter commands.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import shlex

cwd = Path(__file__).resolve().parent

env_path = cwd / 'example.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    # allow user to still run by relying on environment variables
    pass

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
FLYWAY_IMAGE = os.getenv('FLYWAY_IMAGE')
FLYWAY_SQL_LOCATION = os.getenv('FLYWAY_SQL_LOCATION')
DOCKER_NETWORK = os.getenv('DOCKER_NETWORK', '').strip()

MIGRATIONS_HOST_PATH = str(cwd / 'migrations')
MIGRATIONS_CONTAINER_PATH = '/flyway/sql'

JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"


def run_flyway_command(flyway_cmd_args):
    """Build and run the docker command calling the flyway image with provided flyway args list."""
    docker_cmd = [
        'docker', 'run', '--rm',
        '-v', f"{MIGRATIONS_HOST_PATH}:{MIGRATIONS_CONTAINER_PATH}",
    ]

    if DOCKER_NETWORK:
        docker_cmd += ['--network', DOCKER_NETWORK]

    # set working dir inside container so relative locations are coherent
    docker_cmd += [FLYWAY_IMAGE]

    # final CLI: flyway <command> -url=... -user=... -password=... -locations=filesystem:/flyway/sql
    flyway_cli = [
        *flyway_cmd_args,
        f"-url={JDBC_URL}",
        f"-user={DB_USER}",
        f"-password={DB_PASSWORD}",
        f"-locations={FLYWAY_SQL_LOCATION}",
    ]

    cmd = docker_cmd + flyway_cli

    print('\nRunning:')
    print(' '.join(shlex.quote(p) for p in cmd))
    print('\n--- output ---')

    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout = process.stdout.decode(errors='ignore')
    stderr = process.stderr.decode(errors='ignore')

    print(stdout)
    if stderr:
        print('--- errors ---')
        print(stderr, file=sys.stderr)

    return process.returncode, stdout, stderr


def cmd_up():
    return run_flyway_command(['migrate'])


def cmd_reset():
    code, _, _ = run_flyway_command(['clean', '-cleanDisabled=false'])
    if code != 0:
        print('Clean failed; aborting migrate.')
        return code
    return run_flyway_command(['migrate'])[0]


def cmd_down(force=False):
    # try undo first
    code, _, stderr = run_flyway_command(['undo'])
    if code == 0:
        return 0

    # if undo failed, report and only perform destructive clean if forced
    print('\nAttempted `flyway undo` but it failed.\n')
    print('Note: Flyway Undo / rollback is provided by Flyway Teams/Enterprise in many releases.\n')

    if not force:
        print('To perform a destructive fallback (clean), re-run with `--force` which will run `flyway clean`.')
        return code

    # user asked to force destructive fallback
    print('Force flag detected: running clean as destructive fallback.')
    return run_flyway_command(['clean', '-cleanDisabled=false'])[0]


def print_usage_and_exit():
    print('Usage: python app.py <up|reset|down> [--force]')
    sys.exit(2)

def main_interactive():
    while True:
        print("\nAvailable commands: migrate, reset, down, exit")
        command = input("Enter command: ").strip().split()
        if not command:
            continue
        if command[0] == "exit":
            break
        elif command[0] == "migrate":
            cmd_up()
        elif command[0] == "reset":
            cmd_reset()
        elif command[0] == "down":
            force = "--force" in command
            cmd_down(force=force)
        else:
            print("Unknown command")
            
def main():
    if len(sys.argv) < 2:
        print_usage_and_exit()

    action = sys.argv[1]
    force = '--force' in sys.argv

    if action == 'up':
        rc, _, _ = cmd_up()
        sys.exit(rc)
    elif action == 'reset':
        rc = cmd_reset()
        sys.exit(rc)
    elif action == 'down':
        rc = cmd_down(force=force)
        sys.exit(rc)
    else:
        print_usage_and_exit()


if __name__ == '__main__':
    # Якщо передано аргументи командного рядка, працюємо як раніше
    if len(sys.argv) > 1:
        main()
    else:
        # Інакше запускаємо інтерактивний режим
        main_interactive()