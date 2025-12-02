#!/bin/bash

copyEnvs() {
  cp ../postgres/example.env ../postgres/.env

  cp ../auth/example.env ../auth/.env

  echo "INFO: for get environments to notification module please write to Illia"
  cp ../notification/example.env ../notification/.env

  cp ../docs/example.env ../docs/.env

  cp ../migration_module/example.env ../migration_module/.env

  cp ../flask_app/example.env ../flask_app/.env

  cp ../minio-local/example.env ../minio-local/.env
}
