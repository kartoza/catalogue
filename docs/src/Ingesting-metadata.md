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

## This wiki explains how to ingest new metadata into the catalogue

1. First, Admin need to login to the catalogue server through ssh.
1. Make sure that the metadata files to be ingested are already in this path `/home/web/catalogue/deployment/data`.
  1. That path is shared between local storage and the catalogue container. 
1. Shell to the catalogue-uwsgi container. You need to make sure you are in `/home/web/catalogue/deployment/`.
1. Using the command `make shell`, you should able to get the container shell to work. You will get the log `Shelling in in production mode`.
1. Now, you are inside the catalogue container `root@uwsgi:/home/web/django_project#`
1. If you check the `data` path `root@uwsgi:/home/web/django_project/data#` you should find your metadata that you previously copied to `/home/web/catalogue/deployment/data`.
1. Run manage.py with a django command. There are many available django commands:
   * cbers_harvest -> This is for CBERS ingestor
   * dims_iif_harvest -> DIMS IIF metadata ingestor 
   * landsat_harvest -> Landsat ingestor
   * spot_harvest -> SPOT1, SPOT2, SPOT3, SPOT4, SPOT5 ingestor
   * spot67_harvest -> SPOT 6 and SPOT 7 ingestor

     The usage example: `python manage.py spot67_harvest` 

     Another example, suppose that the metadata is located on `/home/web/catalogue/deployment/data/SPOT/spot7`. You can type the following command: `python manage.py spot67_harvest --source=./data/SPOT` 
   * convert_GB2312_utf8 -> convert GB2312 to utf8 (CBERS04 metadata used to be in GB2312 encoding so it needs to be UTF8 before ingestion)

     For example, if you want to ingest CBERS04, you need to run `python manage.py cbers_harvest <your data path>`. For the CBERS04 you have to make sure first that your metadata in UTF8 format. If your metadatas in GB2312 encoding, you need to run `python manage.py convert_GB2312_utf8 <your_data_path>`, then you run the CBERS ingestor again. 

If you fail when you try to ingest, you can check the management code inside the `/home/web/catalogue/django_project/catalogue/management/commands` directory. Maybe you need to change the data path for your metadata manually. 

## Below is an example of NAMIBIA ingested. 

There are 10 metadata files in the NAMIBIA directory. I have copied those metadata to `/home/web/catalogue/deployment/data`
```

root@testenv:/EOSHARE/Karabo/CATALOGUE/CBERS/NAMIBIA# ls -al *.XML
-rw-r--r-- 1 nobody 4294967294 3878 Nov 19  2015 CB04-MUX-84-119-20151118-L20000024094.XML
-rw-r--r-- 1 nobody 4294967294 3878 Sep 28 11:18 CB04-MUX-84-119-20160925-L20000033415.XML
-rw-r--r-- 1 nobody 4294967294 3878 Nov 13  2015 CB04-MUX-86-120-20151112-L20000023022.XML
-rw-r--r-- 1 nobody 4294967294 3896 Jun 20  2016 CB04-P10-73-135-B2-20160620-L20000030540.XML
-rw-r--r-- 1 nobody 4294967294 3895 Jun  7  2016 CB04-P10-86-121-A2-20160607-L20000030108.XML
-rw-r--r-- 1 nobody 4294967294 3895 Jun  7  2016 CB04-P10-86-128-A1-20160607-L20000030121.XML
-rw-r--r-- 1 nobody 4294967294 3895 Jul 20  2016 CB04-P10-89-126-A1-20160720-L20000031706.XML
-rw-r--r-- 1 nobody 4294967294 3896 Jun 24  2016 CB04-P10-89-126-B1-20160624-L20000030704.XML
-rw-r--r-- 1 nobody 4294967294 3895 Jul 20  2016 CB04-P10-89-128-A2-20160720-L20000031711.XML
-rw-r--r-- 1 nobody 4294967294 3895 Jul 14  2016 CB04-P10-91-120-A2-20160714-L20000031228.XML
root@testenv:/EOSHARE/Karabo/CATALOGUE/CBERS/NAMIBIA# 

```
Login to the catalogue container using `make shell` then run the command after you get catalogue container shell
CBERS04 metadata has GB2312 encoding, so we need to convert to UTF8 first. 

### convert metadata to utf8 
```
root@uwsgi:/home/web/django_project# python manage.py convert_GB2312_utf8 /home/web/django_project/data/CBERS/NAMIBIA
Starting directory scan...
Converting CB04-P10-89-126-A1-20160720-L20000031706.XML ....
Converting CB04-P10-91-120-A2-20160714-L20000031228.XML ....
Converting CB04-P10-73-135-B2-20160620-L20000030540.XML ....
Converting CB04-MUX-84-119-20151118-L20000024094.XML ....
Converting CB04-P10-86-128-A1-20160607-L20000030121.XML ....
Converting CB04-P10-89-128-A2-20160720-L20000031711.XML ....
Converting CB04-MUX-84-119-20160925-L20000033415.XML ....
Converting CB04-P10-89-126-B1-20160624-L20000030704.XML ....
Converting CB04-MUX-86-120-20151112-L20000023022.XML ....
Converting CB04-P10-86-121-A2-20160607-L20000030108.XML ....
===============================
Products converted : 10 
Products failed to convert : 0 

### Ingest the CBERS04 metadata

root@uwsgi:/home/web/django_project# python manage.py cbers_harvest
Scanning folders in /home/web/django_project/data/CBERS/NAMIBIA
Trying to update
Product: CB04P1089126A120160720L20000031706
/home/web/django_project/data/CBERS/NAMIBIA/CB04-P10-89-126-A1-20160720-L20000031706-THUMB.JPG
CB04P1089126A120160720L20000031706.jpg
Imported scene : CB04-P10-89-126-A1-20160720-L20000031706.XML
Trying to update
Product: CB04P1091120A220160714L20000031228
/home/web/django_project/data/CBERS/NAMIBIA/CB04-P10-91-120-A2-20160714-L20000031228-THUMB.JPG
CB04P1091120A220160714L20000031228.jpg
Imported scene : CB04-P10-91-120-A2-20160714-L20000031228.XML
Trying to update
Product: CB04P1073135B220160620L20000030540
/home/web/django_project/data/CBERS/NAMIBIA/CB04-P10-73-135-B2-20160620-L20000030540-THUMB.JPG
CB04P1073135B220160620L20000030540.jpg
Imported scene : CB04-P10-73-135-B2-20160620-L20000030540.XML
Trying to update
/home/web/django_project/data/CBERS/NAMIBIA/CB04-MUX-84-119-20151118-L20000024094-THUMB.JPG
CB04MUX8411920151118L20000024094.jpg
Imported scene : CB04-MUX-84-119-20151118-L20000024094.XML
Trying to update
Product: CB04P1086128A120160607L20000030121
/home/web/django_project/data/CBERS/NAMIBIA/CB04-P10-86-128-A1-20160607-L20000030121-THUMB.JPG
CB04P1086128A120160607L20000030121.jpg
Imported scene : CB04-P10-86-128-A1-20160607-L20000030121.XML
Trying to update
Product: CB04P1089128A220160720L20000031711
/home/web/django_project/data/CBERS/NAMIBIA/CB04-P10-89-128-A2-20160720-L20000031711-THUMB.JPG
CB04P1089128A220160720L20000031711.jpg
Imported scene : CB04-P10-89-128-A2-20160720-L20000031711.XML
Trying to update
Product: CB04MUX8411920160925L20000033415
/home/web/django_project/data/CBERS/NAMIBIA/CB04-MUX-84-119-20160925-L20000033415-THUMB.JPG
CB04MUX8411920160925L20000033415.jpg
Imported scene : CB04-MUX-84-119-20160925-L20000033415.XML
Trying to update
Product: CB04P1089126B120160624L20000030704
/home/web/django_project/data/CBERS/NAMIBIA/CB04-P10-89-126-B1-20160624-L20000030704-THUMB.JPG
CB04P1089126B120160624L20000030704.jpg
Imported scene : CB04-P10-89-126-B1-20160624-L20000030704.XML
Trying to update
/home/web/django_project/data/CBERS/NAMIBIA/CB04-MUX-86-120-20151112-L20000023022-THUMB.JPG
CB04MUX8612020151112L20000023022.jpg
Imported scene : CB04-MUX-86-120-20151112-L20000023022.XML
Trying to update
Product: CB04P1086121A220160607L20000030108
/home/web/django_project/data/CBERS/NAMIBIA/CB04-P10-86-121-A2-20160607-L20000030108-THUMB.JPG
CB04P1086121A220160607L20000030108.jpg
Imported scene : CB04-P10-86-121-A2-20160607-L20000030108.XML
===============================
Products processed : 10 
Products updated : 2 
Products imported : 8 
Products failed to import : 0 
===============================
```

### 8 metadata files ingested and 2 updated 
* '2 updated' means the data are already in the database. The system will update that record with the current metadata values

## Troubleshooting
### No Ingestion
When all steps have been taken and you are very sure that all the metadata is under the specified directory, yet the end result is something like this:
```
===============================
Products processed : 0 
Products updated : 0 
Products imported : 0 
Products failed to import : 0 
===============================
```

Try to add the path to the metadata in the command. 

For example, if your metadata is located under `/home/web/django_project/data/CBERS/NAMIBIA` folder, you can type:
```
root@uwsgi:/home/web/django_project#python manage.py cbers_harvest --source=./data/CBERS/NAMIBIA
```

Notice how the path is written in the *source* argument: `./data/CBERS/NAMIBIA`

The current folder is `/home/web/django_project`

A dot means starting from the current folder.

### Thumbnails Don't Show Up

Before do the ingestion, make sure all the thumbnail files use lowercase extension `.jpg`. 

If the extension is happened to be on the uppercase extension `.JPG`, a simple shell command can do the trick.
Make sure you are on the same folder with the thumbnail files that you would like to change. 

Then, you can type this command on the terminal:

`rename 's/\.JPG$/.jpg/' * `

The command tells the shell to rename all files end with .JPG into .jpg.
