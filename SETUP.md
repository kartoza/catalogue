Setup notes on a fresh server:

# Virtualenv and pip

We set up using a pip cache to make repeatable setup easy and fast:

Add to ~/.pip/pip.conf :

```
[global]
download_cache =  ~/.cache/pip
```

And make the pip dir:

```
mkdir ~/.cache/pip
```


Create the virtualenv:

```
virtualenv venv
```

Manually install gdal:

```
source venv/bin/activate
pip install --no-install GDAL
cd venv/build/GDAL/
python setup.py build_ext --include-dirs=/usr/include/gdal/
pip install --no-download GDAL
```

Installing uno
```
apt-get install python-uno
# copy system install over to venv
.../venv/lib/python2.7/site-packages ln -s /usr/lib/python2.7/dist-packages/uno.py
.../venv/lib/python2.7/site-packages ln -s /usr/lib/python2.7/dist-packages/unohelper.py
```


# Development database configuration

## Build docker db container

```
docker build -t kartoza/postgis:2.6 git://github.com/timlinux/docker-postgis
docker run --name="catalogue-postgis" -p 2000:5432 -p 20001:22 -t -d kartoza/postgis:2.6
psql -U docker -h localhost -p 2000 -l
```

(use 'docker' for the password)

## Restore dump to container

```
createdb -U docker -h localhost -p 2000 -T template_postgis catalogue
pg_restore drunk_elephant.dmp | psql -U docker -h localhost -p 2000 catalogue
```

``drunk_elephant`` being the name of the database dump to restore.


# PyCharm configurations:

## Django Server:

* Configuration type: Django server
* Host: localhost
* Additional options: ``--settings=core.settings.dev_timlinux``
*


## All Tests:

* Configuration type: Django tests
* Target: catalogue
* [x] Custom settings: ``/home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py``
* Working directory: /home/timlinux/dev/python/catalogue/django_project

## Test: Catalogue IIF Ingestors:

* Configuration type: Django tests
* Target: catalogue.tests.test_dims_iif_ingestor
* [x] Custom settings: ``/home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py``
* Working directory: /home/timlinux/dev/python/catalogue/django_project



## catalogue.tests.test_spot_ingestor:

Configuration type: Django tests

Target: catalogue.tests.test_spot_ingestor
[x] Custom settings: ``/home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py``
Working directory: /home/timlinux/dev/python/catalogue/django_project


# Ingesting IIF Data

```
python manage.py dims_iif_harvest --help  --settings=core.settings.dev_timlinux
Usage: manage.py dims_iif_harvest [options]

Imports DIMS Landsat records into the SANSA catalogue

Options:
  -v VERBOSITY, --verbosity=VERBOSITY
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings=SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath=PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on exception
  -t, --test_only       Just test, nothing will be written into the DB.
  -d SOURCE_DIR, --source_dir=SOURCE_DIR
                        Source directory containing DIMS IIF xml file and
                        thumbnail to import.
  -e HALT_ON_ERROR, --halt_on_error=HALT_ON_ERROR
                        Halt on first error that occurs and print a stacktrace
  -i IGNORE_MISSING_THUMBS, --ignore-missing-thumbs=IGNORE_MISSING_THUMBS
                        Continue with importing records even if they miss
                        theirthumbnails.
  --version             show program's version number and exit
  -h, --help            show this help message and exit

```

Real example of use:

```
python manage.py dims_iif_harvest -i True -d \
    "/home/timlinux/dev/python/catalogue/django_project/deliveries" \
    -e -v2  --settings=core.settings.dev_timlinux
```

# Ingesting SPOT data

```
python manage.py spot_harvest --help --settings=core.settings.dev_timlinuxUsage: manage.py spot_harvest [options]

Imports SPOT packages into the SANSA catalogue

Options:
  -v VERBOSITY, --verbosity=VERBOSITY
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings=SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath=PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on exception
  -f SHAPEFILE, --file=SHAPEFILE
                        Shapefile containing spot coverage data.
  -d DOWNLOAD_THUMBS, --download-thumbs=DOWNLOAD_THUMBS
                        Whether thumbnails should be fetched to. If not
                        fetched now they will be fetched on demand as needed.
  -t, --test_only       Just test, nothing will be written into the DB.
  -a AREA, --area=AREA  Area of interest, images which are external to this
                        area will not be imported (WKT Polygon, SRID=4326)
  -e HALT_ON_ERROR, --halt_on_error=HALT_ON_ERROR
                        Halt on first error that occurs and print a stacktrace
  --version             show program's version number and exit
  -h, --help            show this help message and exit
```

Example usage:

```
python manage.py spot_harvest -e True \
    -f /home/timlinux/dev/python/catalogue/django_project/SPOT_Coverage/Africa_2002_ACScorrected.shp \
    --settings=core.settings.dev_timlinux
```

# Debugging ingestors in pycharm

To run a management command you have to do:

* New configuration
* Django server (I know it is a little counter-intuitive)
* Additional options: Options for management commnad  ``-e True -f /home/timlinux/dev/python/catalogue/django_project/SPOT_Coverage/Africa_2002_ACScorrected.shp --settings=core.settings.dev_timlinux``
* [x] Run custom command: set the name of the command (without args) e.g. ``spot_harvest``

You can now run that command in debug mode with breakpoints etc.
