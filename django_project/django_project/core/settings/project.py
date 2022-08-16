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
        'CONN_MAX_AGE': 0
    },
}

# Application specific apps
INSTALLED_APPS += (
    'catalogue',
    'dictionaries',
    'useraccounts',
    'search',
    'orders',
    'pycsw_integration',
    'reports',
)

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

# External site URL, used in KML data generation and elsewhere
# No terminating slash
EXTERNAL_SITE_URL = 'http://catalogue.sansa.org.za'

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
GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'
GEOIP_CITY = 'GeoLite2-City.mmdb'

# this is the public domain name or IP address of this django instance.
# get ip address logic provided in utils.py
# HOST = get_ip_address('eth1')
HOST = '192.168.1.1'

# used in various places including kml generator
DOMAIN = 'catalogue.sansa.org.za'

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
# MIDDLEWARE += (
#     'catalogue.middleware.stripwhitespace'
#    '.StripWhitespaceMiddleware',
# )

CATALOGUE_ISO_METADATA_XML_TEMPLATE = abspath(join('..', (
    'resources/PackageTemplate/Metadata/'
    'ISOMetadata/ISOMetadata_template.xml')))

# limit the number of returned metadata records
MAX_METADATA_RECORDS = 500

# number of search results per page
RESULTS_NUMBER = 50

# For ingesting MISR data
MISR_ROOT = ''

# These are optional - only set if you have wierd issues like DataSource
# unknown
# GEOS_LIBRARY_PATH='/usr/lib/libgeos_c.so.1'
# GEOIP_LIBRARY_PATH='/usr/lib/libGeoIP.so.1'
# GDAL_LIBRARY_PATH='/usr/local/lib/libgdal.so'

PIPELINE = {
    'STYLESHEETS': {
        'catalogue': {
            'source_filenames': (
                'css/map.css',
                'js/libs/bootstrap-5.0.2/css/bootstrap.css',
                'bootstrap/css/bootstrap/responsive.css',
                'css/font-awesome/font-awesome.css',
                'datepicker/css/datepicker.css',
                'css/base.css',
                'js/libs/openlayers-6.5.0/ol.css',
            ),
            'output_filename': 'css/catalogue.css',
            'extra_context': {
                'media': 'screen, projection',
            },
        },
    },
    'JAVASCRIPT': {

    }
}

# userena settings
USERENA_SIGNIN_REDIRECT_URL = '/search/'

from .celery_setting import *  # noqa
