#!/usr/bin/env python3
"""
Alembic CLI with auto virtual environment activation
"""

import os
import subprocess
import sys
from pathlib import Path

def activate_venv():
    """Automatically activate virtual environment"""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print("❌ Virtual environment '.venv' not found!")
        print("Please create it with: python -m venv .venv")
        sys.exit(1)
    
    if os.name == 'nt':  # Windows
        python_executable = venv_path / "Scripts" / "python.exe"
        activate_script = venv_path / "Scripts" / "Activate.ps1"
    else:  # Linux/Mac
        python_executable = venv_path / "bin" / "python"
        activate_script = venv_path / "bin" / "activate"
    
    if not python_executable.exists():
        print(f"❌ Python executable not found at {python_executable}")
        sys.exit(1)
    
    # Add virtual environment to PATH
    if os.name == 'nt':
        venv_bin = str(venv_path / "Scripts")
    else:
        venv_bin = str(venv_path / "bin")
    
    os.environ["PATH"] = venv_bin + os.pathsep + os.environ["PATH"]
    
    print(f"✅ Virtual environment activated: {venv_path}")
    return str(python_executable)

def check_and_install_alembic():
    """Check if alembic is installed, offer to install if not"""
    try:
        subprocess.run([sys.executable, "-m", "alembic", "--version"], 
                      capture_output=True, check=True)
        print("✅ Alembic is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Alembic not found in virtual environment")
        response = input("Would you like to install Alembic now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            try:
                print("Installing Alembic...")
                subprocess.run([sys.executable, "-m", "pip", "install", "alembic"], check=True)
                print("✅ Alembic installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install Alembic")
                return False
        return False

def run_alembic_command(command):
    """Execute an alembic command and return the result"""
    try:
        cmd_parts = ["alembic"] + command.split()
        
        print(f"🚀 Executing: {' '.join(cmd_parts)}")
        print("-" * 50)
        
        # Run the command
        result = subprocess.run(
            cmd_parts,
            capture_output=False,
            text=True,
            shell=False
        )
        
        print("-" * 50)
        return result.returncode == 0
        
    except FileNotFoundError:
        print("❌ Error: Alembic command failed.")
        return False
    except Exception as e:
        print(f"❌ Error executing command: {e}")
        return False

def main():
    print("🔧 Alembic Interactive CLI")
    print("=" * 45)
    
    # Auto-activate virtual environment
    python_executable = activate_venv()
    
    # Update sys.executable to use venv Python
    sys.executable = python_executable
    
    # Check if alembic is installed
    if not check_and_install_alembic():
        print("❌ Cannot continue without Alembic.")
        sys.exit(1)
    
    print("\n✅ Ready! Type 'help' for available commands, 'exit' to quit")
    print("=" * 45)
    
    while True:
        try:
            # Get user input
            user_input = input("\nalembic> ").strip()
            
            # Handle special commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
                
            elif user_input.lower() in ['help', '?']:
                show_help()
                continue
                
            elif user_input.lower() == 'status':
                show_status()
                continue
                
            elif user_input.lower() == '':
                continue
                
            # Execute alembic command
            success = run_alembic_command(user_input)
            
            if not success:
                print(f"❌ Command failed: {user_input}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break

def show_status():
    """Show current migration status"""
    print("\n📊 Current Migration Status:")
    run_alembic_command("current")
    print("\n📜 Migration History:")
    run_alembic_command("history --indicate-current")

def show_help():
    """Show available commands and examples"""
    help_text = """
🎯 AVAILABLE COMMANDS

🔧 Migration Commands:
  upgrade head          - Upgrade to latest revision
  downgrade -1          - Downgrade by one revision
  downgrade base        - Downgrade to base (initial state)
  current               - Show current revision
  history               - Show revision history
  revision --autogenerate -m "message" - Create new migration
  stamp head            - Stamp database to head without running migrations
  show <revision>       - Show specific revision

📋 Info Commands:
  status                - Show current status and history
  help                  - Show this help message

🚪 Exit:
  exit, quit, q         - Exit the application

💡 EXAMPLES:
  upgrade head
  revision --autogenerate -m "Add users table"
  downgrade -1
  current
  status
    """
    print(help_text)

if __name__ == "__main__":
    main()