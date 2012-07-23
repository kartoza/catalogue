#from packagekit.enums import LICENSE_TPL
from django.contrib.gis.db import models

###############################################################################
# Product related model ancilliary tables
###############################################################################

class MissionGroup( models.Model ):
    """Mission Group"""
    name = models.CharField( max_length="255", unique=True )
    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name


###############################################################################

class Mission(models.Model):
    """Satellite or Mission"""
    abbreviation = models.CharField(max_length=3, unique=True)  # SAC abbreviation
    operator_abbreviation = models.CharField(max_length=255, unique=True)  # UI abbreviation
    name = models.CharField(max_length=255, unique=True)
    mission_group = models.ForeignKey(MissionGroup)  # e.g. S5
    owner = models.CharField(max_length=255)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        """
        Return 'operator_abbreviation' as model representation

        - in case 'operator_abbreviation' is an empty string (blank)
            - return 'abbreviation'
        """
        if self.operator_abbreviation:
            return "%s" % self.operator_abbreviation
        else:
            return "%s" % self.abbreviation


###############################################################################

class MissionSensor( models.Model ):
    """
    MissionSensor on the mission or satellite - e.g. HRV
    ABP: TODO: get rid of has_data (or auto-update with soft trigger ?)
    """
    abbreviation = models.CharField( max_length="3")
    name = models.CharField( max_length="255" )
    description = models.TextField()
    has_data = models.BooleanField(help_text='Mark false if there is no data for this sensor')
    mission = models.ForeignKey(Mission) # e.g. S5
    is_radar = models.BooleanField(help_text='Mark true if this sensor is a radar sensor', default=False)
    is_taskable = models.BooleanField(default=False, help_text="Can this sensor be tasked?")
    operator_abbreviation = models.CharField( max_length=255, unique=True ) # UI abbreviation
    class Meta:
        app_label= 'catalogue'
        unique_together = ('mission', 'abbreviation')
    def __unicode__(self):
        if self.name:
            return "%s:%s" % (self.mission.operator_abbreviation, self.name)
        else:
            return "%s:%s" % (self.mission.operator_abbreviation,self.abbreviation)


###############################################################################

class SensorType( models.Model ):
    """Sensor type
       @note: Moved notes below and above from AcuisitionMode class to here on 2 June 2010
              as they were mixed up
       @note: mode examples:
             J = Multispectral 10m
             P/M = Panchromatic 10m
             A/B = Panchromatic 5m
             T = Panchromatic 2.5m
             X = Multispectral 20m
             JT = Pansharpened 2.5m Multispectral"""
    abbreviation = models.CharField( max_length="4")
    name = models.CharField( max_length="255" )
    mission_sensor = models.ForeignKey( MissionSensor ) # e.g. HRV
    operator_abbreviation = models.CharField( max_length=255 ) # UI abbreviation
    class Meta:
        app_label= 'catalogue'
        unique_together = ('mission_sensor', 'abbreviation')
    def __unicode__(self):
        return "%s:%s" % (self.mission_sensor.operator_abbreviation, self.name)

###############################################################################


class AcquisitionMode(models.Model):
    """Acquisition mode / camera number e.g. CAM1
       @note: Moved notes below and above from SensorType class to here on 2 June 2010
              as they were mixed up
       @todo refactor resoltion, band count is grayscale up to type
    """
    sensor_type = models.ForeignKey(SensorType)  # e.g. M
    abbreviation = models.CharField(max_length="4")
    name = models.CharField(max_length="255")
    # TODO: The next three properties must be moved to SensorType based on
    #       discussions between Linda and Tim 22/07/2012
    spatial_resolution = models.IntegerField(
        help_text="Spatial resolution in m")
    band_count = models.IntegerField()
    is_grayscale = models.BooleanField(default=False)
    operator_abbreviation = models.CharField(max_length=255)  # UI abbreviation

    class Meta:
        app_label = 'catalogue'
        unique_together = ('sensor_type', 'abbreviation')

    def __unicode__(self):
        return "%s:%s" % (self.sensor_type.mission_sensor.operator_abbreviation,
            self.name)


###############################################################################

class ProcessingLevel( models.Model ):
    """Processing level e.g. L3Aa"""
    abbreviation = models.CharField( max_length="4", unique=True )
    name = models.CharField( max_length="255" )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label= 'catalogue'
        verbose_name = 'Processing Level'
        verbose_name_plural = 'Processing Levels'

    class Admin:
        pass


###############################################################################

class Projection( models.Model ):
    epsg_code = models.IntegerField(unique=True)
    name = models.CharField('Name', max_length=128, db_index=True, unique=True)

    def __unicode__(self):
        return "EPSG:" + str( self.epsg_code ) + " " + self.name

    class Meta:
        app_label= 'catalogue'
        verbose_name = 'Projection'
        verbose_name_plural = 'Projections'
        ordering = ('epsg_code', 'name')


    class Admin:
        pass

###############################################################################
# These models are not used in generating the sac id
###############################################################################

class Institution( models.Model ):
    name = models.CharField( max_length="255", unique=True )
    address1 = models.CharField( max_length="255" )
    address2 = models.CharField( max_length="255" )
    address3 = models.CharField( max_length="255" )
    post_code = models.CharField( max_length="255" )
    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name


###############################################################################

class License( models.Model ):
    """
    Licenses for Products
    """
    LICENSE_TYPE_FREE       = 1
    LICENSE_TYPE_GOVERNMENT = 2
    LICENSE_TYPE_COMMERCIAL = 3

    LICENSE_TYPE_CHOICES = (
        (LICENSE_TYPE_FREE,       'Free'),
        (LICENSE_TYPE_GOVERNMENT, 'Government'),
        (LICENSE_TYPE_COMMERCIAL, 'Commercial'),
      )
    name = models.CharField( max_length="255", unique=True )
    details = models.TextField()
    type = models.IntegerField(choices=LICENSE_TYPE_CHOICES, default=LICENSE_TYPE_COMMERCIAL)

    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name


###############################################################################

class Quality( models.Model ):
    name = models.CharField( max_length="255" , unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        app_label= 'catalogue'
        verbose_name = 'Quality'
        verbose_name_plural = 'Qualities'

###############################################################################

class CreatingSoftware( models.Model ):
    name = models.CharField( max_length="255", unique=True )
    version = models.CharField( max_length="100" )
    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name

###############################################################################

class Topic( models.Model ):
    """A dictionary to define geospatial dataset topics e.g. LANDUSE, ROADS etc."""
    abbreviation = models.CharField( max_length="10", unique=True, null=False )
    name = models.CharField( max_length="255", unique=True, null=False )
    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name

###############################################################################

class PlaceType( models.Model ):
    """A dictionary to define place types e.g. Global, Continent, Region, Country, Province, City etc."""
    name = models.CharField( max_length="255", unique=True, null=False )
    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name

###############################################################################

class Place( models.Model ):
    """A collection on named places based largely on geonames (which all get a place type of Nearest named place)"""
    name = models.CharField( max_length="255", null=False )
    place_type = models.ForeignKey( PlaceType, help_text="Type of place" )
    geometry  = models.PointField( srid=4326, help_text="Place geometry", null=False )
    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name
    objects = models.GeoManager()

###############################################################################

class Unit( models.Model ):
    """A dictionary to define unit types e.g. m, km etc."""
    abbreviation = models.CharField( max_length="10", unique=True, null=False )
    name = models.CharField( max_length="255", unique=True, null=False )
    class Meta:
        app_label= 'catalogue'
    def __unicode__(self):
        return self.name
