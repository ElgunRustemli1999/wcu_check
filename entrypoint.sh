#!/bin/sh

echo "🚀 Starting app on port ${PORT}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn wcu_check.wsgi:application --bind 0.0.0.0:${PORT:-8000}