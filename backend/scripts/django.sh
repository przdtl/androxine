#!/bin/sh

python manage.py makemigrations
python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py createsuperuserifnotexists --no-input
