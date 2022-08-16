Webmapping
------------------------------------------

A key part of the system is the provision of web mapping services. These form
the backdrops for search and visualisation maps and play various other roles
within the system. Although it is not advertised to clients, the web maps can
be consumed with any OGC-WMS compatible client via a number of public wms urls.

GDAL Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GDAL provides read and write capabilities for numerous GIS formats. We are going 
to had build GDAL so that we have MrSid and ECW support, as well as support for 
various other data formats.

Checkout the source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We need to make sure subversion is installed first::

   sudo apt-get install subversion

Make a work directory for building gdal in::

  cd
  mkdir -p dev/cpp
  cd dev/cpp
  svn co https://svn.osgeo.org/gdal/trunk/gdal gdal-svn
  cd gdal-svn


Hdf4 and Hdf5 support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do this::

  sudo apt-get install libhdf5-serial-dev libhdf5-serial-1.6.6-0 libhdf4g-dev \
  libhdf4g libhdf4g-doc

Building with ECW Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Note:** you can only compress images up to 500mb unless you have an erdas licesne
(though as far as I know there is no limit to decompression size).

Install dependencies::

  sudo apt-get install build-essential libjpeg62-dev libtiff4-dev

Go to the erdas ecw sdk web page::
  
  http://www.erdas.com/Products/ERDASProductInformation/tabid/84/CurrentID/1142/Default.aspx

(or just search their site for 'ecw sdk')

Get the ECW JPEG2000 Codec SDK Source Code (second item listed - first if win version)

After the download you should have::

   ecw_jpeg_2000_sdk_3_3_source.zip

Now unzip it::

  cd /tmp
  unzip ecw_jpeg_2000_sdk_3_3_source.zip
  unzip ImageCompressionSDKSourceCode3.3Setup_20070509.zip
  sudo mv libecwj2-3.3 /usr/local/src/
  cd /usr/local/src/
  sudo chown -R timlinux libecwj2-3.3/
  cd libecwj2-3.3

Now build the ecw lib::

  ./configure
  make
  sudo make install


Next gdal must be (re)built with the ecw flag:

**Note:** You can skip this step if you are going on to add MrSid support below too.


**Note:** If you want the gdal python bindings installed into your django
python virtual env, first do and ensure you have python setup tools on your
venv::

  source /opt/sac_catalogue/python

or similar before running the build procedure below. The bindings will then go
into your python env rather than into the global python dir::

  cd <gdal src>
  make clean
  export CXXFLAGS=-fPIC
  ./configure --with-libtiff=internal \
              --with-geotiff=internal \
              --with-ecw=/usr/local \
              --with-python \
              --with-jpeg=internal \
              --with-jpeg12 \
              --without-libtool
  make -j8
  sudo make install            

Jpeg internal and jpeg 12 needed for jpeg12 tif compression support::

See also http://trac.osgeo.org/gdal/wiki/ECW

We configure gdal to build with its own internal copy of libtiff otherwise we 
encounter problems with assertion errors if the system tiff lib is not compatible.
(see http://trac.osgeo.org/gdal/ticket/3139 for more details).

Gdal MrSid Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to first create a user account on the LizardTech website and then get
this download (don't worry about the Redhat Enterprise mentioned on the
download page, it will work on Ubuntu server too).

http://www.lizardtech.com/developer/members/download.php?dl=Unified_DSDK_8.0_linux.x86-64.gcc41.tgz

Extract the downloaded SDK to /usr/local

To add mr sid support, you need the MrSid geosdk and then to reconfigure and
build gdal like this (adjust the Geo_DSDK directory name as needed to match
where you extracted it to)::

  cd <gdal src>
  make clean
  export CXXFLAGS=-fPIC
  ./configure --with-libtiff=internal \
              --with-geotiff=internal \
              --with-ecw=/usr/local \
              --with-python \
              --with-mrsid=/usr/local/Geo_DSDK-7.0.0.2167/ \
              --without-jp2mrs \
              --with-jpeg=internal \
              --with-jpeg12 \
              --without-libtool
  make -j8
  sudo make install            

Jpeg internal and jpeg 12 needed for jpeg12 tif compression support

**Note:** If you want the gdal python bindings installed into your django
python virtual env, first do::

  source /opt/sac_catalogue/python

or similar before running the build procedure above. The bindings will then go
into your python env rather than into the global python dir. With the above you
should see something like this in the output from configure for gdal::

  checking for python bindings... checking for python... python
  checking for location of Python Makefiles... found
  checking where to install Python modules... /opt/sac_catalogue/python/lib64/python2.7/site-packages
  enabled
  checking for python setuptools... found

Mapserver Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First of all you need to compile mapserver from source since we need 
ecw and MrSid support. We will link it to our hand built GDAL::

   sudo apt-get build-dep cgi-mapserver libxslt1-dev libpam-dev libreadline-dev

Now fetch and install mapserver::

  cd dev/cpp/
  wget http://download.osgeo.org/mapserver/mapserver-5.6.5.tar.gz
  tar xfz mapserver-5.6.5.tar.gz
  cd mapserver-5.6.5/
  export LD_LIBRARY_PATH=/usr/local/lib/

Now build agg::

  cd agg-2.4/
  ./configure
  make -j8
  sudo make install

Now compile mapserver::

  cd ..
  ./configure \
      --prefix=/usr \
      --enable-debug \
      --without-tiff \
      --without-pdf \
      --with-gd=/usr \
      --with-freetype=/usr \
      --with-zlib=/usr \
      --with-png=/usr \
      --with-xpm=/usr \
      --with-jpeg=/usr \
      --with-gdal=/usr/local/bin/gdal-config \
      --with-ogr \
      --with-proj \
      --with-eppl \
      --with-postgis \
      --with-wcs \
      --with-wms \
      --with-wmsclient \
      --with-wfs \
      --with-wfsclient \
      --with-threads \
      --with-geos \
      --with-fastcgi \
      --with-agg=/usr/local
  apt-get remove cgi-mapserver
  make -j8
  sudo cp mapserv /usr/lib/cgi-bin/

Once it is built you can check if everything is ok by doing::

/usr/lib/cgi-bin/mapserv -v

Which should give out something like::

  MapServer version 5.0.3 OUTPUT=GIF OUTPUT=PNG OUTPUT=JPEG OUTPUT=WBMP
  OUTPUT=SVG SUPPORTS=PROJ SUPPORTS=AGG SUPPORTS=FREETYPE SUPPORTS=WMS_SERVER
  SUPPORTS=WMS_CLIENT SUPPORTS=WFS_SERVER SUPPORTS=WFS_CLIENT SUPPORTS=WCS_SERVER
  SUPPORTS=FASTCGI SUPPORTS=THREADS SUPPORTS=GEOS INPUT=EPPL7 INPUT=POSTGIS
  INPUT=OGR INPUT=GDAL INPUT=SHAPEFILE

Ensure that after doing the above, your mapserver install supports fastcgi::

  SUPPORTS=FASTCGI

Set up the web mapping dir
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The web mapping dir contains mapserver configuration files and resources. It
should be checked out of GIT first. You should make sure you have needed 
permissions for checking the repo out into /opt::
  
  cd /opt
  git clone git@orasac1:sansa_webmapping.git webmapping


After checkout of the webmapping GIT project, you should create a symlink to 
the data directory::
  
  cd webmapping
  ln -s /mnt/cataloguestorage2/gisdata/ data

Apache configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do this::
  
  sudo apt-get install libapache2-mod-fcgid

Add these map file paths to your /etc/apache2/sites-enabled/default file::
  
  Include /opt/webmapping/apache-include/mapserver.conf

Mapserver database connection details encrytion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To allow storing mapfiles with database connection details in git, they should
be hashed using the [documented msencrypt utility
http://mapserver.org/utilities/msencrypt.html]::

  /home/timlinux/mapserver-5.4.2/msencrypt -keygen mapserver-key.txt
  /home/timlinux/mapserver-5.4.2/msencrypt -key mapserver-key.txt "fooo"

Foo being the username and password for the databse connection. This produces
output like this::

688477225F5ABDFA

Then in the mapfile replace all usernames and passwords with hashes and freely
commit the mapfiles to git.

At the top of each mapfile just after the MAP clause add a line like this::

   CONFIG "MS_ENCRYPTION_KEY" "/opt/webmapping/mapfiles/mapserver-key.txt"

And for the connection string to the database use this format::

   CONNECTION "user={688477225F5ABDFA} password={688477225F5ABDFA} dbname=sac host=localhost"

Adding a new backdrop layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this section we will use the new 2010 ZA SPOT5 Mosaic as an example of how
to deploy a new backdrop layer into the WMS environment.

Synchronising the data to the catalogue server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first task it to place the data onto the catalogue server (in our case
LION). The data could be copied over by various means. In the SAC context it
will typically come from the CXFS file store:

on cheetah::

  cd /cxfs/archive/production/Spot5_Mosaic_Packaging_2010/Imagery/Latlong/TLTIF
  dmfind . -state MIG -o -state OFL | dmget
  rsync -ave ssh *.gz lion:/mnt/cataloguestorage2/gisdata/za/SPOT5_2010/tif-gz/
  dmput *

The second command above instructs to retrieve all migrated files from tape,
which is needed before the data can be synced over to LION via rsync over ssh.

The last command instructs dmf to push the files back down to tape again when 
we are done.

Batch conversion to ecw
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To covert the mosaic tiles in batch we use a simple script like this (called tif2ecw)::

  #!/bin/bash
  mkdir ecw
  EXT=tif
  for FILE in tif/*.${EXT}
  do
    BASENAME=$(basename $FILE .${EXT})
    OUTFILE=ecw/${BASENAME}.ecw
    LOCKFILE=${BASENAME}.lock
    echo "Processing: ${BASENAME}.${EXT}"
    if [ -f $LOCKFILE ] || [ -f $OUTFILE ] #skip if exists
    then
      echo "Skipping: $OUTFILE"
    else
      /usr/local/bin/gdal_translate -of ECW -co LARGE_OK=YES $FILE $OUTFILE
      rm $LOCKFILE
    fi
  done

Note the above script requires that you have an appropriate ERDAS license so
that you can compress large files (although it is not enforced anywhere).

So assuming our data exist in ''/mnt/cataloguestorage2/gisdata/za/SPOT5_2010/tif-gz/'' and
we run the script from ''/mnt/cataloguestorage2/gisdata/za/SPOT5_2010/'', the result will 
be a new directory: ''/mnt/cataloguestorage2/gisdata/za/SPOT5_2010/ecw'' containing the 
mosaic tiles in ecw format.

Creation of a virtual raster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gdal has a concept called \\virtual rasters\\ (roughly analagous to ESRI image
catalogues I believe) that presents multiple images as a single file resource.

We will create a virtual raster for the mosaic so that we can simply add a single 
layer to our mapfile configuration::

  cd ecw
  gdalbuildvrt za2010ecw.vrt *.ecw

Creation of a new mapfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each new backdrop layer has a new mapfile created for it. The mapfiles are 
stored in the GIT repository with passwords and usernames tokenised.
When checked out, mapfiles are placed in the webmapping directory under::

   /opt/webmapping/mapfiles



The structure of this directory looks like this::

  webmapping/
  +-- apache-include
  |   +-- README
  |   \-- mapserver.conf
  +-- config
  |   +-- 000-default
  |   +-- default
  |   \-- tilecache.cfg
  +-- data -> /mnt/cataloguestorage/data/
  +-- fonts
  |   +-- arialbd.ttf
  |   +-- arialbi.ttf
  |   +-- ariali.ttf
  |   +-- arial.ttf
  |   +-- ariblk.ttf
  |   +-- courbd.ttf
  |   +-- courbi.ttf
  |   +-- couri.ttf
  |   +-- cour.ttf
  |   +-- fonts.list
  |   \-- symbols.ttf
  +-- mapfiles
  |   +-- geonames.map
  |   +-- cart.map
  |   +-- debug.include
  |   +-- jpl.include
  |   +-- landsat7-global-mosaic.map
  |   +-- pg.map
  |   +-- searches.map
  |   +-- vector_layers.map.include
  |   +-- visitors.map
  |   +-- world.map
  |   +-- za.map
  |   +-- za_nbi.map
  |   +-- za_vector.map
  |   +-- za_vector_spot2007_10m_ecw.map
  |   +-- za_vector_spot2007_2_5m_ecw.map
  |   +-- za_vector_spot2008_10m_ecw.map
  |   +-- za_vector_spot2008_2_5m_ecw.map
  |   +-- za_vector_spot2009_10m_ecw.map
  |   +-- za_vector_spot2009_2_5m_ecw.map
  |   +-- za_vector_spot2010_2_5m_tif.map
  |   \-- za_vector_test.map
  +-- scripts
  |   \-- reseed.sh
  +-- symbols
  |   +-- flaeche1_1.png
  |   +-- flaeche1.png
  |   +-- flaeche2_1.png
  |   +-- flaeche2.png
  |   +-- flaeche3.png
  |   +-- schraffur.png
  |   +-- stern.png
  |   +-- symbols.sym
  |   \-- welle.png
  \-- templates
      +-- search_footer.html
      +-- search_header.html
      +-- search.html
      \-- search.txt

So under ''/opt/webmapping/mapfiles'' we simply copy the mapfile definition
from a previous year. Of course depending on what you are trying to achieve,
you could create a totally new map file in this case too.

``cp za_vector_spot2009_2_5m_ecw.map za_vector_spot2010_2_5m_ecw.map``

For clarity it is suggested to stick to a standardised naming convention.

Now the map file needs to be edited and the relevant part for the mosaic layer
specified.::

  #
  # Notes:
  # 
  # Tim Sutton 2009
  #
  # By using status default for all layers, mapserver will render them 
  # all based on their scale dependent ranges when open layers 
  # makes a request. This is a good thing since It will allow us 
  # to create complex maps without having to add many layer definitions to 
  # OpenLayers.
  #

  MAP
    NAME "SouthAfricaSPOT5Mosaic2010_2.5m"
    # Map image size
    SIZE 400 400
    UNITS dd

    #EXTENT 28.156069 -25.890870 28.169983 -25.879721
    EXTENT -180 -90 180 90
    PROJECTION
      "init=epsg:4326"
    END

    SYMBOLSET "../symbols/symbols.sym"
    FONTSET "../fonts/fonts.list"
    # Background color for the map canvas -- change as desired
    IMAGECOLOR 192 192 192
    IMAGEQUALITY 95
    # Background color for the map canvas -- change as desired
    IMAGECOLOR -1 -1 -1
    IMAGEQUALITY 95
    
    INCLUDE "debug.include"

    #IMAGETYPE png24
    #OUTPUTFORMAT
    #  # use the new rendering backend from MapServer 5
    #  NAME 'AGGA'
    #  DRIVER AGG/PNG
    #  IMAGEMODE RGBA
    #END

    #OUTPUTFORMAT
    #  NAME png 
    #  DRIVER 'GD/PNG'
    #  MIMETYPE 'image/png'
    #  IMAGEMODE PC256
    #  EXTENSION 'png'
    #END

    IMAGETYPE jpeg
    OUTPUTFORMAT
      # use the new rendering backend from MapServer 5
      NAME 'AGG_JPEG'
      DRIVER AGG/JPEG
      IMAGEMODE RGB
    END

    # Legend
    LEGEND
        IMAGECOLOR 255 255 255
      STATUS OFF
      KEYSIZE 18 12
      LABEL
        TYPE BITMAP
        SIZE MEDIUM
        COLOR 0 0 89
      END
    END

    # Web interface definition. Only the template parameter
    # is required to display a map. See MapServer documentation
    WEB
      # Set IMAGEPATH to the path where MapServer should
      # write its output.
      IMAGEPATH '/tmp/'

      # Set IMAGEURL to the url that points to IMAGEPATH
      # as defined in your web server configuration
      IMAGEURL '/tmp/'

      # WMS server settings
      METADATA
        'wms_title'           'South Africa SPOT 5 Mosaic 2010 2.5m'
        'wms_onlineresource'  'http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT2010&'
        'wms_srs'             'EPSG:4326 EPSG:900913'
      END

      #Scale range at which web interface will operate
      # Template and header/footer settings
      # Only the template parameter is required to display a map. See MapServer documentation
    END

    LAYER
      NAME 'BlueMarble'
      TYPE RASTER
      DATA '/opt/webmapping/data/world/bluemarble/rectifywesternhemisphere.tif'
      METADATA
        'wms_title' 'WesternHemisphere'
        'wms_srs'             'EPSG:4326'
      END
      STATUS DEFAULT
      TRANSPARENCY 100
      PROJECTION
      'proj=longlat'
      'ellps=WGS84'
      'datum=WGS84'
      'no_defs'
      ''
      END
    END

    LAYER
      NAME 'BlueMarble'
      TYPE RASTER
      DATA '/opt/webmapping/data/world/bluemarble/rectifyeasternhemisphere.tif'
      METADATA
        'wms_title' 'EasternHemisphere'
        'wms_srs'             'EPSG:4326'
      END
      STATUS DEFAULT
      TRANSPARENCY 100
      PROJECTION
      'proj=longlat'
      'ellps=WGS84'
      'datum=WGS84'
      'no_defs'
      ''
      END
    END

    LAYER
      NAME "Jpl"
      TYPE RASTER
      CONNECTION "http://wms.jpl.nasa.gov/wms.cgi?"
      CONNECTIONTYPE WMS
      METADATA
        "wms_srs"             "EPSG:4326"
        "wms_name"            "global_mosaic_base" #comma separated list of layer names
        "wms_server_version"  "1.1.1"
        "wms_format"          "image/png"
        #"wms_auth_username" "username"
        #"wms_auth_password" "password"
        "wms_bgcolor" "0xFFFFFF"
      END
    END

    LAYER
      NAME 'Spot5_RSA_2009_2_5m'
      TYPE RASTER
      DATA '/opt/webmapping/data/za/SPOT5_2010/ecw/za2010ecw.vrt'
      METADATA
        'wms_title' 'Spot5_RSA_2010_2_5m'
        'wms_srs'             'EPSG:4326'
      END
      STATUS DEFAULT
      TRANSPARENCY 100
      OFFSITE 0 0 0 #transparent pixels
      MAXSCALEDENOM 1000000
      MINSCALEDENOM 0
      PROJECTION
      'proj=longlat'
      'ellps=WGS84'
      'datum=WGS84'
      'no_defs'
      ''
      END
    END

    INCLUDE 'vector_layers.map.include'
  END

This file should be committed in GIT under ``webmapping/mapfiles`` in the GIT repo.

**Note:** A detailed description of the above file is beyond the scope of this
document - please see the UMN Mapserver project for full documentation.

Deploy under apache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To deploy your web mapping project, you need to do two things:

+ Add an entry to mapserver.conf
+ Reload apache
+

To add a new entry to mapserver.conf, edit ''apache-include/mapserver.conf'' and add a
new line e.g.::
  
  SetEnv ZA_SPOT2010 "/opt/webmapping/mapfiles/za_vector_spot2010_2_5m_ecw.map"

Then test the configuration and reload::

   sudo apache2ctl -t

If it reports ok then reload::

  sudo /etc/init.d/apache2 reload

Testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can test using a WMS client (QGIS!) by adding a new connection to the url e.g.::

   http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT2010



Available end points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can connect to the various end points / map services using the following urls::

  http://196.35.94.243/cgi-bin/mapserv?map=ZA_VECTOR
  http://196.35.94.243/cgi-bin/mapserv?map=GEONAMES
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_VECTOR_TEST
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT2007
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT2008
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT2009
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT2010
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT10m2007
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT10m2008
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT10m2009
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_SPOT10m2010
  http://196.35.94.243/cgi-bin/mapserv?map=L7_MOSAIC
  http://196.35.94.243/cgi-bin/mapserv?map=ZA_NBI
  http://196.35.94.243/cgi-bin/mapserv?map=WORLD
  http://196.35.94.243/cgi-bin/mapserv?map=SEARCHES
  http://196.35.94.243/cgi-bin/mapserv?map=CART
  http://196.35.94.243/cgi-bin/mapserv?map=VISITORS

Please exercise discretion as to which of these you make publicly available -
there is currently no access control and not all of these datasets may be made
available to the general public.

Please note these end points will change when the server is moved into the DMZ.


Issue Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is an issue tracker for web mapping related issues here:

```http://196.35.94.196/projects/sansa-webmapping```


