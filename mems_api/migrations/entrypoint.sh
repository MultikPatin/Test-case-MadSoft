#!/usr/bin/env bash

echo "Waiting Postgres start"
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 1
done
echo "Postgres started"

alembic upgrade head