#!/bin/sh
echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn wcu_check.wsgi:application --bind 0.0.0.0:${PORT}
