from .test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac-master',
        'USER': 'jenkins',
        'PASSWORD': 'jenkins-test',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    }
}

INSTALLED_APPS += (
    'django_jenkins',  # don't remove this comma
)

# exclude files/folders, wildcards accepted

COVERAGE_EXCLUDES_FOLDERS = [
    '*settings/*',
    '*tests*'
]

NOSE_ARGS = [
    'catalogue',
    'dictionaries',
    'useraccounts',
    'search',
    'dictionaries',
]

#
# For django-jenkins integration
#
PROJECT_APPS = (
    'catalogue',
    'dictionaries',
    'useraccounts',
    'search',
)

PYLINT_RCFILE = 'pylintrc'

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
    # 'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    # Needs rhino or nodejs
    #'django_jenkins.tasks.run_jslint',
    #'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_sloccount',
)

# added nose_test_runner for jenkins
# this feature is currently in git master
# commit 2f241bb6b7a111172f1e5bd26a1d21815f83d1e7
JENKINS_TEST_RUNNER = 'django_jenkins.nose_runner.CINoseTestSuiteRunner'
