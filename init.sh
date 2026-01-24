#!/bin/bash
set -e

echo "Sleeping for 5 sec, waiting for db"
sleep 5

echo "Run migrations"
alembic upgrade head

if [ "$GENERAL__ENV" = "production" ]; then
    export UVICORN_RELOAD=""
    supervisord -n
else
    sleep infinity
fi