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

# DevOps Documentation  

The DevOps guide provides structured documentation on DevOps practices, tools, and workflows used in software development and deployment.  

## Deploying with Docker  

This document explains how users can perform various system administration tasks when deploying a site using Docker. The following deployment modes are supported:  

- **Production**: Debugging is disabled, and a discrete database is used. Users should configure the production environment in `core.settings.prod_docker`. This `DJANGO_SETTINGS_MODULE` is used when running in production mode.  
- **Staging**: Users should configure the staging environment in `core.settings.staging_docker`. This `DJANGO_SETTINGS_MODULE` is used when running in staging mode.  

## Build Docker Images and Run Them  

### Production  

Users can run the provided script to build and deploy Docker images in `production mode`:  

```bash
cd deployment
# Allow PostgreSQL volume to be written to
sudo chmod -R a+rwX pg/postgres_data/
make deploy
sudo chmod -R a+rwX static
```

### Running in Development Mode  

Users can run `makedev` in the terminal.  

Then, connect to the Django container and run:  

```bash
python manage.py runserver 0.0.0.0:8080
```

- `Pycsw` runs on port `8000`.  
- Users can access the web container via port `8080` or as defined in the `fig.yml` file.  

To create a superuser account, run:  

```bash
make shell
python manage.py createsuperuser
exit
```

### Staging  

The staging deployment follows the same process as production, but users should precede each command with `staging`, e.g.,  

```bash
make staging-deploy
```

>Note: For staging deployment, users should use a `separate Git checkout` from the production checkout, as the Git checkout code is shared into the source tree.  

## Using Make  

Key `make` commands for production include:  

- **build** – Builds production containers.  
- **run** – Builds and runs database and `uwsgi` services.  
- **collectstatic** – Collects static files for production.  
- **migrate** – Runs Django migrations in production.  

Additional `make` commands are available in the `Makefile`.  

### Running Arbitrary Commands  

Users can execute arbitrary management commands easily within the container.  

## Setting Up an Nginx Reverse Proxy  

Users should create a new `Nginx virtual host`. Example configurations are available in `*-nginx.conf` in the `deployment` directory, with separate configurations for `production` and `staging`.  

To apply these configurations:  

1. Copy the example file (renaming if necessary) to `/etc/nginx/sites-enabled/`.  
2. Modify the contents to match the local file system paths.  
3. Verify the configuration:  

   ```bash
   sudo nginx -t
   ```

4. Reload or restart Nginx:  

   ```bash
   sudo /etc/init.d/nginx restart
   ```

## Managing Containers  

For managing infrastructure, refer to the [Fig documentation](http://www.fig.sh/cli.html).  

## Configuration Options  

Users can configure the `base port`, `image organisation namespace`, `PostGIS user/password`, and other settings by modifying the `fig*.yml` files.  
