"""
SANSA-EO Catalogue - Uncategorized models

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
#for translation
from userprofile.models import BaseProfile
from catalogue.models.dictionaries import MissionSensor
from catalogue.models.products import GenericSensorProduct

###############################################################################


class Visit(models.Model):
    """
    Each time a visitor to the site arrives to the front page we will log
    their IP address and Lat/Long
    """

    city = models.CharField('City', max_length=255)
    country = models.CharField('Country', max_length=255)
    ip_address = models.IPAddressField('IP Address')
    ip_position = models.PointField('IP Lat/Long', srid=4326)
    visit_date = models.DateTimeField(
        'DateAdded', auto_now=True, auto_now_add=False
    )
    user = models.ForeignKey(User, null=True, blank=True)
    objects = models.GeoManager()

    def customSQL(self, sql_string, qkeys, args=None):
        from django.db import connection
        cursor = connection.cursor()
        #args MUST be parsed in case of SQL injection attempt
        #execute() does this automatically for us
        if args:
            cursor.execute(sql_string, args)
        else:
            cursor.execute(sql_string)
        rows = cursor.fetchall()
        fdicts = []
        for row in rows:
            i = 0
            cur_row = {}
            for key in qkeys:
                cur_row[key] = row[i]
                i = i + 1
            fdicts.append(cur_row)
        return fdicts

    class Meta:
        app_label = 'catalogue'
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'
        ordering = ('visit_date',)


class VisitorReport(models.Model):
    """
    This is a *special*, *read-only* model intended to
    be used for generating the visitors summary report as kml
    """
    visit_count = models.IntegerField()
    geometry = models.PointField(srid=4326, null=True, blank=True)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    objects = models.GeoManager()

    def __unicode(self):
        return str(self.city)

    class Meta:
        app_label = 'catalogue'
        db_table = u'vw_visitor_report'
        #requires django 1.1
        managed = False

##############################################################################


class SacUserProfile(BaseProfile):
    # See:
    # http://www.djangobook.com/en/1.0/chapter12/#cn222
    # We define extra properties we want to store about users
    # here - in particular if they belong to institutions
    # that have strategic partnerships with SAC so that they may
    # view hires spot data etc.
    #
    # update : 25 May 2010 - add django-profile app for more flexible
    # profile management. See http://code.google.com/p/django-profile/

    # This first field won't be made available to users in their
    # profile forms since admins must set it only if the user is a
    # employee of a sac strategic partner
    strategic_partner = models.BooleanField(
        'Strategic Partner?', help_text=('Mark this as true if the person '
        'belongs to an institution that is a CSIR/SAC strategic partner')
    )
    firstname = models.CharField(
        'First Name (required)', max_length=255, null=False, blank=False
    )
    surname = models.CharField(
        'Surname (required)', max_length=255, null=False, blank=False
    )
    url = models.URLField(blank=True)
    about = models.TextField(blank=True)
    address1 = models.CharField(
        'Address 1 (required)', max_length=255, null=False, blank=False
    )
    address2 = models.CharField(
        'Address 2 (required)', max_length=255, null=False, blank=False
    )
    address3 = models.CharField(max_length=255, blank=True)
    address4 = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(
        'Post Code (required)', max_length=25, null=False, blank=False
    )
    organisation = models.CharField(
        'Organisation (required)', max_length=255, null=False, blank=False
    )
    contact_no = models.CharField(
        'Contact No (required)', max_length=16, null=False, blank=False
    )

    class Meta:
        app_label = 'catalogue'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __unicode(self):
        return str(self.user.name)


class OrderNotificationRecipients(models.Model):
    """
    This class is used to map which staff members receive
    notifications for which sensors so that the notices when
    orders are placed/updated etc are targeted to the correct
    individuals
    """
    user = models.ForeignKey(User)
    sensors = models.ManyToManyField(
        MissionSensor,
        verbose_name='Sensors', null=True, blank=True,
        help_text=('Please choose one or more sensor. Use ctrl-click'
                   'to select more than one.')
    )
    classes = models.ManyToManyField(
        ContentType,
        null=True, blank=True,
        verbose_name='Product classes',
        help_text=('Please subscribe to one or more product class. Use '
                   'ctrl-click to select more than one.')
    )

    class Meta:
        app_label = 'catalogue'
        verbose_name = 'Order Notification Recipient'
        verbose_name_plural = 'Order Notification Recipients'

    def __unicode(self):
        return str(self.user.name)

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
                    sensors=instance.acquisition_mode.sensor_type.mission_sensor)
                .select_related()
            )])
        return listeners


class WorldBorders(models.Model):
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    geometry = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    class Meta:
        app_label = 'catalogue'

world_borders_mapping = {
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'name': 'NAME',
    'geometry': 'POLYGON'
}
