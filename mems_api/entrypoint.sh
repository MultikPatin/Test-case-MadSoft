#!/usr/bin/env bash

echo "Waiting Postgres start"
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 1
done
echo "Postgres started"

echo "Waiting Redis start"
while ! nc -z "${REDIS_HOST}" "${REDIS_PORT}"; do
  sleep 1
done
echo "Redis started"

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "$API_HOST":"$API_PORT"
