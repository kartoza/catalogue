# noinspection PyUnresolvedReferences
from .dev import *  # noqa
import os
print((os.environ))

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}

MEDIA_ROOT = '/home/web/media'
STATIC_ROOT = '/home/web/static'

# See docker-compose.yml file for postfix container definition
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp')
# Port for sending e-mail.
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 25))
# SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'noreply@kartoza.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'docker')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False').lower() in ['true', '1']
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '[sansa-catalogue]')
EMAIL_CUSTOMER_SUPPORT = os.getenv('EMAIL_CUSTOMER_SUPPORT', 'customers-eo@sansa.org.za')