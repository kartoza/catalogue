#!/bin/bash
source /opt/sac_catalogue/python/bin/activate

STARTDATE=2010-01-01
DAYCOUNT=365
LASTMONTH=0
for ((i=0; i<$DAYCOUNT; i++))
do
  YEAR=$(date -d "$STARTDATE + $i day" "+%Y")
  MONTH=$(date -d "$STARTDATE + $i day" "+%m")
  DAY=$(date -d "$STARTDATE + $i day" "+%d")
  echo "$YEAR $MONTH $DAY"
  #fetch daily records e.g. https://delivery.rapideye.de/catalogue/shapes/2010/08/01/it_shape_2010-08-01.shp
  #python manage.py rapideye_harvest -v 2 -a 'POLYGON((-22.235294 44.666018,61.630435 44.666018,61.630435 -41.616591,-22.476982 -41.616591,-22.235294 44.666018))' -y $YEAR -m $MONTH -d $DAY
  if [ $LASTMONTH -lt $MONTH ]
  then
    #fetch month records e.g. https://delivery.rapideye.de/catalogue/shapes/2010/03/it_shape_2010-03.shp
    python manage.py rapideye_harvest -v 2 -a 'POLYGON((-22.235294 44.666018,61.630435 44.666018,61.630435 -41.616591,-22.476982 -41.616591,-22.235294 44.666018))' -y $YEAR -m $MONTH
    $LASTMONTH=$MONTH
  fi
done


