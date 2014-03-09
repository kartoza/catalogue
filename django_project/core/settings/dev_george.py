from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'catalogue2',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    },
}

POSTGIS_VERSION = (2, 0)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# set up devserver if installed
try:
    import devserver
    INSTALLED_APPS += (
        'devserver',
    )
except ImportError:
    pass

# These are optional - only set if you have wierd issues like DataSource
# unknown
#GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'
#GDAL_LIBRARY_PATH = '/usr/lib/libgdal1.7.0.so.1'

PIPELINE_YUGLIFY_BINARY = ABS_PATH('node_modules', 'yuglify', 'bin', 'yuglify')
