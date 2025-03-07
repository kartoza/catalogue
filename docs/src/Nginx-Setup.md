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

# Background

When your tile stores are set up, you need to host them as public 'xyz' tile services. This is simply a case of deploying apache or nginx (we describe the process using nginx here) and then hosting the tile directories. We use the following scheme for these tile store urls:

* http://maps.sansa.org.za/bluemarble - tiles for the global blue marble dataset
* http://maps.sansa.org.za/za_spot_2012 - National SPOT mosaic for South Africa
* http://maps.sansa.org.za/osm_africa - transparent overlay tiles for South Africa

As successive years of tiles are added, they will be published according to http://maps.sansa.org.za/za_spot_XXXX where the XXXX represents the year number.

# Nginx Installation

Install nginx using the following command:

```
sudo apt-get install nginx
```

# Create directory shares for nginx

Edit ``/etc/nginx/sites-enabled/default`` as sudo and set the file contents as per the listing below:

```
server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;

        root /usr/share/nginx/html;
        index index.html index.htm;

        server_name localhost, 41.74.158.9, maps.sansa.org.za;

        location /bluemarble {
                try_files $uri $uri/ =404;
        }
}
```

**Note** Your sysadmin will need to open port 80 on the firewall so that the server is publicly accessible.
