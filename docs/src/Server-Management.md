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

This page explains some useful commands for administering the production server.

# Server

## Restart Server
*Note: Please don't restart server frequently, as we don't have any backup server yet.*

If a change is made and it requires to restart the server, there are 2 ways (depends on the scope of the changes):
- Go to `/home/web/catalogue/deployment` and type: `make reload`. 

  This command will restart uwsgi container.

  If the changes don't immediately take place, try this command:

  `docker-compose -p catalogue restart uwsgi`

- `docker-compose -p catalogue up -d web`

  This will restart the web server (nginx and uwsgi containers).

# Database

## Database Container

If for some reasons you need to go to the database via a terminal, you can do:
- Go to `/home/web/catalogue/deployment`
- Type: `make dbshell`
- Type *docker* when asking a password
- You are already inside the database container.

## Database Backup Files

The database is backed up daily at 00.00 AM.

The location of the backup files is `/home/web/catalogue/deployment/backups`.

The backup file naming convention is `PG_catalogue_gis.<date_of_backup>.dmp`.

The backup files is stored based on year and month folders.

Suppose you are looking for a last backup file dated on 3 March 2017, then you can find the backup file under `/home/web/catalogue/deployment/backups/2017/March` folder. 
From this folder, you should expect a file called `PG_catalogue_gis.03-March-2017.dmp`.
