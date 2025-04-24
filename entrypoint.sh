#!/bin/sh

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server on port $PORT..."
exec gunicorn wcu_check.wsgi:application --bind 0.0.0.0:$PORT
