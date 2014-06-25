from .test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'catalogue2',
        'USER': 'george',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    },
}

POSTGIS_VERSION = (2, 1, 1)