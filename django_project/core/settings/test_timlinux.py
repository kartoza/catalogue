from .test import *
import platform

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'catalogue',
        'USER': 'timlinux',
        'PASSWORD': 'pumpkin',
        'HOST': '192.168.2.158',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    }
}

# OSX - see readme in geoip data dir
if 'Darwin' in platform.platform():
    GEOIP_LIBRARY_PATH = '/opt/local/lib/libGeoIP.dylib'
