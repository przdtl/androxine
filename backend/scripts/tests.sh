#!/bin/sh

coverage run manage.py test -v 2 

RETURN=$?

coverage combine
coverage report
coverage html

exit $RETURN
