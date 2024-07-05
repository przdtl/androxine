#!/bin/sh

cd /app/androxine

python manage.py makemigrations
python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec "$@"