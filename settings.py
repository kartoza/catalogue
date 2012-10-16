import os
import logging
from raven.conf import setup_logging
from raven.contrib.django.handlers import SentryHandler
# This is an exception to our 'dont import globally' rule
from settings_local import *

# See: http://www.djangobook.com/en/1.0/chapter12/#cn222
AUTH_PROFILE_MODULE = 'catalogue.SacUserProfile'

# Django settings for sac_catalogue project.

MANAGERS = ADMINS
DATABASES = {
        'default': {  # new db that does not mimic acs system
         'ENGINE': 'postgresql_psycopg2',
         'NAME': DBNAME,
         'USER': DBUSER,
         'PASSWORD': DBPASSWORD,
         'HOST': DBHOST,
         'PORT': DBPORT,
         'TEST_NAME': DBTEST,
         },
        'acs': {  # legacy acs port to django
         'ENGINE': 'postgresql_psycopg2',
         'NAME': ACSDBNAME,
         'USER': ACSDBUSER,
         'PASSWORD': ACSDBPASSWORD,
         'HOST': ACSDBHOST,
         'PORT': ACSDBPORT,
         }
        }
DATABASE_ROUTERS = ['catalogue.dbrouter.CatalogueRouter']

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = os.path.join(ROOT_PROJECT_FOLDER, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
STATIC_ROOT = os.path.join(ROOT_PROJECT_FOLDER, 'static')

# URL prefix for static files.
# Example: 'http://media.lawrence.com/static/'
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: 'http://foo.com/static/admin/', '/static/admin/'.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PROJECT_FOLDER, 'project_static_files'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c(x1$mngg*&#re1shf2r3(j&1&rl528_ubo2#x_)ljabk2*cly'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'catalogue.middleware.stripwhitespace.StripWhitespaceMiddleware',
)
MIDDLEWARE_CLASSES += EXTRA_MIDDLEWARE_CLASSES

TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PROJECT_FOLDER, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.gis',
    'offline_messages',
    'registration',
    'raven.contrib.django',  # for sentry logging
    'catalogue',
    #'acscatalogue',
    'shapes',
    'django_extensions',
    'userprofile',
)
INSTALLED_APPS += EXTRA_INSTALLED_APPS

#where to take the user after they logged in
LOGIN_REDIRECT_URL = '/'
#where to take the user if they try to access a page requiring a logged in user
LOGIN_URL = '/accounts/login/'

#for userprofile app
I18N_URLS = False
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'generic.jpg')
AVATAR_WEBSEARCH = False

#limit the number of returned metadata records
MAX_METADATA_RECORDS = 500

# South is currently disabled
SOUTH_MIGRATION_MODULES = {
  'acs': 'ignore',
}

# For offline messages app
MESSAGE_STORAGE = 'offline_messages.storage.OfflineStorageEngine'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--nologcapture',
    '--with-coverage',
    '--cover-package=catalogue',
    '--cover-inclusive',
]

#
# For django-jenkins integration
#
PROJECT_APPS = (
    'catalogue',
)
JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.django_tests',
    #'django_jenkins.tasks.run_pep8',
    # Needs rhino or nodejs
    #'django_jenkins.tasks.run_jslint',
    #'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_sloccount',
)

#
# Sentry settings - logs exceptions to a database
# see http://sentry.sansa.org.za/account/projects/catalogue-live/docs/django/

#logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(LOG_LEVEL)
setup_logging(SentryHandler())

