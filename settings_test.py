# This is an exception to our 'dont import globally' rule
from settings import *
import coverage

# See http://hustoknow.blogspot.com/2011/02/setting-up-django-nose-on-hudson.html
INSTALLED_APPS += ('django_nose', )  # don't remove this comma

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--cover-html', 
    '--cover-html-dir=xmlrunner/html', 
    '--cover-inclusive',
    '--cover-package=catalogue',
    '--nocapture', 
    '--nologcapture',
    '--testmatch=^test'
    '--with-coverage', 
]
JENKINS_NOSE_ARGS = (
    '--with-xunit', 
    '--xunit-file=xmlrunner/nosetests.xml', 
    '--with-xcoverage', 
    '--xcoverage-file=coverage.xml')
NOSE_ARGS += JENKINS_NOSE_ARGS

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# change this to a proper location
EMAIL_FILE_PATH = '/tmp/'

#COVERAGE_MODULE_EXCLUDES = [
#        'tests$', 
#        'settings$', 
#        '^urls$', 
#        'locale$',
#        '__init__', 
#        'django',
#        'migrations',
#    ]

#coverage.use_cache(False)
#for e in COVERAGE_MODULE_EXCLUDES:
#    coverage.exclude(e)
#coverage.start()
