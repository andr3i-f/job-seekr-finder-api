#!/bin/bash
set -e

echo "Sleeping for 5 sec, waiting for db"
sleep 5

echo "Run migrations"
alembic upgrade head

if [ "$ENV" = "production" ]; then
    supervisord -n
else
    sleep infinity
fi