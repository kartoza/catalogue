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

# Backup Important Files

Cited from [Wikipedia](https://en.wikipedia.org/wiki/Backup):
```
a backup, or the process of backing up, refers to the copying and archiving of computer data so it may be used to restore the original after a data loss event. 
```

We see the backup as an additional layer in case something terrible happens.

Having extra layer, we hope the new server can be up again as soon as possible after unexpected event.

Docker images of `kartoza/pg-backup`, `kartoza/docker-sftp-backup`, and `docker-btsync` are used to do this job.

Before running the images, all images are required to be obtained locally.

## kartoza/pg-backup

This section provides technical explanation on how to implement the PostGIS database backup.
You can simply skip this part as the project has implemented this type of backup.

### Getting the image
#### pull

The easiest way to get an image is by pulling the image:
```
docker pull kartoza/pg-backup:9.4
```

#### build 

Although it takes more time to build an image, building the image locally will enable us to customise the image later.

Get the code from github by typing:

`git clone https://github.com/kartoza/docker-pg-backup` 

Then, type:

`cd docker-pg-backup`

Next, build it:

`docker build -t kartoza/pg-backups .`

### Running the image

If downloading the image is chosen, you can run the image by typing the following command:

`docker run --name="backups" --hostname="pg-backups" --link=watchkeeper_db_1:db -v backups:/backups -e PGUSER=bob -e PGPASSWORD=secret -link db -i -d kartoza/pg-backup`

If you decide to build the image yourself, make sure you have already in the repo folder. 
Then type this command in the shell:

`docker-compose up -d dbbackup`

Note that you need `docker-compose.yml`.
The sample of `docker-compose.yml` is given below:

```
dbbackups:
  image: kartoza/pg-backup:9.4
  hostname: pg-backups
  volumes:
    - ./backups:/backups
  links:
    - db:db
  environment:
    - DUMPPREFIX=PG_YOURSITE
    # These are all defaults anyway, but setting explicitly in
    # case we ever want to ever use different credentials
    - PGUSER=docker
    - PGPASSWORD=docker
    - PGPORT=5432
    - PGHOST=db
    - PGDATABASE=gis  
```

## kartoza/docker-sftp-backup
`docker-sftp-backup` can be used to store all important files (ex: thumbnails, user home folders), including the one from the `kartoza/pg-backup`.

It also can utilise spaces as the app will constantly delete the old files.

### Getting the image

To get the image, first we need to clone the repo first by typing:

`git clone https://github.com/kartoza/docker-sftp-backup`

Suppose we would like to store the code in `/home`, then running the above command, will create a directory in the following path: 

`/home/docker-sftp-backup`

Go to `/home/docker-sftp-backup` by typing:

`cd /home/docker-sftp-backup`

Now, we can build the image using:

`docker build -t kartoza/sftp-backup .`

### Running the image

To verify whether we have the image, we can type:

`docker ps | grep sftp-backup`

Make sure the `sftp-backup` image is on the list.

If we build the image from the scratch, make sure we are on the same directory as the cloned folder (`/home/docker-sftp-backup`).

Running the image is by using the following command:

`docker-compose up -d sftpbackup`

Before running the command, you may want to set up the environment first.

Open `docker-compose.yml`, then modify the parameters to your need.

A sample of docker-compose.yml:

```
sftpbackup:
  image: kartoza/sftp-backup
  hostname: sftp-backup
  volumes:
    # mount stored backups folder to a folder in docker container
    - ./backups:/backups
    # mount source for the backups folder to a folder in docker container
    - /home/target_dirs:/targets
  environment:
    - DUMPPREFIX=PG_CATALOGUE
    - DAILY=14
    - MONTHLY=12
    - YEARLY=3
    # set this to the target/source folder where the backup comes from
    - TARGET_FOLDER=/targets
  env_file:
    - sftp_credential.env
```

Please note that we specify `sftp_credential.env` file here. 
This file contains the required credentials to use sftp protocol.
A sample of `sftp_credential.env` is:

```
export DUMPPREFIX=backup
export TARGET_FOLDER=/targets
export DAILY=7
export MONTHLY=12
export YEARLY=3
export USE_SFTP_BACKUP=False
export SFTP_HOST=localhost
export SFTP_USER=user
export SFTP_PASSWORD=password
export SFTP_DIR=/
``` 

## docker-btsync
This image runs BitTorrent Sync.

When there are several servers or storages, `docker-btsync` can be used to distribute the backup across these sites.

We can also use this image as an alternative data transmitting against FTP protocol. 

The location of the backup folders is required and to be specified. 

Then, it will auto sync with any BT clients installed in the targeted servers and/or storages. 

### Getting the image

Download the github repo: 

`git clone https://github.com/kartoza/docker-btsync` 

Then, type: 

`docker build -t kartoza/btsync .`

Another way to build the image without download the repo is:

`docker build -t kartoza/btsync git://github.com/kartoza/docker-btsync`

### Running the image

Type:

`docker-compose up -d kartoza/btsync`

Don't forget to set `btsync.conf` accordingly, including the `shared_folders` parameters.
