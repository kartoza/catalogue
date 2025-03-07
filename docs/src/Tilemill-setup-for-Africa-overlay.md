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

## Tile server setup notes:

We are publishing OpenStreetmap transparent tiles - a modified version of the [OSM Bright](https://github.com/mapbox/osm-bright) project.


```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"

sudo apt-get update
sudo apt-get install -y lxc-docker git rpl byobu postgresql-client-9.3
sudo usermod -a -G docker <username>

mkdir -p ~/dev/docker
cd ~/dev/docker
git clone https://github.com/kartoza/docker-tilemill.git
git clone https://github.com/kartoza/docker-postgis.git

cd docker-tilemill
./build.sh

cd ..
cd docker-postgis
./build.sh

cd ..
```

## Create the postgis container and load it:

Password is ``docker``, username is ``docker``. The ``osm.dmp`` was copied over from the local machine.

```
docker run --name="osm-africa-postgis" \
        -d -t -p 5432:5432 kartoza/postgis

# Test
psql -l -h localhost -p 5432 -U docker


createdb -h localhost -p 5432 -U docker -T template_postgis osm
pg_restore osm.dmp | psql -h localhost -p 5432 -U docker osm

```

**Note:** You should be able to ignore any errors like the one below since the occur because the docker database already has postgis installed into it:

```bash
ERROR:  function "srid" already exists with same argument types
```



## Create the tilemill container:

Note that the ``Documents/MapBoxdir`` was copied over from my local machine

```
cd ~/Documents/MapBox/project/OSMAfrica
rpl "172.17.0.2" "41.74.158.9" *

docker.io run \
        --name=tilemill \
        --link osm-africa-postgis:osm-africa-postgis \
        -v /home/<username>/Documents/MapBox:/Documents/MapBox \
        -p 20008:20008 \
        -p 20009:20009 \
        -d \
        -t kartoza/tilemill
```

## When the server reboots

The docker containers will be brought down on reboot. To bring them up again simply do:

```
docker start osm-africa-postgis
docker start tilemill
```

**Note:** You should replace ``<username>`` with your actual username throughout this document.
