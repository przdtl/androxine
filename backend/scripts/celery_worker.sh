#!/bin/sh

cd /app/androxine

celery -A config worker -l INFO --uid=nobody --gid=nogroup
