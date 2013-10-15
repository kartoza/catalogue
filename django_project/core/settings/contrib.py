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
)

# Added by George for webodt
WEBODT_CONVERTER = 'webodt.converters.openoffice.OpenOfficeODFConverter'
WEBODT_TEMPLATE_PATH = '/home/web/catalogue/django_project/reports/report-templates/'
WEBODT_ODF_TEMPLATE_PREPROCESSORS = [
    'webodt.preprocessors.xmlfor_preprocessor',
    'webodt.preprocessors.unescape_templatetags_preprocessor',
]
WEBODT_OPENOFFICE_SERVER = ('127.0.0.1', 2002)
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
