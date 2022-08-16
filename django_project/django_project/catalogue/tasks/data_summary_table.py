__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '4/29/16'


from django.core import management
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist


import logging
logger = logging.getLogger(__name__)

# This is data summary table task, we can use it for updating data summary table data.

@shared_task(name='tasks.data_summary_table')
def data_summary_table(json_path):
    management.call_command('data_summary_table', json_path)