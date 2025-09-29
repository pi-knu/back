#!/bin/bash
set -e

echo "** Started init up"

cp ../postgres/example.env ../postgres/.env

docker compose -f docker-compose.dev.yml up -d

echo "** Containers started"
