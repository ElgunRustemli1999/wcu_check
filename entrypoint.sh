#!/bin/bash

echo "Installing face_recognition_models from GitHub..."
pip install --no-cache-dir git+https://github.com/ageitgey/face_recognition_models

echo "Running Migrations..."
python manage.py migrate --noinput

echo "Collecting Static Files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn Server..."
exec gunicorn wcu_check.wsgi:application --bind 0.0.0.0:$PORT
