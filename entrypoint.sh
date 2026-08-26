#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Seeding personality prompts..."
python manage.py seed_personality_prompts

echo "Setting up Qdrant collection..."
python manage.py shell -c "from memory.qdrant_client import ensure_collection_exists; ensure_collection_exists()"

echo "Starting server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-10000}
