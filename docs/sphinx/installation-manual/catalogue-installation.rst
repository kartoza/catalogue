Catalogue Software Installation
-------------------------------

Prepare your system
^^^^^^^^^^^^^^^^^^^

You need to be running Django  >= 1.2.1 for the catalogue to work. Ubuntu Lucid
and Debian Lenny ship with older versions so do a manual build. We walk through this
setup using the python virtual environment system.

Create working dir
^^^^^^^^^^^^^^^^^^

Do this (on the server)::

   cd /opt
   mkdir sac
   cd sac

Or on a desktop development system::
   
   cd /home
   sudo mkdir web
   sudo chown -R <username>.<username> web
   cd web
   mkdir sac



Setup python virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We install Python in a virtual environment on Ubuntu and Debian, to be able to
install Django 1.2 separate from the "System Python" and avoid conflicts.

If you do not have the Python virtualenv software, get it with::

  sudo apt-get install python-virtualenv \
  build-essential \
  python-dev \
  python-all-dev \
  python-profiler \
  python-dateutil

Now, start the Python virtual environment setup. We install Python in the
"python" subfolder of the project directory and then activate the virtual
environment.::

  virtualenv --no-site-packages python
  source python/bin/activate

Set your ssh config up
^^^^^^^^^^^^^^^^^^^^^^

To get started, first add an entry like this to your ssh config file in 
:file:`~/.ssh/config`::

   Host rhino
     User <your user>
     Port 8697
     HostName hbk-rhino.sansa.org.za
     FallBackToRsh no  

   Host lion
     User <your user>
     Port 8697
     HostName hbk-lion.sansa.org.za
     FallBackToRsh no  
     
   Host elephant
     User <your user>
     Port 8697
     HostName hbk-elephant.sansa.org.za
     FallBackToRsh no  


Checkout Sources
^^^^^^^^^^^^^^^^

Then setup a working dir and check out the sources (you can adapt dirs / paths
as needed, using these paths will keep you consistent with all setup notes but
its not required).::


Now you can check out either from linfiniti's repo:

``git clone git@github.com:timlinux/catalogue.git``

or from SANSA's repo:

``git clone git@orasac1:sac_catalogue.git sac_catalogue``


.. note:: Your sysamdin will need to make an account for you on github or
   your local repo.


Install some development dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On older ubuntu systems.

``sudo apt-get install libpq-dev libpq4 libpqxx-dev libxslt1-dev``

On newer editions of ubuntu you may need to use libpq5 rather:

``sudo apt-get install libpq-dev libpq5 libpqxx3-dev libxslt1-dev``

Then make sure the virtual environment is active:

``source ../python/bin/activate``

.. note:: After running this you should see (python) in front of your prompt.

On older ubuntu versions you need to install easy_install so that we can use
pip thereafter (not needed for ubuntu 12.04):

``easy_install pip``

Informix DB Support
^^^^^^^^^^^^^^^^^^^

.. note:: This is only needed on machines that will be doing updates from
   the legacy acs system.

You need to have the informix client sdk installed on the machine first.

Then make sure the virtual environment is active:

``source ../python/bin/activate``

Then extract the python informix client to tmp and install it into your venv::
   
   cd /tmp/
   tar xfz /home/timlinux/Informix/InformixDBPython-2.5.tar.gz
   cd InformixDB-2.5/
   python setup.py build_ext
   python setup.py install


GDAL Python Bindings
^^^^^^^^^^^^^^^^^^^^

**On your test system**::

   sudo apt-get install python-gdal gdal-bin libgdal1-dev

The gdal python bindings (which are installed using the REQUIREMENTS file in
the section that follows) did not compile without swq.h header. I copied
the aforementioned header into /usr/local/include. The header file is available
here::

   http://svn.osgeo.org/gdal/branches/1.7/gdal/ogr/swq.h

Please see the webmapping chapter (600-webmapping.rst) for notes on the setup
process for GDAL

.. note:: When installing gdal from source and you want the python bindings
   installed into your python virtual env, make sure to activate the virtual
   environment before building gdal so that its bindings are placed in the v.env
   site packages dir.

GDAL Python Bindings - Ubuntu 12.04 - Python virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Optional:**

You may want to upgrade to newer gdal:: 
   
   sudo gedit /etc/apt/sources.list

Then add these two lines

   deb http://ppa.launchpad.net/ubuntugis/ubuntugis-unstable/ubuntu precise main 
   deb-src http://ppa.launchpad.net/ubuntugis/ubuntugis-unstable/ubuntu precise main


Now upgrade your gdal doing this::
   
   sudo apt-get update
   sudo apt-get upgrade
   dpkg -l | grep gdal
   sudo apt-get install gdal-bin
   sudo apt-get install libgdal-dev

If your gdal does not work, try the procedure below.

**On your test system**::

   pip install gdal==1.7.0

.. note:: the gdal version should match your system installed gdal.

**On the live system (legacy notes)**

To install GDAL Python bindings in virtual environment, manual installation
is required. 

.. warning:: On live server dont forget to copy swq.h header, in active
   virtual environment execute:

First delete GDAL folder ``$VIRTUAL_ENV/build/GDAL``, if it exists.

On Ubuntu 12.04 we have 1.7.2 GDAL library, so we need to install correct
Python GDAL library from pypi::
   
   pip install --no-install GDAL==1.7
   cd $VIRTUAL_ENV/build/GDAL
   rm setup.cfg
   python setup.py build_ext --gdal-config=gdal-config --library-dirs=/usr/lib \
     --libraries=gdal1.7.0 --include-dirs=/usr/include/gdal install


Now test if your python gdal bindings are there::

   python -m gdal

The test is a success if there is no output from the above command.


Install django and required django apps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install django, django authentication etc into our virtual environment do::
   
   pip install -r sac_catalogue/REQUIREMENTS.txt


Then make sure the appropriate settings from djangodblog in settings.py.templ are 
deployed in your production settings.py

The full list of packages installed using the REQUIREMENTS file is:

.. literalinclude:: ../../REQUIREMENTS.txt

Next manually install PIL as shown below (**mandatory**).

PIL Issues
^^^^^^^^^^

You need to manually build PIL into your virtual environment and you should
avoid using the installed python-imaging (the debian pil package) on your
system that is needed by tilecache.

If thumbnails produced are being corrupted or you get an error like this
when trying to view jpg thumbs::

   decoder jpeg not available

then our PIL is missing jpg (and probably png support). To fix it do::
   
   ../python/bin/activate
   pip uninstall pil
   sudo apt-get install libjpeg-dev libfreetype6 libfreetype6-dev
   wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
   tar xfz Imaging-1.1.7.tar.gz
   cd Imaging-1.1.7

Now edit setup.py to set these (for 64 bit)::
   
   TCL_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
   JPEG_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
   ZLIB_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
   TIFF_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
   FREETYPE_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"


Now edit setup.py to set these (for 32 bit)::
   
   TCL_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   JPEG_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   ZLIB_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   TIFF_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   FREETYPE_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"


Test if your configs work::
   
   python setup.py build_ext -i

The build report should show::
   
   *** TKINTER support not available (Tcl/Tk 8.5 libraries needed)
   --- JPEG support available
   --- ZLIB (PNG/ZIP) support available
   --- FREETYPE2 support available
   *** LITTLECMS support not available

Now build pil::
   
   python setup.py install

Further info on django registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may also want to read this `article on <http://devdoodles.wordpress.com/2009/02/16/user-authentication-with-django-registration/>`_
if you want more info on how the registration stuff works.  
  
.. note:: You need to log in to the admin area of the site and change the
   domain name in the sites table from something other than 'example.com',
   otherwise the registration middleware will send the reminder with an incorrect
   url.


Settings configuration
^^^^^^^^^^^^^^^^^^^^^^

Copy :file:`settings.py.template` to :file:`settings.py` and then 
modify settings.py as needed (probably you just need to set 
the eth adapter and db connection settings).

Database setup
^^^^^^^^^^^^^^

Create the database using::
   
   createlang plpgsql template1
   psql template1 < /usr/share/postgresql-8.3-postgis/lwpostgis.sql
   psql template1 < /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql
   createdb sac
   createdb acs

.. warning:: There is a known bug with django 1.2 and postgresql 9.1, 
   which requires that you make the following alteration to your postgresql.conf
   configuration::
      
      ###########################
      #Added by Tim
      ###########################
      #see https://code.djangoproject.com/ticket/16778
      standard_conforming_strings = off



For an empty database:
^^^^^^^^^^^^^^^^^^^^^^

Sync the model to the db (dont do this is you plan to restore an existing db as
explained in the next section):

``````````````````````````````````````````
python manage.py syncdb --database=default
``````````````````````````````````````````

And if you have the legacy acs catalogue do:

``````````````````````````````````````
python manage.py syncdb --database=acs
``````````````````````````````````````

The django fixtures included with this project should populate the 
initial database when you run the above command.

Restoring an existing database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nightly backups are made on lion at:

``````````````````````````````````````````````
/mnt/cataloguestorage1/backups/YEAR/MONTH/DAY/
``````````````````````````````````````````````

To restore the backup do::
   
   pg_restore sac_postgis_30August2010.dmp | psql sac
   pg_restore acs_postgis_30August2010.dmp | psql acs


Setup apache (mod  python way)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning:: This will be deprecated in favour of mod_wsgi
    (see next section)

Make sure you have mod_expires and mod_deflate installed.

The assumption is that you are using name based virtual hosts and that the 
catalogue will run at the root of such a virtual host. Add to you apache site
config::

   cd apache
   cp apache-site-modpy.templ catlogue-modpy

Modify as appropriate your closed catalogue-modpy file the source tree then
link it to apache.::
   
   sudo ln -s catlogue-modpy /etc/apache2/sites-available/catalogue-modpy

Also do::
   
   sudo apt-get install libapache2-mod-python

Now deploy the site::
   
   sudo a2ensite catalogue-modpy
   sudo /etc/init.d/apache reload


Setup apache (mod_wsgi way)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The assumption is that you are using name based virtual hosts and that the 
catalogue will run at the root of such a virtual host. Add to you apache site config:

Modify as appropriate a copy of the apache-site-wsgi.templ file found in the apache 
dir in the source tree then link it to apache::
   
   cd apache
   cp apache-site-wsgi.templ catlogue-wsgi

Now create a symlink::
   
   sudo ln -s catlogue-wsgi /etc/apache2/sites-available/catalogue-wsgi

Also do::
   
   sudo apt-get install libapache2-mod-wsgi

Now deploy the site::

   sudo a2ensite catalogue-wsgi
   sudo /etc/init.d/apache reload

Copy over the ribbon
^^^^^^^^^^^^^^^^^^^^

There is a ribbon image that displays in the top left corner of the site that
is used to convey version numbers etc. Since this may vary from deployment to
deployment, you should copy over an appropriate ribbon e.g.::
   
   cp media/images/ribbon_template.png media/images/ribbon.png


Install GEOIP data
^^^^^^^^^^^^^^^^^^

GeoIP is used to resolve IP addresses to Lon/Lat. This directory needs the
GeoIP lite dataset in it::
   cd geoip_data
   wget http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
   gunzip GeoLiteCity.dat.gz`

Check settings.py!
^^^^^^^^^^^^^^^^^^

Go through settings.py (after first copying it from settings.py.templ if
needed) and check all the details are consistent in that file.

Install proxy.cgi - note this will be deprecated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some parts of this site use cross site XHttpRequests. This is not allowed in
the spec (to prevent cross site scripting attacks) so to get around this you
need to install a proxy cgi on the django hosting server *if the mapserver
instance is on a different physical server*::
   
   cd /usr/lib/cgi-bin
   sudo wget -O proxy.cgi \
   http://trac.openlayers.org/browser/trunk/openlayers/examples/proxy.cgi?format=raw
   sudo chmod +x /usr/lib/cgi-bin/proxy.cgi

Once you have installed the proxy.cgi you need to configure it to tell it the 
list of allowed servers it can proxy for. This is to prevent it becoming 
an open relay on the internet. Edit /usr/lib/cgi-bin/proxy/cgi and change 
line 18 to look like this::

   allowedHosts = [ '196.35.94.243','lion', ]

I also changed line 32 to look like this::
   
   url = fs.getvalue('url', "http://196.35.94.243")


so that the default proxy url is our wms server. See 
http://faq.openlayers.org/proxyhost/all/ for more info...


Creating branches
^^^^^^^^^^^^^^^^^

.. note:: This section uses svn commands and should be updated to use git
   equivalents.

When the code gets stabilised to a certain point you should create a branch 
to mark that stable code base and then deploy it on the live server. To 
create the branch do e.g.::

   svn cp https://196.35.94.196/svn/trunk/sac_catalogue \
   https://196.35.94.196/svn/branches/catalogue_v1_beta3

Where:
**v1** = version 1
**beta3** = the current status of that major version

Backup of the web server
^^^^^^^^^^^^^^^^^^^^^^^^

```
sudo dd if=/dev/sdb | ssh definiens4 "dd of=/cxfs/dd_backups/orasac1/orasac1_sdb_`date +%a%d%b%Y`.dd"
sudo dd if=/dev/sda | ssh definiens4 "dd of=/cxfs/dd_backups/orasac1/orasac1_sda_`date +%a%d%b%Y`.dd"
`````````````````````````````````````````````````````````````````````````````````````````````````````


Creation of the ReadOnly db user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This should be done on the database server i.e. elephant

This user is required for mapserver access to some of the tables::
   
   sudo su - postgres
   createuser -S -D -R -l -P -E -e readonly
   exit
   psql sac
   grant select on vw_usercart to readonly;
   grant select on visit to readonly;
   grant select on sensor to readonly;
   \q

Optimal database configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To support the large number of recs tweak
:file:`/etc/postgresql/8.3/main/postgresql.conf`

```
# Changed by Tim as the sac db required more
max_fsm_pages = 500000
``````````````````````

Then restart the db

```````````````````````````````````
sudo /etc/init.d/postgresql restart
```````````````````````````````````

set some file permissions
^^^^^^^^^^^^^^^^^^^^^^^^^

Apache user needs write access in avatars:

```
sudo chgrp www-data media/avatars
sudo chmod g+w media/avatars
````````````````````````````

ER Diagram
^^^^^^^^^^

You can generate an ER diagram for the application using the django command
extensions:


To generate the graph use:

```
python manage.py graph_models catalogue > docs/catalogue_diagram.dot
cat docs/catalogue_diagram.dot | dot -Tpng -o docs/catalogue_diagram.png ; \
display docs/catalogue_diagram.png
``````````````````````````````````

Troubleshooting
^^^^^^^^^^^^^^^

settings.py not found
^^^^^^^^^^^^^^^^^^^^^

This is usually a symptom that one of the imports withing settings.py failed.
Test by doing:

``````
python
``````

Then at the python prompt do

```````````````
import settings
```````````````

The error you obtain there (if any) will be more descriptive.


Sentry Setup
------------

We use sentry to log events and provide over time history of issues. The
process is described well here: http://sentry.readthedocs.org/en/latest/quickstart/index.html

Here is the log of the setup process I did, and any variations on the process
documented above::

  mkdir sentry
  cd sentry/
  virtualenv python
  source python/bin/activate
  pip install sentry
  sentry init sentry.conf.py
  sentry --config=sentry.conf.py upgrade
  vim sentry.conf.py 

At this point I needed to add the following to the top of the file::

  #Added by Tim
  from sentry.conf.server import *
  INSTALLED_APPS = INSTALLED_APPS + (
           'gunicorn',
  )


Then setup apache to use a reverse proxy.::

  sudo vim /etc/apache2/sites-enabled/catalogue.wsgi 

And add these lines::

  ProxyPass /sentry/ http://localhost:9000/
  ProxyPassReverse /sentry/ http://localhost:9000/
  <Location /sentry/>
    Order deny,allow
    Allow from all
    SetHandler None
  </Location>

Check that mod_proxy is installed then restart::

  sudo a2enmod proxy
  sudo /etc/init.d/apache2 reload

Now run sentry and it should bd available at http://catalogue.sansa.org.za/sentry/

.. note:: The above embedding into existing site doesnt work - css doesnt show.
   We will host it under its own subdomain.


  sentry --config=sentry.conf.py start


Sentry client setup
-------------------


On client we need to add ``raven`` to application virtualenv::

  pip install raven

Make sure to add ``'raven.contrib.django'`` to **INSTALLED_APPS** list in
settings.py.

Then in local setting.py, we need to update following config parameters
(default settings are already present in settings.py.template)::

  from raven.conf import setup_logging
  from raven.contrib.django.handlers import SentryHandler
  import logging

  logging.getLogger().setLevel(logging.ERROR)
  logging.getLogger().addHandler(SentryHandler())
  setup_logging(SentryHandler())

  # Sentry server client settings
  SENTRY_DSN = 'http://74b4e04b3738403c9670c8b67bb602c0:36f52a2271094938b2e8739e562bb37c@localhost:9000/2'

  # only if running with DEBUG=True ( DEVELOPMENT ENV )
  # and we want to catch exceptions with sentry
  # RAVEN_CONFIG = {
  #     'register_signals': True,
  # }

Most important settings are ``logging.getLogger().setLevel()`` and ``SENTRY_DSN``:

  * ``setLevel`` sets which level of messages are sent to Sentry (for production use logging.ERROR)
  * ``SENTRY_DSN`` we can get this on sentry server when we create project

Currently commented out section is only relevant if we want to catch
exceptions with sentry in development environment (DEBUG=True).
