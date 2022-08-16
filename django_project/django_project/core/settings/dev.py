from .project import *

# Set debug to True for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# set up Django Debug Toolbar if installed
# try:
#     import debug_toolbar
#     MIDDLEWARE += (
#         'debug_toolbar.middleware.DebugToolbarMiddleware',
#     )
#     INSTALLED_APPS += (
#         'debug_toolbar',
#     )
#     DEBUG_TOOLBAR_CONFIG = {
#         'INTERCEPT_REDIRECTS': False,
#         # always show toolbar
#         'SHOW_TOOLBAR_CALLBACK': lambda *args, **kwargs: False,
#         'ENABLE_STACKTRACES': True
#     }
#     DEBUG_TOOLBAR_PANELS = (
#         'debug_toolbar.panels.version.VersionDebugPanel',
#         'debug_toolbar.panels.timer.TimerDebugPanel',
#         'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#         'debug_toolbar.panels.headers.HeaderDebugPanel',
#         'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#         'debug_toolbar.panels.template.TemplateDebugPanel',
#         'debug_toolbar.panels.sql.SQLDebugPanel',
#         'debug_toolbar.panels.signals.SignalDebugPanel',
#         #'debug_toolbar.panels.logger.LoggingPanel',
#     )
# except ImportError:
#     pass

# Make sure static files storage is set to default
