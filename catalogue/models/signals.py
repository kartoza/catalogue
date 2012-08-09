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


from django.contrib.gis.db import models
from catalogue.models.products import (
    OpticalProduct,
    RadarProduct,
    GenericImageryProduct,
)
import datetime
import logging


def setGenericProductDate(theSender, theInstance, **kwargs):
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
    if theInstance.product_acquisition_end:
        theInstance.product_date = (
            datetime.datetime.fromordinal(
                theInstance.product_acquisition_start.toordinal() +
                (
                    theInstance.product_acquisition_end -
                    theInstance.product_acquisition_start
                )
                .days
            )
        )
    else:
        theInstance.product_date = theInstance.product_acquisition_start
    logging.info('Pre-save signal activated for %s' % theInstance)


# ABP: doesn't work for GenericSensorProduct
# needs the child (concrete) models :(
models.signals.pre_save.connect(
    reciever=setGenericProductDate,
    sender=OpticalProduct)

models.signals.pre_save.connect(
    reciever=setGenericProductDate,
    sender=RadarProduct)


def setGeometricResolution(theSender, theInstance, **kwargs):
    """
    Sets default spatial_resolution_x and spatial_resolution_y
    from AcquisitionMode.spatial_resolution
    Sets spatial_resolution as the average value from spatial_resolution_x and
    spatial_resolution_y

    Args:
        theSender - The model class
        theInstance - The actual instance being saved
        **kwargs - other keyword arguments
    Returns:
        None
    Exceptions:
        None
    """

    #only trigger on real model save, do not trigger when importing fixtures
    #https://docs.djangoproject.com/en/1.4/ref/signals/#pre-save
    if not kwargs.get('raw', False):
        logging.info('Pre-save signal activated for %s' % theInstance)
        if not theInstance.spatial_resolution_x:
            theInstance.spatial_resolution_x = (
                theInstance.acquisition_mode.spatial_resolution)
            logging.debug('setting spatial_resolution_x to %s' % (
                theInstance.spatial_resolution_x,)
            )
        if not theInstance.spatial_resolution_y:
            theInstance.spatial_resolution_y = (
                theInstance.acquisition_mode.spatial_resolution)
            logging.debug('setting spatial_resolution_y to %s' % (
                theInstance.spatial_resolution_y,)
            )
        theInstance.spatial_resolution = (
            theInstance.spatial_resolution_y +
            theInstance.spatial_resolution_y) / 2.0
        logging.debug('setting spatial_resolution to %s' % (
            theInstance.spatial_resolution,)
        )

        if not theInstance.band_count:
            theInstance.band_count = theInstance.acquisition_mode.band_count
            logging.debug('setting band_count to %s' % theInstance.band_count)

# Apply to all GenericImageryProduct and subclasses
models.signals.pre_save.connect(
    reciever=setGeometricResolution,
    sender=OpticalProduct)

models.signals.pre_save.connect(
    reciever=setGeometricResolution,
    sender=RadarProduct)

models.signals.pre_save.connect(
    reciever=setGeometricResolution,
    sender=GenericImageryProduct)
