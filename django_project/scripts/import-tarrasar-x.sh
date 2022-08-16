#!/bin/bash
source ../python/bin/activate
#python manage.py terrasar_harvest -v 2 -a 'POLYGON((-22.235294 44.666018,61.630435 44.666018,61.630435 -41.616591,-22.476982 -41.616591,-22.235294 44.666018))' -b 'http://localhost/TerraSAR-X_Archive_20_06_2011.zip'
python manage.py terrasar_harvest -v 2 -b 'http://localhost/TerraSAR-X_Archive_20_06_2011.zip'
deactivate

