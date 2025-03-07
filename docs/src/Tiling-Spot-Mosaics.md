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

1. Go to the TLTIF_10m directory for the mosaic
2. Unzip all files: FILES=`ls *.gz`;do gunzip $FILE; done
3. Build a virtual mosaic by doing this: gdalbuildvrt za2010_10mtif.vrt *.tif
4. Generate the tileset by doing this:


```bash
gdal2tiles.py -s EPSG:4326 -z 1-15 -e -t \
    "SPOT 2010 10m Mosaic for South Africa." \
    -u http://maps.sansa.org.za/2010/ \
    -c "2014 SpotImage and SANSA" za2010_10mtif.vrt 2010-10m-SPOT-tiles
```
