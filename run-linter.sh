#!/usr/bin/env bash
set -e
docker exec -it milestones_api /app/linter.sh
