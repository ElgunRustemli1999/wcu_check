#!/bin/sh

# Railway avtomatik olaraq $PORT təyin edir, sadəcə onu istifadə edirik
echo "Starting on port: $PORT"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# GUNICORN serveri $PORT dəyişəni ilə işə salırıq
exec gunicorn wcu_check.wsgi:application --bind 0.0.0.0:${PORT:-8000}
