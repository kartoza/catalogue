from .project import *

SENTRY_DSN = ('http://a63c799050b94d72aae177153df32f46:998d4e6fe9a643a5bf270d8c65831216@sentry.linfiniti.com/9')

MIDDLEWARE_CLASSES = (
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.middleware.SentryLogMiddleware',
) + MIDDLEWARE_CLASSES

#
# Sentry settings - logs exceptions to a database
# see http://sentry.sansa.org.za/account/projects/catalogue-live/docs/django/
LOGGING = {
    # internal dictConfig version - DON'T CHANGE
    'version': 1,
    'disable_existing_loggers': True,
    # default root logger - handle with sentry
    'root': {
        'level': 'DEBUG',
        'handlers': ['sentry'],
    },
    'formatters': {
        # define output formats
        'verbose': {
            'format': (
                '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        # send email to mail_admins, if DEBUG=False
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # sentry logger
        'sentry': {
            'level': 'WARNING',  # use LOG_LEVEL from settings_local
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        # console output, useful for debugging
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
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
        },
        'pycsw': {
            'handlers': ['sentry'],
            'level': 'ERROR',
            'propagate': False
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
PIPELINE_YUGLIFY_BINARY = '/usr/local/bin/yuglify'

