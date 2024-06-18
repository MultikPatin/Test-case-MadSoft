#!/usr/bin/env bash

echo "Waiting Postgres start"
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 1
done
echo "Postgres started"

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "$API_HOST":"$API_PORT"
