#!/bin/sh
set -e

# Seed the database only if it does not already exist
if [ ! -f "/app/inventory.db" ]; then
    echo "Seeding database..."
    python seed.py
fi

exec "$@"
