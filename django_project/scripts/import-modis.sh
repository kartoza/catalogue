#!/bin/bash

source ../python/bin/activate
python manage.py modis_harvest -v 2 --maxproducts=100


