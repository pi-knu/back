#!/bin/bash
set -e

echo "** Started init up"

cp ../postgres/example.env ../postgres/.env

docker compose -f docker-compose.prod.yml up -d

echo "** Containers started"
