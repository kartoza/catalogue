#!/bin/bash
echo "Usage: $0 or $0 <task> to run a specific migration"
echo "e.g. $0 pycsw"
echo "To do the pycsw migration"

source ../python-dev/bin/activate
cd django_project
if [ $# -ne 0 ] 
then
  python manage.py migratev3 --migrations=$1 --settings=sansa_catalogue.settings.dev_${USER}
else
  python manage.py migratev3 --settings=sansa_catalogue.settings.dev_${USER}
fi
cd ..

