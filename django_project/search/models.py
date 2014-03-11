"""
SANSA-EO Catalogue - Search related models

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
__date__ = '16/08/2012'
__copyright__ = 'South African National Space Agency'

# for generating globally unique id's - I think python 2.5 is required
import uuid
import json
from datetime import datetime

from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist

from exchange.conversion import convert_value

from catalogue.dbhelpers import executeRAWSQL

from dictionaries.models import (
    SpectralModeProcessingCosts,
    InstrumentTypeProcessingLevel
)

###############################################################################


class SearchRecord(models.Model):
    """
    A class used for returning search results to a web page in a normalised
    way, regardless of which sensor was used etc.

    Normally the SearchRecord.save() method will only be called if you want to
    add an item to and order to the cart.

    By definition, cart items have no order ID, but do have a user id.

    Order items on the other hand will have both a user id and a order id.

    When the user creates a new order, all current search records that do not
    havean order id should be added to it.
    """
    user = models.ForeignKey('auth.User')
    order = models.ForeignKey('orders.Order', null=True, blank=True)
    product = models.ForeignKey(
        'catalogue.GenericProduct', null=False, blank=False)
    # DIMS ordering related fields
    internal_order_id = models.IntegerField(null=True, blank=True)
    download_path = models.CharField(
        max_length=512, null=False, blank=False,
        help_text=(
            'This is the location from where the product can be downloaded '
            'after a successfull OS4EO order placement.'))
    # Default to False unless there is a populated local_storage_path in the
    # product (see overridden save() below) or download_path is filled
    product_ready = models.BooleanField(default=False)
    cost_per_scene = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    rand_cost_per_scene = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    currency = models.ForeignKey(
        'exchange.Currency', null=True, blank=True
    )
    processing_level = models.ForeignKey(
        'dictionaries.ProcessingLevel', verbose_name='Processing Level',
        null=True, blank=True
    )
    projection = models.ForeignKey(
        'dictionaries.Projection', verbose_name='Projection',
        null=True, blank=True
    )
    product_process_state = models.ForeignKey(
        'dictionaries.ProductProcessState', null=True, blank=True
    )
    # Required because genericproduct fkey references a table with geometry
    objects = models.GeoManager()

    class Meta:
        verbose_name = 'Record'
        verbose_name_plural = 'Records'

    def __unicode__(self):
        return self.product.product_id

    def availableUTMZonesJSON(self):
        """
        json formatted available UTM zones for product
        used in order page for populating available product UTM zones
        """
        return json.dumps(
            [list(zone) for zone in self.product.getUTMZones(theBuffer=1)])

    def availableProcessingLevelsJSON(self):
        """
        json formated available processing levels for products
        user in order page for populating available product processing
        options
        """
        availableLevels = (
            self.product.getConcreteInstance().availableProcessingLevels()
        )
        levels = list()
        for lvl in availableLevels:
            insTypeProcLevel = InstrumentTypeProcessingLevel.objects.filter(
            processing_level=lvl,
            instrument_type=(
                self.product.getConcreteInstance().product_profile
                .satellite_instrument.satellite_instrument_group
                .instrument_type
            )
            ).get()
            try:
                spectralModeProcCosts = SpectralModeProcessingCosts.objects.filter(
                spectral_mode=(
                    self.product.getConcreteInstance().product_profile
                    .spectral_mode
                ),
                instrument_type_processing_level=insTypeProcLevel
                ).get()
                rand_cost_per_scene = convert_value(
                spectralModeProcCosts.cost_per_scene,
                spectralModeProcCosts.currency.code, 'ZAR'
                )
            except ObjectDoesNotExist:
                rand_cost_per_scene = 0;
            levels.append([lvl.id, lvl.name, int(rand_cost_per_scene)])
        # add base level and cost
        try:
            instrumentType = self.product.getConcreteInstance().product_profile.satellite_instrument.satellite_instrument_group.instrument_type
            baseinsTypeProcLevel = InstrumentTypeProcessingLevel.objects.filter(
                processing_level=instrumentType.base_processing_level,
                instrument_type=instrumentType).get()
            basespectralModeProcCosts = SpectralModeProcessingCosts.objects.filter(
                spectral_mode=(
                    self.product.getConcreteInstance().product_profile
                    .spectral_mode
                ),
                instrument_type_processing_level=baseinsTypeProcLevel
                ).get()
            rand_cost_per_scene = convert_value(
                basespectralModeProcCosts.cost_per_scene,
                basespectralModeProcCosts.currency.code, 'ZAR'
                )
        except ObjectDoesNotExist:
                rand_cost_per_scene = 0;
        levels.append([14, 'Level 0 Raw instrument data', rand_cost_per_scene])
        return json.dumps([list(level) for level in levels])

    def create(self, theUser, theProduct):
        """Python has no support for overloading constrctors"""
        myRecord = None
        # in future this could be other product types e.g. atmospheric or radar
        # which is wy search record is not modelled with a fkey ref to optical
        # product
        myRecord = SearchRecord()
        myRecord.user = theUser
        myRecord.product = theProduct

        return myRecord

    def save(self, *args, **kwargs):
        """
        Set product_ready according to local_storage_path and download_path
        """
        if not self.pk:
            if self.product.local_storage_path or self.download_path:
                self.product_ready = True
            else:
                self.product_ready = False
        # if order is null and searchrecord is updated, make snapshot at the
        # time of placing order
        if (self.pk and self._cached_data.get('order_id') is None and
                self.order_id is not None):
            # snapshot data and suppress save (we are in a save method)
            self._snapshot_cost_and_currency(save=False)

        super(SearchRecord, self).save(*args, **kwargs)

    def kmlExtents(self):
        """Return the extents of this product in kml xml notation"""
        myExtent = self.product.spatial_coverage.extent
        myString = """<north>%s</north>
          <south>%s</south>
          <east>%s</east>
          <west>%s</west>""" % (
            myExtent[3],  # ymax
            myExtent[1],  # ymin
            myExtent[2],  # xmax
            myExtent[0])  # xmin
        return myString

    def _snapshot_cost_and_currency(self, save=True):
        """
        This method will grab latest price_per_km and currency and save them
        to the model in the moment of order creation

        This method is invoked by a post_save signal on Order model
        """
        # identify InstrumentTypeProcessingLevel
        insTypeProcLevel = InstrumentTypeProcessingLevel.objects.filter(
            processing_level=self.processing_level,
            instrument_type=(
                self.product.getConcreteInstance().product_profile
                .satellite_instrument.satellite_instrument_group
                .instrument_type
            )
        ).get()
        # retrieve the processing mode costs
        spectralModeProcCosts = SpectralModeProcessingCosts.objects.filter(
            spectral_mode=(
                self.product.getConcreteInstance().product_profile
                .spectral_mode
            ),
            instrument_type_processing_level=insTypeProcLevel
        ).get()
        # snapshot current values
        self.cost_per_scene = spectralModeProcCosts.cost_per_scene
        self.currency = spectralModeProcCosts.currency
        self.rand_cost_per_scene = convert_value(
            spectralModeProcCosts.cost_per_scene,
            spectralModeProcCosts.currency.code, 'ZAR'
        )

        # invoke model save method - default behaviour
        if save is True:
            self.save()


###############################################################################
#
# Every search a user does we will keep a record of
#
###############################################################################

class BaseSearch(models.Model):
    """
    ABC Search model, generic search fields
    """
    user = models.ForeignKey('auth.User', null=True, blank=True)
    geometry = models.PolygonField(
        srid=4326, null=True, blank=True,
        help_text=
        'Digitising an area of interest is not required but is recommended.')

    ip_position = models.PointField(srid=4326, null=True, blank=True)
    search_date = models.DateTimeField(
        'Search Date', auto_now=True, auto_now_add=True,
        help_text='When the search was made - not shown to users')
    # e.g. 16fd2706-8baf-433b-82eb-8c7fada847da
    guid = models.CharField(max_length=40, unique=True)
    deleted = models.NullBooleanField(
        'Deleted?', blank=True, null=True, default=True,
        help_text='Mark this search as deleted so the user doesn not see it')

    record_count = models.IntegerField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        #makes a random globally unique id
        if not self.guid or self.guid == 'null':
            self.guid = str(uuid.uuid4())
        super(BaseSearch, self).save(*args, **kwargs)


class SearchHelpersManager(models.GeoManager):
    """
    Search model helper methods
    """
    def monthlyReport(self, theDate):
        """
        Count searches per country for user each month
        """
        myResults = executeRAWSQL("""
WITH search_geom AS (SELECT a.name, b.search_date FROM catalogue_worldborders a
    INNER JOIN search_search b ON
    st_intersects(a.geometry,b.ip_position))
SELECT name as country, date_trunc('month',search_date) as month,
    count(*) as count
FROM search_geom
WHERE search_date BETWEEN to_date(%(date)s,'MM-YYYY') AND
    to_date(%(date)s,'MM-YYYY') + interval '1 month'
GROUP BY name,date_trunc('month',search_date)
ORDER BY count DESC;""", {'date': theDate.strftime('%m-%Y')})

        return myResults

    def monthlyReportAOI(self, theDate):
        """
        Count AOI searches per country per each month
        """
        myResults = executeRAWSQL("""
SELECT a.name as country, date_trunc('month',b.search_date) as month,
    count(*) as count
FROM catalogue_worldborders a INNER JOIN search_search b ON
    st_intersects(a.geometry,b.geometry)
WHERE search_date between to_date(%(date)s,'MM-YYYY') AND
        to_date(%(date)s,'MM-YYYY') + interval '1 month'
GROUP BY  a.name,date_trunc('month',b.search_date)
ORDER BY count desc;""", {'date': theDate.strftime('%m-%Y')})

        return myResults


class Search(BaseSearch):
    """
    Stores search results
    """
    # ABP: added to store spatial_resolution ranges
    # Values for spatial_resolution
    SPATIAL_RESOLUTION_0 = 0
    SPATIAL_RESOLUTION_1 = 1
    SPATIAL_RESOLUTION_2 = 2
    SPATIAL_RESOLUTION_3 = 3
    SPATIAL_RESOLUTION_4 = 4
    SPATIAL_RESOLUTION_5 = 5

    SPATIAL_RESOLUTION_OPTIONS = (
        (SPATIAL_RESOLUTION_0, '<= 1m'),
        (SPATIAL_RESOLUTION_1, '1m - 2m'),
        (SPATIAL_RESOLUTION_2, '2m - 6m'),
        (SPATIAL_RESOLUTION_3, '6m - 20m'),
        (SPATIAL_RESOLUTION_4, '20m - 35m'),
        (SPATIAL_RESOLUTION_5, '35m - 60m'),
    )

    SPATIAL_RESOLUTION_RANGE = {
        SPATIAL_RESOLUTION_0: (0.0, 1.0),
        SPATIAL_RESOLUTION_1: (1.0, 2.0),
        SPATIAL_RESOLUTION_2: (2.0, 6.0),
        SPATIAL_RESOLUTION_3: (6.0, 20.0),
        SPATIAL_RESOLUTION_4: (20.0, 35.0),
        SPATIAL_RESOLUTION_5: (35.0, 60.0),
    }
    # ABP: added to store bands
    BAND_COUNT_PANCHROMATIC = 0
    BAND_COUNT_TRUECOLOR = 1
    BAND_COUNT_MULTISPECTRAL = 2
    BAND_COUNT_SUPERSPECTRAL = 3
    BAND_COUNT_HYPERSPECTRAL = 4

    BAND_COUNT_CHOICES = (
        (BAND_COUNT_PANCHROMATIC, 'Panchromatic'),
        (BAND_COUNT_TRUECOLOR, 'True colour (3 bands RGB)'),
        (BAND_COUNT_MULTISPECTRAL, 'Multispectral (4 - 8 bands)'),
        (BAND_COUNT_SUPERSPECTRAL, 'Superspectral (9 - 40 bands)'),
        (BAND_COUNT_HYPERSPECTRAL, 'Hyperspectral (> 41 bands)'),
    )

    BAND_COUNT_RANGE = {
        BAND_COUNT_PANCHROMATIC: (0, 2),
        BAND_COUNT_TRUECOLOR: (3, 3),
        BAND_COUNT_MULTISPECTRAL: (4, 8),
        BAND_COUNT_SUPERSPECTRAL: (9, 40),
        BAND_COUNT_HYPERSPECTRAL: (41, 1000)
    }

    # foreign keys require the first arg to the be the relation name
    # so we explicitly have to use verbose_name for the user friendly name
    instrument_type = models.ManyToManyField(
        'dictionaries.InstrumentType',
        verbose_name=u'Sensors', null=True, blank=True,
        help_text=(
            'Choosing one or more instrument types is required. Use ctrl-click'
            ' to select more than one.')
    )
    satellite = models.ManyToManyField(
        'dictionaries.Satellite', null=True, blank=True,
        help_text='Select satellite mission.'
    )  # e.g. S5

    k_orbit_path = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=(
            'Path (K) value. If specified here, geometry will be ignored. '
            'Must be a value between 1 and 233. Can also be specified as a '
            'comma separated list of values or a range. Will be ignored if '
            'sensor type does not include J/K metadata.')
    )
    j_frame_row = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=(
            'Row (J) value. If specified here, geometry will be ignored. Must '
            'be a value between 1 and 248. Can also be specified as a comma '
            'separated list of values or a range. Will be ignored if sensor '
            'type does not include J/K metadata.')
    )
    use_cloud_cover = models.BooleanField(
        'Use cloud cover?', blank=False, null=False, default=False,
        help_text=(
            'If you want to limit searches to optical products with a certain '
            'cloud cover, enable this.')
    )
    cloud_mean = models.IntegerField(
        null=True, blank=True, max_length=3,
        verbose_name="Max Clouds"
    )
    license_type = models.ManyToManyField(
        'dictionaries.License', blank=True, null=True,
        help_text='Choose a license type.'
    )
    band_count = models.IntegerField(
        choices=BAND_COUNT_CHOICES, blank=True, null=True,
        help_text='Select the spectral resolution.'
    )
    spatial_resolution = models.IntegerField(
        null=True, blank=True, verbose_name='Spatial resolution',
        choices=SPATIAL_RESOLUTION_OPTIONS,
        help_text='Select mean spatial resolution class.'
    )
    # sensor_inclination_angle: range
    sensor_inclination_angle_start = models.FloatField(
        null=True, blank=True,
        help_text='Enter a minimum sensor inclination angle.'
    )
    sensor_inclination_angle_end = models.FloatField(
        null=True, blank=True,
        help_text='Enter a maximum sensor inclination angle.'
    )
    spectral_group = models.ManyToManyField(
        'dictionaries.SpectralGroup',
        null=True, blank=True,
        help_text='Select one or more spectral groups.'
    )
    processing_level = models.ManyToManyField(
        'dictionaries.ProcessingLevel', null=True, blank=True,
        help_text='Select one or more processing level.'
    )
    collection = models.ManyToManyField(
        'dictionaries.Collection', null=True, blank=True,
        help_text='Select one or more satellite collections.'
    )
    # Use the geo manager to handle geometry
    objects = models.GeoManager()
    helpers = SearchHelpersManager()

    class Meta:
        verbose_name = 'Search'
        verbose_name_plural = 'Searches'
        ordering = ('search_date',)

    def __unicode__(self):
        return "%s Guid: %s User: %s" % (
            self.search_date, self.guid, self.user)

    def datesAsString(self):
        """
        Date ranges formatted
        """
        result = []
        for d in self.searchdaterange_set.all():
            result.append(d.local_format())
        return ', '.join(result)

###############################################################################
#
# Search date ranges
#
###############################################################################


class SearchDateRange(models.Model):
    """
    Stores the date ranges for the Search model
    """

    local_format_string = '%d-%m-%Y'

    start_date = models.DateField(
        help_text='Product date is required. DD-MM-YYYY.')
    end_date = models.DateField(
        help_text='Product date is required. DD-MM-YYYY.')
    search = models.ForeignKey(Search)

    def __unicode__(self):
        return "%s Guid: %s" % (self.local_format(), self.search.guid)

    def local_format(self):
        """
        Returns a string describing locally formatted date range
        """
        return '%s : %s' % (
            self.start_date.strftime(SearchDateRange.local_format_string),
            self.end_date.strftime(SearchDateRange.local_format_string))

    @staticmethod
    def from_local_format(formatted_value):
        """
        Returns the date range tuple
        """
        return (
            datetime.strptime(
                formatted_value[:10], SearchDateRange.local_format_string),
            datetime.strptime(
                formatted_value[-10:], SearchDateRange.local_format_string))


###############################################################################

class Clip(models.Model):
    """
    Stores the information about clip performed by the user. The clip is
    actually done by Lion via urllib, then results saved in /clips/guid and
    Clip model is updated with url and is_completed flag is set to True. User
    will be notified by email and/or via a view that shows all clips and their
    status.
    """
    guid = models.CharField(max_length=40)
    owner = models.ForeignKey('auth.User')
    date = models.DateTimeField(
        verbose_name='Date', auto_now=True, auto_now_add=True,
        help_text='Not shown to users')
    ## provisory hardcoded choices for clipped image source.
    image = models.CharField(
        max_length=20,
        choices=[
            (0, 'zaSpot2mMosaic2009'),
            (1, 'zaSpot2mMosaic2008'),
            (2, 'zaSpot2mMosaic2007')])
    # polygon is the one from the shapefile
    geometry = models.PolygonField(srid=4326)
    status = models.CharField(
        max_length=20,
        choices=[
            (0, 'submitted'),
            (1, 'in process'),
            (2, 'completed')])
    # the result of the clipping operation is available via a URL that is sent
    # to the user
    result_url = models.URLField(max_length=1024)

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        #makes a random globally unique id
        if not self.guid or self.guid == 'null':
            self.guid = str(uuid.uuid4())
        super(Clip, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Clip'
        verbose_name_plural = 'Clips'
