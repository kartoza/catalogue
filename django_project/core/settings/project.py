from .contrib import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'catalogue',
        'USER': 'catalogue',
        'PASSWORD': 'catalogue',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    },
}

# Application specific apps
INSTALLED_APPS += (
    'catalogue',
    'dictionaries',
    'useraccounts',
    'search',
    'pycsw_integration',
    'reports'
)

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

# External site URL, used in KML data generation and elsewhere
# No terminating slash
EXTERNAL_SITE_URL = 'http://catalogue.localhost'


# Url that holds directories of thumbnails...
THUMBS_ROOT = ABS_PATH('thumbs_out')

# And this is the dir that holds imagery
IMAGERY_ROOT = ABS_PATH('imagery_mastercopies')

# The public visible url that imagery should be
# accessed from (include trailing /)
IMAGERY_URL_ROOT = EXTERNAL_SITE_URL + '/imagery/'


# Set to false if you want jquery to be loaded
# on clients from google mirrors rather
LOCAL_JQUERY = True

# Set to false to temporarily disable ip lat long logging - useful for then sac
# internet connection is in super tortoise mode
USE_GEOIP = True

# This is the path to MaxMinds Datasets, can be relative or absolute
GEOIP_PATH = ABS_PATH('core', 'geoip_data')
# Hack to make geoip work on OSX
# See https://code.djangoproject.com/ticket/19168
GEOIP_COUNTRY = 'GeoIP.dat'
GEOIP_CITY = 'GeoLiteCity.dat'

# this is the public domain name or IP address of this django instance.
# get ip address logic provided in utils.py
#HOST = get_ip_address('eth1')
HOST = '192.168.1.1'

# used in various places including kml generator
DOMAIN = 'catalogue.localhost'

# Standard page size for pagination
PAGE_SIZE = 20

WMS_SERVER = 'maps.sansa.org.za'

CART_LAYER = 'CART_TEST'

# This is for shapefile uploading using dane springmeyer's django-shapes lib
SHP_UPLOAD_DIR = '/tmp/'

# Set to true if you want staff members to receive email notification
# when orders are received and changed
EMAIL_NOTIFICATIONS_ENABLED = True

# extra middleware classes
MIDDLEWARE_CLASSES += (
    'catalogue.middleware.stripwhitespace'
    '.StripWhitespaceMiddleware',
)

CATALOGUE_ISO_METADATA_XML_TEMPLATE = ABS_PATH('..', (
    'resources/PackageTemplate/Metadata/'
    'ISOMetadata/ISOMetadata_template.xml'))

#limit the number of returned metadata records
MAX_METADATA_RECORDS = 500

# For ingesting MISR data
MISR_ROOT = ''

# These are optional - only set if you have wierd issues like DataSource
# unknown
#GEOS_LIBRARY_PATH='/usr/lib/libgeos_c.so.1'
#GEOIP_LIBRARY_PATH='/usr/lib/libGeoIP.so.1'
#GDAL_LIBRARY_PATH='/usr/local/lib/libgdal.so'

PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.10.1.min.js',
        ),
        'output_filename': 'js/contrib.js',
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/bootstrap.min.css',
            # 'css/bootstrap-responsive.min.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    }
}
