from .base import *

# Extra installed apps
INSTALLED_APPS += (
    'offline_messages',
    'raven.contrib.django',
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
    'django_tables2'
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
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'noreply@catalogue.sansa.org.za'
#define organisation acronym, used in filenaming schemes
ORGANISATION_ACRONYM = 'SANSA'

# USERENA settings

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'useraccounts.SansaUserProfile'

#LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
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

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# we use some of the libraries which use global namespace (OL, Proj4JS, ...)
PIPELINE_DISABLE_WRAPPER = True

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