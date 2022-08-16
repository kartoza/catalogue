#!/bin/bash
export PGHOST=elephant
export PGPORT=5432
export PGPASSWORD=pumpkin

DB_NAME="sac-test"
TMP_DIR="/tmp"
OUTPUT_DIR="../media/heatmaps"
HEATMAP_COLORS="heatmap.txt"
BORDERS="../resources/heatmaps/borders900913.tif"

#clean TMP_DIR
rm $TMP_DIR/heatmap*

#update heatmap_value table (use max(search_date) as starting point)
psql -c 'select update_heatmap((select max(search_date) from heatmap_values));' -d $DB_NAME 

#last week
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap(date(now()-'7 days'::interval),date(now()))" PG:dbname=$DB_NAME $TMP_DIR/heatmap_data_lastweek.tif

gdaldem color-relief $TMP_DIR/heatmap_data_lastweek.tif $HEATMAP_COLORS $TMP_DIR/heatmap-lastweek.tif

gdalwarp -r cubic -s_srs '+init=epsg:4326' -t_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs' -of Gtiff $TMP_DIR/heatmap-lastweek.tif $TMP_DIR/heatmap-lastweek-900913.tif

convert $TMP_DIR/heatmap-lastweek-900913.tif -fill white -opaque black $TMP_DIR/heatmap-lastweek-900913.png
convert $TMP_DIR/heatmap-lastweek-900913.png $BORDERS -composite $OUTPUT_DIR/heatmap-lastweek.png

#last month
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap(date(now()-'1 month'::interval),date(now()))" PG:dbname=$DB_NAME $TMP_DIR/heatmap_data_lastmonth.tif

gdaldem color-relief $TMP_DIR/heatmap_data_lastmonth.tif $HEATMAP_COLORS $TMP_DIR/heatmap-lastmonth.tif

gdalwarp -r cubic -s_srs '+init=epsg:4326' -t_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs' -of Gtiff $TMP_DIR/heatmap-lastmonth.tif $TMP_DIR/heatmap-lastmonth-900913.tif

convert $TMP_DIR/heatmap-lastmonth-900913.tif -fill white -opaque black $TMP_DIR/heatmap-lastmonth-900913.png
convert $TMP_DIR/heatmap-lastmonth-900913.png $BORDERS -composite $OUTPUT_DIR/heatmap-lastmonth.png

#last 3 months
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap(date(now()-'3 month'::interval),date(now()))" PG:dbname=$DB_NAME $TMP_DIR/heatmap_data_last3month.tif

gdaldem color-relief $TMP_DIR/heatmap_data_last3month.tif $HEATMAP_COLORS $TMP_DIR/heatmap-last3month.tif

gdalwarp -r cubic -s_srs '+init=epsg:4326' -t_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs' -of Gtiff $TMP_DIR/heatmap-last3month.tif $TMP_DIR/heatmap-last3month-900913.tif

convert $TMP_DIR/heatmap-last3month-900913.tif -fill white -opaque black $TMP_DIR/heatmap-last3month-900913.png
convert $TMP_DIR/heatmap-last3month-900913.png $BORDERS -composite $OUTPUT_DIR/heatmap-last3month.png

#total (runs for 22min on intel i5 @ 2.4 Ghz
#gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap('1900-1-1'::DATE, date(now()))" PG:dbname=$DB_NAME $TMP_DIR/heatmap_data_total.tif
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap(date(now()-'12 month'::interval), date(now()))" PG:dbname=$DB_NAME $TMP_DIR/heatmap_data_total.tif

gdaldem color-relief $TMP_DIR/heatmap_data_total.tif $HEATMAP_COLORS $TMP_DIR/heatmap-total.tif

gdalwarp -r cubic -s_srs '+init=epsg:4326' -t_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs' -of Gtiff $TMP_DIR/heatmap-total.tif $TMP_DIR/heatmap-total-900913.tif

convert $TMP_DIR/heatmap-total-900913.tif -fill white -opaque black $TMP_DIR/heatmap-total-900913.png
convert $TMP_DIR/heatmap-total-900913.png $BORDERS -composite $OUTPUT_DIR/heatmap-total.png


