#!/bin/bash

echo "Collect static files"
echo yes | python manage.py collectstatic

echo "Apply database migrations"
python manage.py migrate

exec "$@"