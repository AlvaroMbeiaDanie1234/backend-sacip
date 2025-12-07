#!/bin/bash
# Build script for Render deployment

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start the server
gunicorn sacip_backend.wsgi:application --bind 0.0.0.0:$PORT