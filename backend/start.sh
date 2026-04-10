#!/bin/bash
# start.sh - Deployment startup script

set -e  # Exit on any error

# Use PORT from environment or default to 8000
PORT="${PORT:-8000}"
HOST="0.0.0.0"

echo "🚀 Starting server on ${HOST}:${PORT}"

# Run database migrations if needed
# python -m backend.database.init_db

exec uvicorn backend.app:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers 1 \
    --log-level info \
    --no-access-log
