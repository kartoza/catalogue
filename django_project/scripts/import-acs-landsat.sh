#!/bin/bash
echo "Did you disable debug mode before running this?"
echo "You should or you will run out of ram!"
source ../python/bin/activate
python manage.py acs_landsat_harvest -v 2 -t -m 100 -e True
