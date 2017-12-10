#!/bin/bash

set -e -x

bash orgname.sh

mkdir _site public

python activity/scraper.py

python manage.py collectstatic --noinput
python manage.py distill-local public --force

mkdir public/activity
cp activity/index.html public/activity/
