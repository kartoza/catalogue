# coding=utf-8
"""
core.settings.contrib
"""
import os
from .base import *

# Extra installed apps
INSTALLED_APPS += (
    'offline_messages',
    'raven.contrib.django.raven_compat',
    'shapes',
    'django_extensions',
    'userena',
    'guardian',
    'easy_thumbnails',
    'crispy_forms',
    'webodt',
    'tastypie',
    'backbone_tastypie',
    'pipeline',
    'exchange',
    'django_tables2',
    'celery',
    # django rest
    'rest_framework',
    'rest_framework_gis',

)

# Added by George for webodt
WEBODT_CONVERTER = 'webodt.converters.abiword.AbiwordODFConverter'
WEBODT_ABIWORD_COMMAND = ['/usr/bin/abiword', '--plugin', 'AbiCommand']
WEBODT_TEMPLATE_PATH = ABS_PATH('reports', 'report-templates')
WEBODT_ODF_TEMPLATE_PREPROCESSORS = [
    'webodt.preprocessors.xmlfor_preprocessor',
    'webodt.preprocessors.unescape_templatetags_preprocessor',
]
WEBODT_DEFAULT_FORMAT = 'pdf'

# Added by Tim for registration app
ACCOUNT_ACTIVATION_DAYS = 2
# DEFAULT_FROM_EMAIL = 'noreply@catalogue.sansa.org.za'
DEFAULT_FROM_EMAIL = 'noreply@noreply.kartoza.com'
# define organisation acronym, used in filenaming schemes
ORGANISATION_ACRONYM = 'SANSA'

# USERENA settings

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_NAME = 'Anonymous'

AUTH_PROFILE_MODULE = 'useraccounts.SansaUserProfile'

# LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

# check https://django-userena.readthedocs.org/en/latest/settings.html
USERENA_MUGSHOT_GRAVATAR = False
USERENA_DEFAULT_PRIVACY = 'closed'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_USE_MESSAGES = False

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# add pipelinefinders to statistic_finders
STATICFILES_FINDERS += (
    'pipeline.finders.PipelineFinder',
)

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# we use some of the libraries which use global namespace (OL, Proj4JS, ...)
DISABLE_WRAPPER = True

# django-exchange openexchangerates API Key
OPENEXCHANGERATES_API_KEY = 'db63cb9bdc5f4199a9302fea8b173f41'

# used to sanitize sorting/column inputs to the executeRAWSQL commands in a
# number of table views
ACCEPTABLE_COLUMNS = [
    'country', 'count'
]

ACCEPTABLE_SORTS = [
    'ASC', 'DESC'
]

# MESSAGE_STORAGE = 'offline_messages.storage.OfflineStorageEngine'

BROKER_URL = 'amqp://guest:guest@%s:5672//' % os.environ['RABBITMQ_HOST']

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # project level templates
            absolute_path('core', 'templates'),
            absolute_path('catalogue', 'templates'),
            absolute_path('dictionaries', 'templates'),
            absolute_path('order', 'templates'),
            absolute_path('reports', 'templates'),
            absolute_path('search', 'templates'),
            absolute_path('shapes', 'templates'),
            absolute_path('useraccounts', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
# URL prefix for static files.
# Example: 'http://media.lawrence.com/static/'
STATIC_ROOT = '/home/web/static'

STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    absolute_path('core', 'base_static'),
    absolute_path('search', 'static'),
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}
