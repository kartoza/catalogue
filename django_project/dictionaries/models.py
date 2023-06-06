# coding=utf-8
"""
SANSA-EO Catalogue - Ancillary Dictionary models

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__date__ = '01/11/2012'
__copyright__ = 'South African National Space Agency'

from django.db.models.query import QuerySet

from django.contrib.gis.db import models
from catalogue.dbhelpers import executeRAWSQL
from exchange.models import Currency


class OpticalProductProfileQuerySet(QuerySet):
    """
    Optical Product Profile extended query manager

    for_instrumenttypes - filters product profile by instrument types

    """

    def for_licence_type(self, theLicenceType):
        return self.filter(
            satellite_instrument__satellite_instrument_group__satellite__license_type__in=
            theLicenceType.all())

    def for_collection(self, theCollection):
        return self.filter(
            satellite_instrument__satellite_instrument_group__satellite__collection__in=
            theCollection.all()
        )

    def for_instrumenttypes(self, theInstrumentTypes):
        return self.filter(
            satellite_instrument__satellite_instrument_group__instrument_type__in=theInstrumentTypes.all())

    def for_satellite(self, theSatellite):
        return self.filter(
            satellite_instrument__satellite_instrument_group__satellite__in=theSatellite.all())

    def for_spectralgroup(self, theSpectralgroup):
        return self.filter(
            spectral_mode__spectralgroup__in=theSpectralgroup.all())

    def only_searchable(self):
        return self.filter(
            satellite_instrument__satellite_instrument_group__instrument_type__is_searchable=True
        )


class ReferenceSystem(models.Model):
    """
    Spatial Reference information
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the reference system.')
    abbreviation = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        """Meta class implementation."""
        ordering = ['name']


class Projection(models.Model):
    """
    A dictionary to define Product Projection, e.g. 32737, UTM37S
    """

    epsg_code = models.IntegerField(unique=True)
    name = models.CharField('Name', max_length=128, unique=True)

    def __unicode__(self):
        return 'EPSG: %s %s' % (str(self.epsg_code), self.name)

    def __str__(self):
        return 'EPSG: %s %s' % (str(self.epsg_code), self.name)

    class Meta:
        verbose_name = 'Projection'
        verbose_name_plural = 'Projections'
        ordering = ('epsg_code', 'name')


class Institution(models.Model):
    """
    A dictionary to define Product Institution, e.g. SANSA, ESA
    """

    name = models.CharField(max_length=255, unique=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    address3 = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class License(models.Model):
    """
    Licenses for Products, e.g. SANSA Free License.
    """

    LICENSE_TYPE_FREE = 1
    LICENSE_TYPE_GOVERNMENT = 2
    LICENSE_TYPE_COMMERCIAL = 3

    LICENSE_TYPE_CHOICES = (
        (LICENSE_TYPE_FREE, 'Free'),
        (LICENSE_TYPE_GOVERNMENT, 'Government'),
        (LICENSE_TYPE_COMMERCIAL, 'Commercial'),
    )

    name = models.CharField(max_length=255, unique=True)
    details = models.TextField()
    type = models.IntegerField(
        choices=LICENSE_TYPE_CHOICES, default=LICENSE_TYPE_COMMERCIAL)

    def __unicode__(self):
        return self.name


class Quality(models.Model):
    """
    A dictionary to define Product Quality, e.g. Unknown
    """

    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Quality'
        verbose_name_plural = 'Qualities'


class Topic(models.Model):
    """
    A dictionary to define geospatial dataset topics e.g. LANDUSE, ROADS etc.
    """

    abbreviation = models.CharField(max_length=10, unique=True, null=False)
    name = models.CharField(max_length=255, unique=True, null=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class PlaceType(models.Model):
    """
    A dictionary to define place types e.g. Global, Continent, Region,
    Country, Province, City etc.
    """

    name = models.CharField(max_length=255, unique=True, null=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Place(models.Model):
    """
    A collection on named places based largely on geonames (which all get a
    place type of Nearest named place)
    """

    name = models.CharField(max_length=255, null=False)
    place_type = models.ForeignKey(
        PlaceType,
        help_text='Type of place',
        on_delete=models.CASCADE
    )
    geometry = models.PointField(
        srid=4326, help_text='Place geometry', null=False)

    objects = models.Manager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    A dictionary to define unit types e.g. m, km etc.
    """

    abbreviation = models.CharField(max_length=10, unique=True, null=False)
    name = models.CharField(max_length=255, unique=True, null=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SalesRegion(models.Model):
    """
    A dictionary for sales region information
    """
    name = models.CharField(
        max_length=50, help_text='Full name of a sales region')
    abbreviation = models.CharField(max_length=4)

    def __unicode__(self):
        return self.abbreviation

    def __str__(self):
        return self.abbreviation


class SubsidyType(models.Model):
    """
    A dictionary for subsidy types
    """
    name = models.CharField(
        max_length=50, help_text='Full name of a subsidy type')
    abbreviation = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Collection(models.Model):
    """Collection of satellites managed by a single operator."""

    name = models.CharField(
        max_length=255, unique=True,
        verbose_name='Collection name',
        help_text='Collection name as defined by operator.')
    description = models.TextField(
        verbose_name='Collection description',
        help_text='Detailed description for this collection')
    institution = models.ForeignKey(
        # NOTE: when referencing models in another application we need ti
        # specify a model with the full application label
        'Institution',
        on_delete=models.CASCADE,
        help_text='Organisation that owns this satellite collection.')

    def __unicode__(self):
        return self.name

    class Meta:
        """Meta class implementation."""
        ordering = ['name']


class Satellite(models.Model):
    """Satellite e.g. SPOT5 - a real satellite in the sky."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the satellite.')
    abbreviation = models.CharField(max_length=20, unique=True)
    operator_abbreviation = models.CharField(
        max_length=255, unique=True,
        help_text=(
            'Satellite abbreviation as named by satellite owning institution.'
        )
    )
    # image = models.ImageField()
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE
    )
    launch_date = models.DateField(
        blank=True, null=True,
        help_text='Satellite launch date')
    status = models.TextField(
        blank=True, null=True,
        help_text='Information about satellite operational status')
    altitude_km = models.IntegerField(
        blank=True, null=True,
        help_text='Satellite altitude in kilometres')
    orbit = models.TextField(
        blank=True, null=True,
        help_text='Satellite orbit description')
    revisit_time_days = models.IntegerField(
        blank=True, null=True,
        help_text='Days elapsed between observations of the same point')
    reference_url = models.URLField(
        blank=True, null=True,
        help_text='Satellite mission URL')
    license_type = models.ForeignKey(
        License,
        on_delete=models.CASCADE,
        help_text='Satellite product license type'
    )

    def __unicode__(self):
        """Return 'operator_abbreviation' as model representation."""
        return '{0}'.format(self.operator_abbreviation)

    def __str__(self):
        return '{0}'.format(self.operator_abbreviation)

    class Meta:
        """Meta class implementation."""
        ordering = ['name']


class ScannerType(models.Model):
    """Scanner type for the instrument type e.g. Pushbroom"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the scanner type.')
    abbreviation = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.abbreviation

    def __str__(self):
        return self.abbreviation

    class Meta:
        """Meta class implementation."""
        ordering = ['name']


class ProcessingLevel(models.Model):
    """
    Available ProcessingLevels, e.g. L1, L1A, ...

    NOTE: This model has the same *name* as one used in old dictionary
    implementation, we need to be careful when switching over to new_dicts
    """
    abbreviation = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the processing level.')

    def __unicode__(self):
        return '{0} {1}'.format(self.abbreviation, self.name)

    def __str__(self):
        return self.abbreviation

    class Meta:
        """Meta class implementation."""
        ordering = ['abbreviation']


class InstrumentType(models.Model):
    """Instrument - a type of sensor on the mission or satellite - e.g. HRV."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the instrument type.')
    abbreviation = models.CharField(max_length=20, unique=True)
    operator_abbreviation = models.CharField(
        max_length=255, unique=True,
        help_text=(
            'Instrument abbreviation as named by satellite owning institution'
            '.'))
    is_radar = models.BooleanField(
        verbose_name='Is this a RADAR sensor?',
        help_text='Mark true if this sensor captures RADAR data.',
        default=False
    )
    is_taskable = models.BooleanField(
        default=False,
        help_text='Can this sensor be tasked?'
    )
    is_searchable = models.BooleanField(
        default=True,
        help_text='Can this sensor be searched?'
    )
    scanner_type = models.ForeignKey(
        ScannerType,
        on_delete=models.CASCADE
    )
    base_processing_level = models.ForeignKey(
        ProcessingLevel,
        blank=True,
        null=True,
        related_name='base_processing_level',
        help_text=('Processing level as provided by the ground station as '
                   '"raw data".'),
        on_delete=models.CASCADE
    )
    default_processing_level = models.ForeignKey(
        ProcessingLevel,
        blank=True, null=True,
        related_name='default_processing_level',
        help_text=('Default processing level that will be supplied to '
                   'customers.'),
        on_delete=models.CASCADE
    )
    reference_system = models.ForeignKey(
        ReferenceSystem,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    swath_optical_km = models.IntegerField(
        blank=True, null=True,
        help_text='On-ground sensor swath width')
    band_count = models.IntegerField(
        blank=True, null=True,
        help_text='Total number of bands for this Instrument')
    band_type = models.TextField(
        blank=True, null=True,
        help_text='Semicolon delimited list of Instrument band types')
    spectral_range_list_nm = models.CharField(
        blank=True, null=True,
        max_length=100,
        help_text='Semicolon delimited list of Instrument spectral ranges')
    pixel_size_list_m = models.CharField(
        blank=True, null=True,
        max_length=100,
        help_text='Semicolon delimited list of Instrument pixel sizes')
    spatial_resolution_range = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Semicolon delimited list of Instrument spatial resolutions')
    quantization_bits = models.IntegerField(
        blank=True, null=True,
        help_text=(
            'Quantization bit rate - the aquisition bits per pixel for '
            'example 12 bit landsat 8. Note that products are likely '
            'delivered with a different bit depth to customers.'))
    image_size_km = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Human readable representation of image size')
    processing_software = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Description of processing software')
    keywords = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Keywords describing InstrumentType')

    def __unicode__(self):
        return self.operator_abbreviation

    def __str__(self):
        return self.operator_abbreviation

    class Meta:
        """Meta class implementation."""
        ordering = ['name']


class RadarBeam(models.Model):
    """
    Only for Radar products
    """
    instrument_type = models.OneToOneField(
        InstrumentType,
        on_delete=models.CASCADE
    )
    band_name = models.CharField(
        max_length=50,
        help_text='RadarBeam band name'
    )
    wavelength_cm = models.IntegerField(
        help_text='Band wavelength in centimetres')
    looking_distance = models.CharField(
        max_length=50,
        help_text='REPLACE ME!'
    )
    azimuth_direction = models.CharField(
        max_length=50,
        help_text='REPLACE ME!'
    )

    def __unicode__(self):
        return '{0} ({1})'.format(self.band_name, self.wavelength_cm)

    def __str__(self):
        return '{0} ({1})'.format(self.band_name, self.wavelength_cm)

    class Meta:
        """Meta class implementation."""
        ordering = ['instrument_type']


class ImagingMode(models.Model):
    """
    Imaging mode for a radar beam
    """
    POLARIZATION_SET = (
        ('HH', 'Horizontal-Horizontal'),
        ('HV', 'Horizontal-Vertical'),
        ('VH', 'Vertical-Horizontal'),
        ('VV', 'Vertical-Vertical'),
    )
    radarbeam = models.ForeignKey(
        RadarBeam,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=50,
        help_text='ImagingMode name'
    )
    incidence_angle_min = models.FloatField(
        help_text='Minimum incidence angle'
    )
    incidence_angle_max = models.FloatField(
        help_text='Maximum incidence angle'
    )
    approximate_resolution_m = models.FloatField(
        help_text='Approximate ImagingMode resolution in meters'
    )
    swath_width_km = models.FloatField(
        help_text='Swath width in kilometres'
    )
    number_of_looks = models.IntegerField(
        help_text='REPLACE ME!'
    )
    polarization = models.CharField(
        max_length=2, choices=POLARIZATION_SET,
        help_text='Polarization type'
    )

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.polarization)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.polarization)

    class Meta:
        """Meta class implementation."""
        ordering = ['name']


class SatelliteInstrumentGroup(models.Model):
    """Satellite instrument group - an instrument as deployed on a satellite.

    It may be the case that an instrument type can be both on multiple
    satellites and deployed multiple times on a single satellite. This model
    caters for the latter case by allowing a one to many relationship between
    instrument group and satellite instrument.

    Example::

        SELECT
          dictionaries_instrumenttype.name,
          dictionaries_satellite.name,
          dictionaries_satelliteinstrumentgroup.id,
          dictionaries_satelliteinstrumentgroup.satellite_id,
          dictionaries_satelliteinstrumentgroup.instrument_type_id,
          dictionaries_satelliteinstrument.name,
          dictionaries_satelliteinstrument.description,
          dictionaries_satelliteinstrument.abbreviation,
          dictionaries_satelliteinstrument.operator_abbreviation
        FROM
          public.dictionaries_satelliteinstrumentgroup,
          public.dictionaries_satellite,
          public.dictionaries_instrumenttype,
          public.dictionaries_satelliteinstrument
        WHERE
          dictionaries_satelliteinstrumentgroup.satellite_id =
          dictionaries_satellite.id AND
          dictionaries_satelliteinstrumentgroup.instrument_type_id =
          dictionaries_instrumenttype.id AND
          dictionaries_satelliteinstrument.satellite_instrument_group_id =
          dictionaries_satelliteinstrumentgroup.id
        ORDER BY
          dictionaries_satellite.name;

    Would produce::

        "HRV";"SPOT 1";15;8;6;"SPOT 1 HRV 2";"HRV Camera 2 on the SPOT 1
            Satellite";"S1-HRV2";"S1-HRV2"
        "HRV";"SPOT 1";15;8;6;"SPOT 1 HRV 1";"HRV Camera 1 on the SPOT 1
            Satellite";"S1-HRV1";"S1-HRV1"
        "HRV";"SPOT 2";8;9;6;"SPOT 2 HRV 1";"HRV Camera 1 on the SPOT 2
            Satellite";"S2-HRV1";"S2-HRV1"
        "HRV";"SPOT 2";8;9;6;"SPOT 2 HRV 2";"HRV Camera 2 on the SPOT 2
            Satellite";"S2-HRV2";"S2-HRV2"

    In the example output above you can see for example that there is an HRV
    camera deployed twice on SPOT 1 and twice on SPOT 2.

    """
    satellite = models.ForeignKey(
        Satellite,
        on_delete=models.CASCADE
    )
    instrument_type = models.ForeignKey(
        InstrumentType,
        on_delete=models.CASCADE
        )
    is_searchable = models.BooleanField(default=True)
    start_date = models.DateField(
        blank=True, null=True,
        help_text='The beginning date to hide the data from the user in the search page')
    end_date = models.DateField(
        blank=True, null=True,
        help_text = 'The end date to hide the data from the user in the search page')

    class Meta:
        unique_together = (
            'satellite',
            'instrument_type'
        )
        ordering = ['satellite', 'instrument_type']

    def __unicode__(self):
        return '{0} - {1}'.format(
            self.satellite.operator_abbreviation,
            self.instrument_type.operator_abbreviation
        )

    def __str__(self):
        return '{0} - {1}'.format(
            self.satellite.operator_abbreviation,
            self.instrument_type.operator_abbreviation
        )

    def min_year(self):
        return self.products_per_year()[0]['year']

    def max_year(self):
        return self.products_per_year()[-1]['year']

    def products_per_year(self):
        myStats = executeRAWSQL("""
SELECT count(*) as count, extract(YEAR from gp.product_date)::int as year
FROM
  catalogue_genericproduct gp, catalogue_genericimageryproduct gip,
  catalogue_genericsensorproduct gsp, catalogue_opticalproduct op,
  dictionaries_opticalproductprofile opp, dictionaries_satelliteinstrument si
WHERE
  gip.genericproduct_ptr_id = gp.id AND
  gsp.genericimageryproduct_ptr_id = gip.genericproduct_ptr_id AND
  op.genericsensorproduct_ptr_id = gsp.genericimageryproduct_ptr_id AND
  opp.id = op.product_profile_id AND opp.satellite_instrument_id = si.id
  AND si.satellite_instrument_group_id=%(sensor_pk)s
GROUP BY extract(YEAR from gp.product_date)
ORDER BY year ASC;""", {'sensor_pk': self.pk})
        return myStats


class SatelliteInstrument(models.Model):
    """Satellite instrument - a specific instrument as deployed on a satellite.
    Note that there may be more than one instrument of the same type per
    satellite e.g. SPOT 5 HRG (camera 1 and 2).
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the satellite instrument.')
    abbreviation = models.CharField(max_length=20, unique=True)
    operator_abbreviation = models.CharField(
        max_length=255, unique=True,
        help_text=('Satellite abbreviation as named by satellite owning '
                   'institution.'))
    satellite_instrument_group = models.ForeignKey(
        SatelliteInstrumentGroup,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        """Return 'operator_abbreviation' as model representation."""
        return '{0}'.format(self.operator_abbreviation)

    def __str__(self):
        """Return 'operator_abbreviation' as model representation."""
        return '{0}'.format(self.operator_abbreviation)

    class Meta:
        """Meta class implementation."""
        ordering = ['name']


class Band(models.Model):
    """Wavelength to bands relation

    Band examples:
        red - 400-484 (wavelength)
    """
    instrument_type = models.ForeignKey(
        InstrumentType,
        on_delete=models.CASCADE
    )
    band_name = models.CharField(max_length=50)
    band_abbr = models.CharField(max_length=20, blank=True)
    band_number = models.IntegerField(
        help_text='Instrument specific band number, e.g. 1,2, ...')
    min_wavelength_nm = models.IntegerField(
        help_text='Lower band wavelength in nanometeres')
    max_wavelength_nm = models.IntegerField(
        help_text='Upper band wavelength in nanometeres')
    pixelsize_resampled_m = models.FloatField(
        help_text='Pixel size in m (resolution) resampled')
    pixelsize_acquired_m = models.FloatField(
        help_text='Pixel size in m (resolution) acquired')

    def __unicode__(self):
        return '{0} ({1} {2}) {3}'.format(
            self.band_name, self.min_wavelength_nm,
            self.max_wavelength_nm,
            self.pixelsize_resampled_m
        )

    def __str__(self):
        return '{0} ({1} {2}) {3}'.format(
            self.band_name, self.min_wavelength_nm,
            self.max_wavelength_nm,
            self.pixelsize_resampled_m
        )

    class Meta:
        """Meta class implementation."""
        ordering = ['instrument_type', 'band_name']


class SpectralGroup(models.Model):
    """A generic named spectral mode that describes spectral grouping.
    e.g Panchromatic, Multispectral, Thermal, Hyperspectral.

    Mode examples:
         J = Multispectral 10m
         P/M = Panchromatic 10m
         A/B = Panchromatic 5m
         T = Panchromatic 2.5m
         X = Multispectral 20m
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the spectral mode.')
    abbreviation = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        """Meta class implementation."""
        ordering = ['abbreviation', 'name']


class SpectralMode(models.Model):
    """
    A specific spectral mode for of an instrument type
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the spectral mode.')
    abbreviation = models.CharField(max_length=20)
    instrument_type = models.ForeignKey(
        InstrumentType,
        on_delete=models.CASCADE
    )
    spectralgroup = models.ForeignKey(
        SpectralGroup,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return '{0} - {1}'.format(self.name, self.instrument_type.name)

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.instrument_type.name)

    class Meta:
        """Meta class implementation."""
        ordering = ['abbreviation', 'name']


class BandSpectralMode(models.Model):
    """
    Band to SpectralMode relation
    """
    band = models.ForeignKey(
        Band,
        on_delete=models.CASCADE
    )
    spectral_mode = models.ForeignKey(
        SpectralMode,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (('band', 'spectral_mode'),)
        ordering = ['band', 'spectral_mode']

    def __unicode__(self):
        return '{0} ({1})'.format(
            self.band.band_name, self.spectral_mode.name)

    def __str__(self):
        return '{0} ({1})'.format(
            self.band.band_name, self.spectral_mode.name)


class InstrumentTypeProcessingLevel(models.Model):
    """
    Relation between ProcessingLevel and InstrumentType
    """
    instrument_type = models.ForeignKey(
        InstrumentType,
        on_delete=models.CASCADE
    )
    processing_level = models.ForeignKey(
        ProcessingLevel,
        on_delete=models.CASCADE
    )
    operator_processing_level_name = models.CharField(
        max_length=50,
        help_text='Operator original processing level name'
    )
    operator_processing_level_abbreviation = models.CharField(
        max_length=4,
        help_text='Operator original processing level abbreviation'
    )

    def __unicode__(self):
        return '{0} - {1}'.format(
            self.instrument_type.name, self.processing_level.abbreviation)

    def __str__(self):
        return '{0} - {1}'.format(
            self.instrument_type.name, self.processing_level.abbreviation)

    class Meta:
        """Meta class implementation."""
        ordering = ['instrument_type', 'processing_level']


class SpectralModeProcessingCosts(models.Model):
    """
    Processing costs for specific processing level per spectral mode
    """
    spectral_mode = models.ForeignKey(
        SpectralMode,
        on_delete=models.CASCADE
    )
    instrument_type_processing_level = models.ForeignKey(
        InstrumentTypeProcessingLevel,
        on_delete=models.CASCADE
    )
    cost_per_scene = models.DecimalField(
        help_text='Cost per scene', max_digits=10, decimal_places=2
    )
    cost_per_square_km = models.DecimalField(
        help_text='Cost per square kilometre',
        null=True, blank=True, max_digits=10, decimal_places=2
    )
    currency = models.ForeignKey(
        Currency,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    minimum_square_km = models.FloatField(
        help_text=(
            'Minimum number of square kilometers that can be ordered for a'
            'price of per kilometer'
        ),
        null=True, blank=True
    )
    sales_region = models.ForeignKey(
        SalesRegion,
        on_delete=models.CASCADE,
        default=1
    )

    def __unicode__(self):
        return '{0} {1} ({2} - {3})'.format(
            self.cost_per_scene,
            self.get_currency().code,
            self.spectral_mode.name, self.instrument_type_processing_level)

    def __str__(self):
        return '{0} {1} ({2} - {3})'.format(
            self.cost_per_scene,
            self.get_currency().code,
            self.spectral_mode.name, self.instrument_type_processing_level)


    def get_currency(self):
        """Handle the case where no currency is specified"""
        if self.currency:
            return self.currency
        else:
            from exchange.models import Currency
            return Currency.objects.get(code='ZAR')

    class Meta:
        """Meta class implementation."""
        ordering = ['spectral_mode', 'instrument_type_processing_level']


class ProductProcessState(models.Model):
    """
    A dictionary for product process states
    """
    name = models.CharField(
        max_length=30, help_text='Full name of a product process state')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class OpticalProductProfile(models.Model):
    """
    An unique product profile for optical sensor based data.

    Consists of:
        * satellite_instrument
        * spectral_mode


    """
    satellite_instrument = models.ForeignKey(
        SatelliteInstrument,
        on_delete=models.CASCADE
    )
    spectral_mode = models.ForeignKey(
        SpectralMode,
        on_delete=models.CASCADE
    )

    # define model passthrough manager
    objects = OpticalProductProfileQuerySet.as_manager()

    def __unicode__(self):
        return '{0} -- {1}'.format(
            self.satellite_instrument,
            self.spectral_mode
        )

    def __str__(self):
        return '{0} -- {1}'.format(
            self.satellite_instrument,
            self.spectral_mode
        )

    class Meta:
        """Meta class implementation."""
        ordering = ['satellite_instrument', 'spectral_mode']

    def baseProcessingLevel(self):
        """Return the InstrumentType.base_processing_level for this profile.

        Args:
            None

        Returns:
            ProcessingLevel: an instance of the ProcessingLevel model
                which represents the base processing level for the instrument
                type.

        Raises:
            None
        """

        return (
            self.satellite_instrument.satellite_instrument_group
                .instrument_type.base_processing_level
        )

    def bandCount(self):
        """Get the band count for this profile.

        Args:
            None

        Returns:
            The number of bands associated with this profile.

        Raises:
            None
        """
        return (
            self.satellite_instrument.satellite_instrument_group
                .instrument_type.band_count
        )

    def owner(self):
        """
        Returns owner institution for this product
        """
        return (
            self.satellite_instrument.satellite_instrument_group.satellite
                .collection.institution
        )


class RadarProductProfile(models.Model):
    """
    An unique product profile for radar sensor based data.

    Consists of:
        * satellite_instrument
        * imaging_mode


    """
    satellite_instrument = models.ForeignKey(
        SatelliteInstrument,
        on_delete=models.CASCADE
    )
    imaging_mode = models.ForeignKey(
        ImagingMode,
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return '{0} -- {1}'.format(
            self.satellite_instrument,
            self.imaging_mode
        )

    def __str__(self):
        return '{0} -- {1}'.format(
            self.satellite_instrument,
            self.imaging_mode
        )

    class Meta:
        """Meta class implementation."""
        ordering = ['satellite_instrument', 'imaging_mode']

