"""
SANSA-EO Catalogue - Order related models

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
#for user id foreign keys
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
# Helper classes
# ABP: unused ? from catalogue.geoiputils import *
from catalogue.nosubclassmanager import NoSubclassManager

from catalogue.models.products import GenericSensorProduct

###############################################################################
#
# Next bunch of models all relate to order management
#
###############################################################################


class Datum(models.Model):
    """
    Geographic datum model, used by Order DeliveryDetail records, i.e. WGS84
    """
    name = models.CharField('Name', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Datums'
        verbose_name_plural = 'Datums'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ResamplingMethod(models.Model):
    """
    Order ResamplingMethod model, used by Order DeliveryDetail records,
    i.e. Nearest Neighbour
    """
    name = models.CharField('Name', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Resampling Method'
        verbose_name_plural = 'Resampling Methods'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class FileFormat(models.Model):
    """
    Order FileFormat model, used by Order DeliveryDetail records, i.e. GeoTiff
    """
    name = models.CharField('Name', max_length=128, unique=True)

    class Meta:
        verbose_name = 'File Format'
        verbose_name_plural = 'File Formats'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class OrderStatus(models.Model):
    """
    OrderStatus model, used by Order and OrderStatusHistory to track current
    Order status, i.e. Placed, Completed, Awaiting info from client
    """
    name = models.CharField('Name', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Status List'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class DeliveryMethod(models.Model):
    """
    Types of Order DeliveryMethod, i.e. Download via FTP or HTTP, DVD(s)
    """
    name = models.CharField('Name', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Delivery Method'
        verbose_name_plural = 'Delivery Methods'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class DeliveryDetail(models.Model):
    """
    DeliveryDetail model, records processing parameters of an order
    """
    user = models.ForeignKey(User)
    processing_level = models.ForeignKey(
        'dictionaries.ProcessingLevel',
        verbose_name='Processing Level', default=3
    )
    projection = models.ForeignKey(
        'dictionaries.Projection', verbose_name='Projection', default=3
    )
    datum = models.ForeignKey(Datum, verbose_name='Datum', default=1)
    resampling_method = models.ForeignKey(
        ResamplingMethod, verbose_name='Resampling Method', default=2
    )  # cubic conv#cubic conv
    file_format = models.ForeignKey(
        FileFormat, verbose_name="File Format", default=1
    )
    #geometry field
    geometry = models.PolygonField(srid=4326, null=True, blank=True)
    #geomanager
    objects = models.GeoManager()

    class Meta:
        verbose_name = 'Delivery Detail'
        verbose_name_plural = 'Delivery Details'


class MarketSector(models.Model):
    """
    A dictionary table of market sectors in which an order will be used.
    """
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return str(self.name)


class Order(models.Model):
    """
    Order model, records orders placed by users
    """
    user = models.ForeignKey(User)
    notes = models.TextField(
        null=True, blank=True,
        help_text=(
            'Make a note of any special requirements or processing '
            'instructions (including processing levels). Please note that in '
            'the case of free products and priority products, they will only '
            'be supplied with default options.'
        ))
    order_status = models.ForeignKey(
        OrderStatus, verbose_name='Order Status', default=1)
    delivery_method = models.ForeignKey(
        DeliveryMethod, verbose_name='Delivery Method', default=1)
    delivery_detail = models.ForeignKey(DeliveryDetail, null=True, blank=True)
    market_sector = models.ForeignKey(
        MarketSector, null=False, blank=False, default=1)
    order_date = models.DateTimeField(
        verbose_name='Order Date', auto_now=True, auto_now_add=True,
        help_text='When the order was placed - not shown to users')
    #default manager
    objects = models.Manager()
    # A model can have more than one manager. Above will be used as default
    # see: http://docs.djangoproject.com/en/dev/topics/db/managers/
    # Also use a custom manager so that we can get
    # orders that have no subclass instances (since
    # we want to be able to list product orders while excluding
    # their TaskingRequest subclasses
    base_objects = NoSubclassManager()  # see catalogue/nosubclassmanager.py

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-order_date']

    def __unicode__(self):
        return str(self.id)

    def get_recent_history_date(self):
        current_status = OrderStatus.objects.get(name=self.order_status)
        recent_history = (
            OrderStatusHistory.objects.filter(order=self)
            .filter(new_order_status=current_status)
            .latest('order_change_date')
        )
        return recent_history.order_change_date


class OrderStatusHistory(models.Model):
    """
    Used to maintain provenance of all status changes that happen to an order
    """
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order)
    order_change_date = models.DateTimeField(
        verbose_name='Date', auto_now=True, auto_now_add=True,
        help_text='When the order status was changed')
    notes = models.TextField()
    old_order_status = models.ForeignKey(
        OrderStatus, verbose_name='Old Order Status',
        related_name='old_order_status')
    new_order_status = models.ForeignKey(
        OrderStatus, verbose_name='New Order Status',
        related_name='new_order_status')

    def __unicode__(self):
        return self.notes[:25]

    class Meta:
        verbose_name = 'Order Status History'
        verbose_name_plural = 'Order Status History'
        ordering = ('-order_change_date',)


class OrderNotificationRecipients(models.Model):
    """
    This class is used to map which staff members receive
    notifications for which sensors so that the notices when
    orders are placed/updated etc are targeted to the correct
    individuals
    """
    user = models.ForeignKey(User)
    satellite_instrument_group = models.ManyToManyField(
        'dictionaries.SatelliteInstrumentGroup',
        verbose_name='SatelliteInstrument', null=True, blank=True,
        help_text=(
            'Please choose one or more SatelliteInstrument. Use ctrl-click'
            'to select more than one.'
        )
    )
    classes = models.ManyToManyField(
        ContentType,
        null=True, blank=True,
        verbose_name='Product classes',
        help_text=(
            'Please subscribe to one or more product class. Use ctrl-click to '
            'select more than one.')
    )

    class Meta:
        verbose_name = 'Order Notification Recipient'
        verbose_name_plural = 'Order Notification Recipients'
        ordering = ['user']

    def __unicode__(self):
        return str(self.user.username)

    @staticmethod
    def getUsersForProduct(theProduct):
        """
        Returns all users registered to this product class or sensors

        Args:
            theProduct - instance of product model (Required)
        Returns:
            listeners - users monitoring contenttypes and sensors
        Exceptions:
            None
        """
        # Determines the product concrete class, should raise an error if does
        # not exists
        instance = theProduct.getConcreteInstance()
        # Get class listeners
        listeners = set([o.user for o in (
            OrderNotificationRecipients.objects
            .filter(
                classes=ContentType.objects.get_for_model(instance.__class__))
            .select_related()
        )])
        # Determines if is a sensor-based product and add sensor listeners
        if isinstance(instance, GenericSensorProduct):
            listeners.update([o.user for o in (
                OrderNotificationRecipients.objects
                .filter(
                    satellite_instrument_group=instance.product_profile
                    .satellite_instrument.satellite_instrument_group)
                .select_related()
            )])
        return listeners