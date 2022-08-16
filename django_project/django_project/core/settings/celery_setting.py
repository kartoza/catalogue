__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '4/27/16'

from celery.schedules import crontab

# daily every midnight
CELERY_BEAT_SCHEDULE = {
    'exchange-update': {
        'task': 'tasks.exchange_update',
        'schedule': crontab(minute=0, hour=0),
    },
    'data-summary-table': {
        'task': 'tasks.data_summary_table',
        'schedule': crontab(minute=0, hour=0),
        'args': ('/home/web/static/',),
    },
}

CELERY_TIMEZONE = 'UTC'
