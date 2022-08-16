"""
SANSA-EO Catalogue - PreSave signals for Catalogue Products

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '09/08/2012'
__copyright__ = 'South African National Space Agency'

import datetime
import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.db import models

from catalogue.models.products import (
    OpticalProduct,
    RadarProduct,
    GenericImageryProduct,
)


def setGenericProductDate(sender, instance, **kwargs):
    """
    Sets the product_date based on acquisition date,
    if both start_date and end_date are set, then calculate the avg,
    uses the start_date if end_date is not set

    Args:
        theSender - The model class
        theInstance - The actual instance being saved
        **kwargs - other keyword arguments
    Returns:
        None
    Exceptions:
        None
    """
    if instance.product_acquisition_end:
        instance.product_date = (
            datetime.datetime.fromordinal(
                instance.product_acquisition_start.toordinal() +
                (
                    instance.product_acquisition_end -
                    instance.product_acquisition_start
                )
                .days
            )
        )
    else:
        instance.product_date = instance.product_acquisition_start
    logger.info('Pre-save signal activated for %s' % instance)


# ABP: doesn't work for GenericSensorProduct
# needs the child (concrete) models :(
models.signals.pre_save.connect(
    setGenericProductDate,
    sender=OpticalProduct)

models.signals.pre_save.connect(
    setGenericProductDate,
    sender=RadarProduct)
