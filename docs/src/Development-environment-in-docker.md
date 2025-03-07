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

# Development Setup

## Prerequisites

* you should have `postgresql-client-9.3` (or more recent) installed on the host.
* you should be using at least docker v 1.2.

## Docker Setup:

Run the postgis test server in docker:

```
docker build -t kartoza/postgis git://github.com/kartoza/docker-postgis
docker run --name="catalogue-postgis" \
           --hostname="catalogue-postgis" \
           --restart="always" -d -t kartoza/postgis
```

### Load the dump:

```
./pg_restore -f catalogue.dmp | psql -h 172.17.0.89 -U docker gis
```

**Note**: You should replace ``172.17.0.89`` with the IP address of your postgis container.



### Run the development container. 

This is a simple container with all deps installed in a venv under /home/web/catalogue and ssh.:

```
cd <this repository root>
./build.sh
./run-dev-docker.sh
```

This will mount your django project directory into `/home/web/catalogue/django_project` inside the container. The container will have a user whose gid and uid matches yours so that there are no permissions issues.

**Note**: The above setup is not intended to be secure - it is intended to provide a repeatable development environment.

## Pycharm configuration

Now set up your pycharm so that you can work with your dev container as a 'remote' container.

First in `File --> Settings --> Python Interpreter` add a remote interpreter with the following details:

* Host: localhost
* Port: 8001
* User name: docker
* Auth Type: Password
* Password: docker
* Python interpreter path: `/home/web/catalogue/venv/bin/python`

Then setup your django integration in `File --> Settings --> Django`:

* Django project root: `<path_to_project>/catalogue/django_project`
* Settings: `core/settings/dev_<yourname>.py`
* Manage script: `manage.py`

Now set up your run configuration under `Run -> Edit configurations`:

* Add a Django server configuration
* Host: 0.0.0.0
* Port: 8000
* Run in browser: http://localhost:8000/
* Environment variable: DJANGO_SETTINGS_MODULE=core.settings.dev_<yourname> (should be there automatically)
