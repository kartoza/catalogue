"""Project level settings."""
from os.path import exists, dirname, join

from .project import *
try:
    from .secret import SENTRY_KEY
except ImportError:
    SENTRY_KEY = None

# Sentry config
if 'raven.contrib.django.raven_compat' in INSTALLED_APPS and SENTRY_KEY:
    # noinspection PyUnresolvedReferences
    import raven  # noqa

    # The .version file is made by the tag_and_deploy script
    version_file = join(dirname(dirname(dirname(__file__))), '.version')
    if exists(version_file):
        with open(version_file, 'r') as version:
            release = version.read()
    else:
        release = 'unknown'

    RAVEN_CONFIG = {
        'dsn': SENTRY_KEY,
        'release': release,
    }

    MIDDLEWARE_CLASSES = (
        # We recommend putting this as high in the chain as possible
        # see http://raven.readthedocs.org/en/latest/integrations/  ...
        # ... django.html#message-references
        # This will add a client unique id in messages
        'raven.contrib.django.raven_compat.middleware.'
        'SentryResponseErrorIdMiddleware',
    ) + MIDDLEWARE_CLASSES

    #
    # Sentry settings - logs exceptions to a database
    LOGGING = {
        # internal dictConfig version - DON'T CHANGE
        'version': 1,
        'disable_existing_loggers': True,
        # default root logger - handle with sentry
        'root': {
            'level': 'ERROR',
            'handlers': ['sentry'],
        },
        'handlers': {
            # send email to mail_admins, if DEBUG=False
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            # sentry logger
            'sentry': {
                'level': 'WARNING',
                'class': (
                    'raven.contrib.django.raven_compat.'
                    'handlers.SentryHandler'),
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['sentry'],
                'propagate': False
            },
            'raven': {
                'level': 'ERROR',
                'handlers': ['mail_admins'],
                'propagate': False
            },
            'sentry.errors': {
                'level': 'ERROR',
                'handlers': ['mail_admins'],
                'propagate': False
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True
            }
        }
    }
# django 1.5 ALLOWED_HOSTS - protects against host-poisoning attacks
# change to the real service name
# https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-ALLOWED_HOSTS
# ALLOWED_HOSTS = ['41.74.158.4', 'test.catalogue.sansa.org.za']
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'catalogue',
        'USER': 'catalogue',
        'PASSWORD': 'catalogue',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST_NAME': 'sac_dev_unittest_master',
    }
}

#PIPELINE_YUGLIFY_BINARY = ABS_PATH('node_modules', 'yuglify', 'bin', 'yuglify')
PIPELINE_ENABLED = True
PIPELINE_YUGLIFY_BINARY = '/usr/local/bin/yuglify'
PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.yuglify.YuglifyCompressor'
# Pipeline - for production we want to compress resources

