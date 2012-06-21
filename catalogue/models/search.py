from django.contrib.gis.db import models
# for generating globally unique id's - I think python 2.5 is required
import uuid
from datetime import datetime
#for user id foreign keys
from django.contrib.auth.models import User
from orders import Order, DeliveryDetail
from products import GenericProduct, RadarProduct
from dictionaries import MissionSensor, AcquisitionMode, License, SensorType, Mission, ProcessingLevel
#for translation

from catalogue.fields import IntegersCSVIntervalsField

###############################################################################

class SearchRecord(models.Model):
    """ A class used for returning search results to a web page in a normalised
    way, regardless of which sensor was used etc.

    Normally the SearchRecord.save() method will only be called if you want to add
    an item to and order to the cart.

    By definition, cart items have no order ID, but do have a user id.

    Order items on the other hand will have both a user id and a order id.

    When the user creates a new order, all current search records that do not have
    an order id should be added to it .

    """
    user = models.ForeignKey(User)
    order = models.ForeignKey( Order, null=True, blank=True )
    product = models.ForeignKey( GenericProduct, null=False, blank=False )
    delivery_detail = models.ForeignKey( DeliveryDetail, null=True, blank=True )
    # DIMS ordering related fields
    internal_order_id = models.IntegerField(null=True, blank=True)
    download_path = models.CharField(max_length=512, null=False, blank=False, help_text="This is the location from where the product can be downloaded after a successfull OS4EO order placement.")
    # Default to False unless there is a populated local_storage_path in the product (see overridden save() below) or download_path is filled
    product_ready = models.BooleanField(default=False)

    # Required because genericproduct fkey references a table with geometry
    objects = models.GeoManager()

    class Meta:
        verbose_name = 'Record'
        verbose_name_plural = 'Records'
        app_label= 'catalogue'

    def __unicode__(self):
        return self.product.product_id

    def create( self, theUser, theProduct ):
        """Python has no support for overloading ctors"""
        myRecord = None
        # in future this could be other product types e.g. atmospheric or radar
        # which is wy search record is not modelled with a fkey ref to optical product
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
        super(SearchRecord, self).save(*args, **kwargs)


    def kmlExtents(self):
        """Return the extents of this product in kml xml notation"""
        myExtent = self.product.spatial_coverage.extent
        myString = """<north>%s</north>
          <south>%s</south>
          <east>%s</east>
          <west>%s</west>""" % (myExtent[3], #ymax
                                myExtent[1], #ymin
                                myExtent[2], #xmax
                                myExtent[0] ) #xmin
        return myString


    class Admin:
        pass


###############################################################################
#
# Every search a user does we will keep a record of
#
###############################################################################

class Search(models.Model):
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
      (SPATIAL_RESOLUTION_0,   '<= 1m'),
      (SPATIAL_RESOLUTION_1,   '1m - 2m'),
      (SPATIAL_RESOLUTION_2,   '2m - 6m'),
      (SPATIAL_RESOLUTION_3,   '6m - 20m'),
      (SPATIAL_RESOLUTION_4,   '20m - 35m'),
      (SPATIAL_RESOLUTION_5,   '35m - 60m'),
    )

    SPATIAL_RESOLUTION_RANGE = {
      SPATIAL_RESOLUTION_0:   (0.0, 1.0),
      SPATIAL_RESOLUTION_1:   (1.0, 2.0),
      SPATIAL_RESOLUTION_2:   (2.0, 6.0),
      SPATIAL_RESOLUTION_3:   (6.0, 20.0),
      SPATIAL_RESOLUTION_4:   (20.0, 35.0),
      SPATIAL_RESOLUTION_5:   (35.0, 60.0),
    }
    # ABP: added to store bands
    BAND_COUNT_PANCHROMATIC = 0
    BAND_COUNT_TRUECOLOR = 1
    BAND_COUNT_MULTISPECTRAL = 2
    BAND_COUNT_SUPERSPECTRAL = 3
    BAND_COUNT_HYPERSPECTRAL = 4

    BAND_COUNT_CHOICES = (
      (BAND_COUNT_PANCHROMATIC,   'Panchromatic'),
      (BAND_COUNT_TRUECOLOR,      'True colour (3 bands RGB)'),
      (BAND_COUNT_MULTISPECTRAL,  'Multispectral (4 - 8 bands)'),
      (BAND_COUNT_SUPERSPECTRAL,  'Superspectral (9 - 40 bands)'),
      (BAND_COUNT_HYPERSPECTRAL,  'Hyperspectral (> 41 bands)'),
    )

    BAND_COUNT_RANGE = {
      BAND_COUNT_PANCHROMATIC:    (0, 2),
      BAND_COUNT_TRUECOLOR:       (3, 3),
      BAND_COUNT_MULTISPECTRAL:   (4, 8),
      BAND_COUNT_SUPERSPECTRAL:   (9, 40),
      BAND_COUNT_HYPERSPECTRAL:   (41, 1000)
    }

    # ABP: added to store which product to search
    # Values for the search_type parameter
    PRODUCT_SEARCH_GENERIC = 0  # default in case of blank/null/0 = simple search
    PRODUCT_SEARCH_OPTICAL = 1
    PRODUCT_SEARCH_RADAR = 2
    PRODUCT_SEARCH_GEOSPATIAL = 3
    PRODUCT_SEARCH_IMAGERY = 4

    PRODUCT_SEARCH_TYPES = (
      (PRODUCT_SEARCH_GENERIC,    'Generic product search'),
      (PRODUCT_SEARCH_OPTICAL,    'Optical product search'),
      (PRODUCT_SEARCH_RADAR,      'Radar product search'),
      (PRODUCT_SEARCH_GEOSPATIAL, 'Geospatial product search'),
      # ABP: has no idea if this makes sense
      (PRODUCT_SEARCH_IMAGERY,    'Generic imagery product search'),
    )

    search_type = models.IntegerField('Search type', default=1,
        choices=PRODUCT_SEARCH_TYPES, db_index=True)
    user = models.ForeignKey(User)
    keywords = models.CharField('Keywords', max_length=255, blank=True)
    # foreign keys require the first arg to the be the relation name
    # so we explicitly have to use verbose_name for the user friendly name
    sensors = models.ManyToManyField(MissionSensor, verbose_name='Sensors',
        null=True, blank=True, help_text='Choosing one or more sensor is \
required. Use ctrl-click to select more than one.')
    geometry = models.PolygonField(srid=4326, null=True, blank=True,
        help_text='Digitising an area of interest is not required but is \
recommended.')
    k_orbit_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Path (K) value. If specified here, geometry will be ignored. \
Must be a value between 1 and 233. Can also be specified as a comma separated \
list of values or a range. Will be ignored if sensor type does not include J/K \
metadata.')
    j_frame_row = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Row (J) value. If specified here, geometry will be ignored. \
Must be a value between 1 and 248. Can also be specified as a comma separated \
list of values or a range. Will be ignored if sensor type does not include J/K \
metadata.')

    # let the user upload shp to define their search box
    # uploaded files will end up in media/uploads/2008/10/12 for example
    #geometry_file = models.FileField(null=True,blank=True,upload_to="uploads/%Y/%m/%d")
    ip_position = models.PointField(srid=4326, null=True, blank=True)
    search_date = models.DateTimeField('Search Date', auto_now=True,
        auto_now_add=True,
        help_text="When the search was made - not shown to users")
    # e.g. 16fd2706-8baf-433b-82eb-8c7fada847da
    guid = models.CharField(max_length=40, unique=True)
    deleted = models.NullBooleanField('Deleted?',
        blank=True,
        null=True,
        default=True,
        help_text='Mark this search as deleted so the user doesn not see it')
    use_cloud_cover = models.BooleanField('Use cloud cover?',
        blank=False,
        null=False,
        default=False,
        help_text='If you want to limit searches to optical products with a \
certain cloud cover, enable this.')
    cloud_mean = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Max Clouds",
        max_length=3)
    acquisition_mode = models.ForeignKey(AcquisitionMode, blank=True, null=True,
    help_text='Choose the acquisition mode.')  # e.g. M X T J etc
    license_type = models.IntegerField(choices=License.LICENSE_TYPE_CHOICES,
        blank=True, null=True, help_text='Choose a license type.')
    band_count = models.IntegerField(choices=BAND_COUNT_CHOICES, blank=True,
        null=True, help_text='Select the spectral resolution.')
    spatial_resolution = models.IntegerField(null=True, blank=True,
        verbose_name='Spatial resolution', choices=SPATIAL_RESOLUTION_OPTIONS,
        help_text='Select mean spatial resolution class.')
    # sensor_inclination_angle: range
    sensor_inclination_angle_start = models.FloatField(null=True, blank=True,
        help_text='Select sensor inclination angle start.')
    sensor_inclination_angle_end = models.FloatField(null=True, blank=True,
        help_text='Select sensor inclination angle end.')
    mission = models.ForeignKey(Mission, null=True, blank=True,
    help_text='Select satellite mission.')  # e.g. S5
    sensor_type = models.ForeignKey(SensorType, null=True, blank=True,
    related_name='search_sensor_type')  # e.g. CAM1
    processing_level = models.ManyToManyField(ProcessingLevel, null=True,
        blank=True, help_text='Select one or more processing level.')
    polarising_mode = models.CharField(max_length=1,
        choices=RadarProduct.POLARISING_MODE_CHOICES, null=True, blank=True)
    record_count = models.IntegerField(blank=True, null=True, editable=False)
    # Use the geo manager to handle geometry
    objects = models.GeoManager()

    class Meta:
        app_label = 'catalogue'
        verbose_name = 'Search'
        verbose_name_plural = 'Searches'
        ordering = ('search_date',)

    def save(self):
        #makes a random globally unique id
        if not self.guid or self.guid == 'null':
            self.guid = str(uuid.uuid4())
        super(Search, self).save()

    def __unicode__(self):
        return "%s Guid: %s User: %s" % (self.search_date, self.guid, self.user)

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

    @staticmethod
    def getDictionaryMap(parm):
        """
        Returns the right join chain from a Product model to dictionary
        parameter

        for example:
        getSensorDictionaryMap('mission')
        will return
        'acquisition_mode__sensor_type__mission_sensor__mission'
        """
        if parm == 'sensor_type':
            return 'acquisition_mode__sensor_type'
        if parm == 'mission_sensor':
            return 'acquisition_mode__sensor_type__mission_sensor'
        if parm == 'mission':
            return 'acquisition_mode__sensor_type__mission_sensor__mission'
        return parm

    @property
    def isAdvanced(self):
        """
        Checks wether the Search is an advanced Search.
        Condition for being an advanced search is that at least one of the
        advanced parameter is set
        """
        myAdvParameterTestList = [
            self.processing_level.count() > 0,
            self.keywords != '',
            self.k_orbit_path is not None,
            self.j_frame_row is not None,
            self.use_cloud_cover == True,
            self.acquisition_mode is not None,
            self.spatial_resolution is not None,
            self.band_count is not None,
            self.sensor_inclination_angle_start is not None,
            self.sensor_inclination_angle_end is not None,
            self.mission is not None,
            self.license_type is not None,
            self.sensor_type is not None
        ]
        #if any of myAdvParameterTestList is True, return True
        return any(myAdvParameterTestList)

    def sensorsAsString(self):
        myList = self.sensors.values_list('operator_abbreviation', flat=True)
        myString = ", ".join(myList)
        return myString

    def datesAsString(self):
        """
        Date ranges formatted
        """
        result = []
        for d in self.searchdaterange_set.all():
            result.append(d.local_format())
        return ", ".join(result)

    def getRowChoices(self):
        """
        Returns a list of choices
        """
        choices = []
        for r in IntegersCSVIntervalsField.to_tuple(self.j_frame_row):
            if len(r) == 1:
                choices.append(r[0])
            else:
                choices.extend(range(r[0], r[1] + 1))
        choices.sort()
        return choices

    def getPathChoices(self):
        """
        Returns a list of choices
        """
        choices = []
        for r in IntegersCSVIntervalsField.to_tuple(self.k_orbit_path):
            if len(r) == 1:
                choices.append(r[0])
            else:
                choices.extend(range(r[0], r[1] + 1))
        choices.sort()
        return choices

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

    start_date = models.DateField(help_text='Product date is required. DD-MM-YYYY.')
    end_date = models.DateField(help_text='Product date is required. DD-MM-YYYY.')
    search = models.ForeignKey(Search)

    class Meta:
        app_label= 'catalogue'

    def __unicode__(self):
        return "%s Guid: %s" % (self.local_format(), self.search.guid)

    def local_format(self):
        """
        Returns a string describing locally formatted date range
        """
        return "%s : %s" % (self.start_date.strftime(SearchDateRange.local_format_string), self.end_date.strftime(SearchDateRange.local_format_string))

    @staticmethod
    def from_local_format(formatted_value):
        """
        Returns the date range tuple
        """
        return datetime.strptime(formatted_value[:10], SearchDateRange.local_format_string), datetime.strptime(formatted_value[-10:], SearchDateRange.local_format_string)


###############################################################################

class Clip( models.Model ):
    """ Stores the information about clip performed by the user. The clip is actually
    done by Lion via urllib, then results saved in /clips/guid and Clip model is
    updated with url and is_completed flag is set to True. User will be notified
    by email and/or via a view that shows all clips and their status."""
    guid = models.CharField(max_length=40)
    owner = models.ForeignKey( User )
    date = models.DateTimeField(verbose_name="Date", auto_now=True, auto_now_add=True, help_text="Not shown to users")
    ## provisory hardcoded choices for clipped image source.
    image = models.CharField( max_length=20,
                              choices = [(0,"zaSpot2mMosaic2009"),
                                         (1,"zaSpot2mMosaic2008"),
                                         (2,"zaSpot2mMosaic2007")])
    # polygon is the one from the shapefile
    geometry = models.PolygonField( srid = 4326 )
    objects = models.GeoManager()
    status = models.CharField( max_length=20,
                              choices = [(0, "submitted"),
                                         (1, "in process"),
                                         (2, "completed")])
    # the result of the clipping operation is available via a URL that is sent to the user
    result_url =  models.URLField( max_length=1024, verify_exists=True )

    def save(self):
        #makes a random globally unique id
        if not self.guid or self.guid=='null':
            self.guid = str(uuid.uuid4())
        super(Clip, self).save()

    class Meta:
        app_label= 'catalogue'
        verbose_name="Clip"
        verbose_name_plural="Clips"
