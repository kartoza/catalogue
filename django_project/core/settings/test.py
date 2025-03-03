from .project import *

# http://hustoknow.blogspot.com/2011/02/setting-up-django-nose-on-hudson.html
INSTALLED_APPS += (
    'django_nose',  # don't remove this comma
)


TEST_RUNNER = 'django.test.runner.DiscoverRunner'

NOSE_ARGS = (
    '--with-coverage',
    '--cover-erase',
    '--cover-html',
    '--cover-html-dir=xmlrunner/html',
    '--cover-inclusive',
    # '--cover-package=catalogue',
    # '--cover-package=useraccounts',
    # '--cover-package=search',
    # '--cover-package=dictionaries',
    # '--cover-package=reports',
    # '--cover-package=orders',
    '--nocapture',
    '--nologcapture',
    #  default test settings don't include any specific tests (see jenkins.py)
)

# change this to a proper location
EMAIL_FILE_PATH = '/tmp/'


LOGGING = {
    # internal dictConfig version - DON'T CHANGE
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'nullhandler': {
            'class': 'logging.NullHandler',
        },
    },
    # default root logger
    'root': {
        'level': 'DEBUG',
        'handlers': ['nullhandler'],
    }
}

# force abiword PDF converter for tests
WEBODT_CONVERTER = 'webodt.converters.abiword.AbiwordODFConverter'

# don't use GEOIP for tests
USE_GEOIP = False
