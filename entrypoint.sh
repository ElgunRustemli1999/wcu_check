#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn wcu_check.wsgi:application --bind 0.0.0.0:$PORT
