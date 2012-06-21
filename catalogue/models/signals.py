# for product_date soft trigger
from django.contrib.gis.db import models
from products import OpticalProduct, RadarProduct, GenericImageryProduct
import datetime
import logging


def setGenericProductDate(sender, instance, **kw):
    """
    Sets the product_date based on acquisition date,
    if both start_date and end_date are set, then calculate the avg,
    uses the start_date if end_date is not set
    """
    if instance.product_acquisition_end:
        instance.product_date = datetime.datetime.fromordinal(instance.product_acquisition_start.toordinal() \
            + (instance.product_acquisition_end - instance.product_acquisition_start).days)
    else:
        instance.product_date = instance.product_acquisition_start
    logging.info('Pre-save signal activated for %s' % instance)


# ABP: doesn't work for GenericSensorProduct: needs the child (concrete) models :(
models.signals.pre_save.connect(setGenericProductDate, sender=OpticalProduct)
models.signals.pre_save.connect(setGenericProductDate, sender=RadarProduct)


def setGeometricResolution(sender, instance, **kw):
    """
    Sets default spatial_resolution_x and spatial_resolution_y
    from AcquisitionMode.spatial_resolution
    Sets spatial_resolution as the average value from spatial_resolution_x and spatial_resolution_y
    """
    #only trigger on real model save, do not trigger when importing fixtures
    #https://docs.djangoproject.com/en/1.4/ref/signals/#pre-save
    if not kw.get('raw', False):
        logging.info('Pre-save signal activated for %s' % instance)
        if not instance.spatial_resolution_x:
            instance.spatial_resolution_x = instance.acquisition_mode.spatial_resolution
            logging.debug('setting spatial_resolution_x to %s' % instance.spatial_resolution_x)
        if not instance.spatial_resolution_y:
            instance.spatial_resolution_y = instance.acquisition_mode.spatial_resolution
            logging.debug('setting spatial_resolution_y to %s' % instance.spatial_resolution_y)
        instance.spatial_resolution = (instance.spatial_resolution_y + instance.spatial_resolution_y) / 2.0
        logging.debug('setting spatial_resolution to %s' % instance.spatial_resolution)

        if not instance.band_count:
            instance.band_count = instance.acquisition_mode.band_count
            logging.debug('setting band_count to %s' % instance.band_count)

# Apply to all GenericImageryProduct and subclasses
models.signals.pre_save.connect(setGeometricResolution, sender=OpticalProduct)
models.signals.pre_save.connect(setGeometricResolution, sender=RadarProduct)
models.signals.pre_save.connect(setGeometricResolution, sender=GenericImageryProduct)
