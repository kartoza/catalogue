"""
SANSA-EO Catalogue - Signals for Search

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '06/02/2014'
__copyright__ = 'South African National Space Agency'

import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.db import models
from .models import SearchRecord


def cache_model_attributes(sender, instance, **kwargs):
    """
    Take a snapshot of current attribute values
    """
    instance._cached_data = instance.__dict__.copy()

# set post_init signal
models.signals.post_init.connect(
    cache_model_attributes, sender=SearchRecord
)
