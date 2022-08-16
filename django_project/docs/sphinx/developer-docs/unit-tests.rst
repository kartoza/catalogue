=====================
Testing the Catalogue
=====================

Quickstart
----------

The catalogue is provided with a test suite. You can run it like this::

   ./runtests.sh


Testing overview
----------------

Two kinds of tests are provided:

- DocTests ([see http://ericholscher.com/blog/2008/nov/2/introduction-pythondjango-testing-doctests/])
- UnitTests ([see http://ericholscher.com/blog/2008/nov/4/introduction-pythondjango-testing-basic-unit-tests/ ])
-

For simple tests, you can edit catalogue/tests/simple_tests.py and add additional tests, or add additional files
containing doctests. Each test file you create must be registered in catalogue/tests/__init__.py.

To power the tests, various fixtures have been created in catalogue/fixtures which will be loaded in the
test database each time you run the tests. For more info on generating fixtures, [see http://ericholscher.com/blog/2008/nov/5/introduction-pythondjango-testing-fixtures/].

Creating Fixtures
-----------------

Here is the procedure followed to create fixtures for testing:

**Note:** This is a once off exercise and is probably not needed as the
fixtures generated now reside in git. The procedure is noted here in case it
ever needs to be repeated::

   pg_dump -Fc -f sac-test-20June2011.dmp sac
   createdb sac-test
   pg_restore sac-test-20June2011.dmp | psql sac-test
   psql sac-test


Now run the following sequence of commands to flush all the data from the db
and keep only dictionaries etc.

**Note:** Be very careful not to run this on any live database!

```
delete from catalogue_radarproduct;
delete from catalogue_searchrecord;
delete from catalogue_orderstatushistory;
delete from catalogue_orderstatus;
delete from catalogue_taskingrequest;
delete from catalogue_order cascade;
delete from catalogue_orderstatus;
delete from catalogue_opticalproduct;
delete from catalogue_genericproduct;
delete from catalogue_taskingrequest;
delete from catalogue_searchrecord;
delete from catalogue_visit;
delete from catalogue_clip;
delete from catalogue_genericimageryproduct;
delete from catalogue_search_processing_level;
delete from catalogue_search_sensors;
delete from catalogue_searchdaterange;
delete from catalogue_search;
drop table heatmap_grid;
drop table heatmap_grid cascade;
delete from catalogue_sacuserprofile;
delete from userprofile_emailvalidation;
delete from catalogue_deliverydetail;
delete from catalogue_ordernotificationrecipients_sensors;
delete from catalogue_ordernotificationrecipients;
delete from userprofile_avatar;
delete from catalogue_ordernotificationrecipients;
delete from django_admin_log;
delete from auth_user where username != 'timlinux';
delete from catalogue_genericsensorproduct;
delete from catalogue_genericproduct;
drop table catalogue_clip;
drop table import.sumb;
drop table import.spot5;
drop table import.sacc;
drop table import.cbers;

vacuum analyze;

```

Next you should tweak your settings.py to point to sac-test and then do:

```
python manage.py syncdb

```


Now generate the fixtures like this:

```
mkdir catalogue/fixtures
python manage.py dumpdata catalogue --format=json --indent=4 > \
catalogue/fixtures/catalogue.json
`````````````````````````````````

Finally throw away your temporary database and reinstate your settings.py to use the
normal production database.

```````````````
dropdb sac-test
```````````````

Selenium setup
--------------

Selenium is used for automating web applications and testing using standard
internet browsers.

To execute Selenium test on a virtualized server, that has no display support
we need to prepare our virtualized server. Basically we can execute in in two
ways:

#. by forwarding X11 server connections through SSH connection
#. running it in a headless mode (uses Xvfb X server)

````````````````````
System prerequisites
````````````````````

To enable X11 forwarding we need to install ``xauth`` package:

    apt-get install xauth

To enable running selenium in a headless mode we need to install ``xvfb``
package::

    apt-get install xvfb

We also need to install a web browser, in this case Firefox, however, at the
time of writing (7th Dec. 2012) latest Selenium version is 2.26 which doesn't
work well with latest Firefox (ver. 17). So we need to install Firefox 16
manually by downloading binary archive from Mozilla ftp site, i.e.::

    wget https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/16.0.2/linux-x86_64/en-GB/firefox-16.0.2.tar.bz2

Then we need to manually unpack, install and symlink it::

    tar jxf firefox-16.0.2.tar.bz2
    mv firefox /opt/
    ln -s /opt/firefox/firefox /usr/bin/firefox

This will enable Selenium web driver to execute correct Firefox version.

After installing Firefox 16.0.2, we need to *DISABLE* automatic Firefox
updates, Edit -> Preferences -> Advanced -> Update and then select *Never
check for updates*.

``````````````````````````````
Installing Selenium Web Driver
``````````````````````````````

In an activated Python virtual environment install Selenium Web Driver::

    pip install selenium==2.26.0


````````````````````````
Executing Selenium tests
````````````````````````

Executing Selenium tests requires a XServer. We can either, export(forward)
local XServer using SSH, or start Xvfb on virtualized server.

Xvfb disadvantage is it's *hidden* view, so it's hard to debug/write tests,
but it's faster. On the other hand forwarding X11 will show browser which
speeds up debugging/writing tests, but it's slower. We can actually use both,
we just need to set correct ``DISPLAY`` environment variable, i.e.::

    # run on forwarded X11 Server
    DISPLAY=:10 python manage.py test  catalogue.tests
    # run on local Xvfb Server
    DISPLAY=:99 python manage.py test  catalogue.tests


Forwarding X11
^^^^^^^^^^^^^^

Connect to local virtualized server using SSH, i.e ::

    ssh -Y sac-live.local

.. note:: -Y enables X11 forwarding

Check if ``DISPLAY`` environment variable is set (``echo $DISPLAY``), continue
as normal, initializing Python virtual environment and executing tests.


Running locally on Xvfb
^^^^^^^^^^^^^^^^^^^^^^^

Before running any tests, we need to start local ``xvfb`` XServer and set
``DISPLAY`` environment variable::

    Xvfb -ac :99 > /dev/null 2>&1 &
    export DISPLAY=:99

After we can continue as normal, initializing Python virtual environment and
executing tests.


Running unit tests
------------------

Running Unit tests using Postgresql
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively you can use postgresql as the test database backend. Before you
can run the tests you should create a template database and set some
permissions on it:

```
createdb template_postgis
psql template_postgis
GRANT ALL ON geometry_columns TO PUBLIC;
GRANT ALL ON spatial_ref_sys TO PUBLIC;
\q
``

Now you can run the tests without the settings_test option and they will be
executed against an autogenerated PostgreSQL database backend.

```````````````````````````````
python manage.py test catalogue
```````````````````````````````
