#!/usr/bin/env bash

echo "Waiting Postgres start"
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 1
done
echo "Postgres started"

gunicorn --worker-class gevent --workers 4 --bind "0.0.0.0:8000" --log-level debug main:app