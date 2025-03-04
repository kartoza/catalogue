from .project import *

LOGGING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

# Logs exceptions to a database
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Console output for debugging
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # Log errors to a file
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'django_errors.log'),
            'formatter': 'verbose',
        },
        # Email admins on critical errors
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # Sentry error tracking
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'raven': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'sentry.errors': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
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

