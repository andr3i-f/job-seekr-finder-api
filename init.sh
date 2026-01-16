#!/bin/bash
set -e

echo "Sleeping for 5 sec, waiting for db"
sleep 5

echo "Run migrations"
alembic upgrade head

# Run whatever CMD was passed
exec "$@"
