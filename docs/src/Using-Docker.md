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

# Catalogue on Docker

This page explains how catalogue is maintained using docker.
Shell or command line interface (CLI) is used to execute all the commands below.

## Images
All required apps have been build and packed into docker images on the server.
These images would then be executed as containers.

## Containers  
Catalogue runs on top of docker containers.
To see the list of docker containers, type: `docker ps`.

Then, a list of containers along with its images and ports are shown.

From here, you could go into a container based on the need, for example: a database container.

To go into database, type: `docker exec -it catalogue-db bash`.
Type `docker` when asking for a password.

You would be on the catalogue db container. Please note that this is not the real database, it's just a container serves as database. Type: `psql -h localhost -U docker "dbname=gis" -p 5432` to go to Postgres interactive terminal.
From here, you can type any sql commands.

If you keen to learn more about docker, you can go to [documentation page](https://docs.docker.com).

## Database backup

### About Database backup
`catalogue-db-backups` is the name for a docker container running a cron job backing up database.
The backup process run on a daily basis at 11 PM.
All the backup files are stored in the `/home/web/catalogue/deployment/backups.`
The files are organised based on *YEAR/MONTH* folder.

### The configuration of database backup
`/home/web/catalogue/deployment/docker-compose.yml` specifies configuration setting for database backup.

Look for `dbbackups` section on the file. 

The following variables are used within the file:

`PGUSER` : user name for connection to database
`PGPASSWORD` : password for connection to database
`PGPORT` : specify port to connect to database
`PGHOST` : the name of host
`PGDATABASE` : the name of the database


