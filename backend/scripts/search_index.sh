#!/bin/sh

python manage.py search_index --rebuild --use-alias --use-alias-keep-index
