#!/bin/sh

cd /app

python manage.py makemigrations
python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec "$@"