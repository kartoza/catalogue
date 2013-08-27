from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac_dev_dodobas',
        'USER': 'dodobas',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
        'TEST_NAME': 'sac_dev_unittest_master',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # define output formats
        'verbose': {
            'format': (
                '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': (
                '%(name)s %(levelname)s %(filename)s L%(lineno)s: '
                '%(message)s')
        },
    },
    'handlers': {
        # console output, useful for debugging
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': '/tmp/sansa-dev.log',
            'formatter': 'simple',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'pycsw': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',  # switch to DEBUG to show actual SQL
        },
        'search': {
            'level': 'ERROR',
            'handlers': ['logfile'],
            # propagate is True by default, which proppagates logs upstream
            'propagate': False
        },
        'search.forms': {
            'level': 'DEBUG',
            'handlers': ['logfile'],
            # propagate is True by default, which proppagates logs upstream
            'propagate': False
        },
        'search.searcher': {
            'level': 'DEBUG',
            'handlers': ['logfile'],
            # propagate is True by default, which proppagates logs upstream
            'propagate': False
        },
    },
    # root logger LEVEL is not configurable when using django-debug-toolbar, as
    # it overrides root logger level if we use LoggingPanel
    # we can use a 'hack' and define level on handler, in this case special
    # 'root_console' handler
    'root': {
        'handlers': ['logfile'],
        'level': 'ERROR'
    }
}

# set up devserver if installed
try:
    import devserver
    INSTALLED_APPS += (
        'devserver',
    )
    # more details at https://github.com/dcramer/django-devserver#configuration
    DEVSERVER_DEFAULT_ADDR = '127.0.0.1'
    DEVSERVER_DEFAULT_PORT = '9999'
    DEVSERVER_AUTO_PROFILE = False  # use decorated functions
    DEVSERVER_TRUNCATE_SQL = True  # squash verbose output, show from/where
    DEVSERVER_MODULES = (
        # uncomment if you want to show every SQL executed
        # 'devserver.modules.sql.SQLRealTimeModule',
        # show sql query summary
        'devserver.modules.sql.SQLSummaryModule',
        # Total time to render a request
        'devserver.modules.profile.ProfileSummaryModule',

        # Modules not enabled by default
        # 'devserver.modules.ajax.AjaxDumpModule',
        # 'devserver.modules.profile.MemoryUseModule',
        # 'devserver.modules.cache.CacheSummaryModule',
        # see documentation for line profile decorator examples
        'devserver.modules.profile.LineProfilerModule',
        # show django session information
        'devserver.modules.request.SessionInfoModule',
    )
except ImportError:
    pass

# These are optional - only set if you have wierd issues like DataSource
# unknown
# GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'
# GDAL_LIBRARY_PATH = '/usr/lib/libgdal1.7.0.so.1'

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    # always show toolbar
    'SHOW_TOOLBAR_CALLBACK': lambda *args, **kwargs: False,
    'ENABLE_STACKTRACES': True
}

# show full Django debug report on TastyPie error
TASTYPIE_FULL_DEBUG = True
