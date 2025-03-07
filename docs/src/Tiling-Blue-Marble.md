---
title: SANSA Catalogue
summary: PROJECT_SUMMARY
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/kartoza/catalogue
copyright: Copyright 2023, PROJECT_OWNER
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#context_id: 1234
---

Recipe for creating a tileset for Blue Marble

* Ensure you have gdal-bin installed: ``sudo apt-get install gdal-bin gdal-python``

* Add this line to the end of ``/usr/share/proj/epsg/``: 
```
# Google Mercator added by Tim
<900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs
```


* Go to the Blue Marble directory containing untiled images for the mosaic (e.g. ``/home/maps/bluemarble``)
* Build a virtual mosaic by doing this: ``gdalbuildvrt bluemarble.vrt *.tif``
* Generate the tileset by doing this:

```bash
gdal2tiles.py -s EPSG:4326 -z 1-15 -e -t \
    "NASA Globale Blue Marble Mosaic." \
    -u http://maps.sansa.org.za/bluemarble/ \
    -c "http://visibleearth.nasa.gov/" bluemarble.vrt bluemarble-tiles
```
