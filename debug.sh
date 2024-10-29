#!/usr/bin/env bash

echo "Starting db container..."
docker-compose -f docker-compose.debug.yml up --build -d milestones_db

echo "Sleeping for 5 seconds..."
sleep 5


# Check if Alembic versions folder exists and has relevant files
VERSIONS_DIR="migrations/versions"
# if [ -d "$VERSIONS_DIR" ] && [ "$(find $VERSIONS_DIR -maxdepth 1 -type f)" ]; then
if [ -d "$VERSIONS_DIR" ] && [ "$(find "$VERSIONS_DIR" -maxdepth 1 -type f ! -name '.*' | wc -l)" -gt 0 ]; then
    echo "Existing Alembic migrations found. Running migrations..."
    # find "$VERSIONS_DIR" -maxdepth 1 -type f
else
    echo "No existing Alembic migrations. Creating new migration next..."
    alembic revision --autogenerate -m "Initial migration"
fi

docker-compose -f docker-compose.debug.yml up --build
