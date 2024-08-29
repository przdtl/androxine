#!/bin/sh

# coverage run --concurrency=multiprocessing manage.py test -v 2 --parallel auto

coverage run manage.py test -v 2 --parallel auto

RETURN=$?

coverage combine
coverage report
coverage html

exit $RETURN
