#!/bin/bash
echo "Did you disable debug mode before running this?"
echo "You should or you will run out of ram!"
source ../python/bin/activate
# Test mode only:
#python manage.py spot_harvest -v 2 -t -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/SPOT_Shape_Africa_2011/Africa_2011.shp'
# producion mode:
#echo "2002 and before"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_1986-2002.shp'
#echo "2002"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2002.shp'
#echo "2003"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2003.shp'
#echo "2004"
#python manage.py spot_harvest -v 1 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2004.shp'
#echo "2005"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2005.shp'
#echo "2006"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2006.shp'
#echo "2007"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2007.shp'
#echo "2008"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2008.shp'
echo "2009"
python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2009.shp' -a 'POLYGON (( 11.0023505003338 -18.1897348238597,17.4940714475553 -34.6307237445404,17.4940714475553 -34.5601615603315,19.1875638685696 -35.4774699550476,25.3264738947466 -35.1246590340029,28.5017721841484 -33.0783556919439,31.959319210386 -29.7619330341242,46.1423182363809 -26.2338238236777,64.206237393867 -20.3066003501276,56.7266458677204 -4.28898453470051,40.7090300522933 -5.06516856099874,32.3826923156396 3.19060699144607,28.5017721841484 5.51915907034076,22.9979218158519 5.58972125454969,18.4113798422714 5.30747251771397,17.4940714475553 1.56767675464068,15.3772059212874 -3.15998958735763,10.9317883161248 -3.44223832419335,11.5668479740052 -7.04090971884878,12.0607832634677 -11.6274516924292,11.0023505003338 -18.1897348238597 ))'
#echo "2010"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2010.shp'
#echo "2011"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2011.shp'
#echo "2012"
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2012.shp'
#python manage.py spot_harvest -v 0 -f '/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage/Africa_2012.shp' -a 'POLYGON (( 11.0023505003338 -18.1897348238597,17.4940714475553 -34.6307237445404,17.4940714475553 -34.5601615603315,19.1875638685696 -35.4774699550476,25.3264738947466 -35.1246590340029,28.5017721841484 -33.0783556919439,31.959319210386 -29.7619330341242,46.1423182363809 -26.2338238236777,64.206237393867 -20.3066003501276,56.7266458677204 -4.28898453470051,40.7090300522933 -5.06516856099874,32.3826923156396 3.19060699144607,28.5017721841484 5.51915907034076,22.9979218158519 5.58972125454969,18.4113798422714 5.30747251771397,17.4940714475553 1.56767675464068,15.3772059212874 -3.15998958735763,10.9317883161248 -3.44223832419335,11.5668479740052 -7.04090971884878,12.0607832634677 -11.6274516924292,11.0023505003338 -18.1897348238597 ))'
#python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2011/Africa_2011.shp'
deactivate
