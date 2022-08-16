#!/bin/bash
echo "Did you disable debug mode before running this?"
echo "You should or you will run out of ram!"
source ../python/bin/activate
# Test mode only:
#python manage.py spot_harvest -v 2 -t -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/SPOT_Shape_Africa_2011/Africa_2011.shp'
# producion mode:
echo "2002 and before"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_1986-2002.shp'
echo "2002"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2002.shp'
echo "2003"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2003.shp'
echo "2004"
python manage.py spot_harvest -v 1 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2004.shp'
echo "2005"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2005.shp'
echo "2006"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2006.shp'
echo "2007"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2007.shp'
echo "2008"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2008.shp'
echo "2009"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2009.shp'
echo "2010"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2010.shp'
echo "2011"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2011.shp'
echo "2012"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2012.shp'
#python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2011/Africa_2011.shp'
deactivate
