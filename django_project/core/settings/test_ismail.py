from .test import *
import platform

POSTGIS_VERSION=(2,1,2)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'catalogue',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': '172.17.0.2',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    }
}

# OSX - see readme in geoip data dir
if 'Darwin' in platform.platform():
    GEOIP_LIBRARY_PATH = '/opt/local/lib/libGeoIP.dylib'
