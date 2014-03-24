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
import datetime

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '09/08/2012'
__copyright__ = 'South African National Space Agency'

from django.contrib.gis.db import models

#for user id foreign keys
from django.contrib.auth.models import User

from offline_messages.models import OfflineMessage
from offline_messages.utils import create_offline_message, constants

from catalogue.dbhelpers import executeRAWSQL


###############################################################################

class VisitHelpersManager(models.GeoManager):
    """
    Visit model helper methods
    """
    def countryStats(self, **kwargs):
        """
        Count visits per country

        NOTE: We need to use executeRAWSQL as manager.raw method requires
        PrimaryKey to be returned which is then used to map objects back to the
        model

        sort_col and sort_order used to allow for sorting of data in rendered
        table in view.
        """
        sort_col = kwargs.get('sort_col', 'count')
        sort_order = kwargs.get('sort_order', 'DESC')
        results = executeRAWSQL("""
SELECT LOWER(country) as country, COUNT(*) AS count
FROM catalogue_visit
GROUP BY LOWER(country)
ORDER BY %s %s;""" % (sort_col, sort_order))

        return results

    def monthlyReport(self, theDate):
        """
        Count visits per country for each month

        sort_col and sort_order used to allow for sorting of data in rendered
        table in view.
        :param kwargs: Contains sort_col and sort_order for table rendering
        :param the_date: The requested date for the report
        """
        myResults = executeRAWSQL("""
SELECT LOWER(country) as country ,count(*) as count, DATE_TRUNC('month',
visit_date) as month
FROM catalogue_visit
WHERE visit_date BETWEEN to_date(%(date)s,'MM-YYYY')
    AND to_date(%(date)s,'MM-YYYY')+ interval '1 month'
GROUP BY LOWER(country),DATE_TRUNC('month',visit_date)
ORDER BY count DESC;""", {'date': theDate.strftime('%m-%Y')})
        return myResults


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
    helpers = VisitHelpersManager()

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
        ordering = ['visit_count']

##############################################################################


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


class AllUsersMessage(models.Model):
    """A simple model for creating messages to broadcase to all users."""
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Specifies which database this model ORM goes to
        app_label = 'catalogue'
        ordering = ['-created']

    def save(self, *args, **kwargs):
        """Broadcase the message using offline messages."""
        for myUser in User.objects.all():
            myNotifiedAlreadyFlag = OfflineMessage.objects.filter(
                user=myUser, message=self.message).exists()
            if not myNotifiedAlreadyFlag:
                create_offline_message(
                    myUser, self.message, level=constants.INFO)
        super(AllUsersMessage, self).save(*args, **kwargs)
