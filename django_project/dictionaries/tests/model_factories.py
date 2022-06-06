"""
SANSA-EO Catalogue - Dictionary model factories

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '16/07/2013'
__copyright__ = 'South African National Space Agency'

import factory

from ..models import (
    Collection,
    ProcessingLevel,
    Satellite,
    ScannerType,
    InstrumentType,
    ReferenceSystem,
    RadarBeam,
    ImagingMode,
    SatelliteInstrumentGroup,
    SatelliteInstrument,
    Band,
    SpectralGroup,
    SpectralMode,
    BandSpectralMode,
    InstrumentTypeProcessingLevel,
    SpectralModeProcessingCosts,
    Institution,
    RadarProductProfile,
    OpticalProductProfile,
    Projection,
    License,
    Quality,
    Topic,
    PlaceType,
    Place,
    Unit,
    SalesRegion,
    SubsidyType,
    ProductProcessState
)


class CollectionF(factory.django.DjangoModelFactory):
    """
    Collection model factory
    """
    class Meta:
        model = Collection

    name = factory.Sequence(lambda n: 'Collection {0}'.format(n))
    description = 'None'
    institution = factory.SubFactory(
        'dictionaries.tests.model_factories.InstitutionF'
    )


class ProcessingLevelF(factory.django.DjangoModelFactory):
    """
    Processing level factory
    """
    class Meta:
        model = ProcessingLevel

    abbreviation = factory.Sequence(lambda n: 'A{0}'.format(n))
    name = factory.Sequence(lambda n: 'Processing level {0}'.format(n))
    description = factory.Sequence(
        lambda n: 'Description of processing level {0}'.format(n))


class SatelliteF(factory.django.DjangoModelFactory):
    """
    Satellite factory
    """
    class Meta:
        model = Satellite

    name = factory.Sequence(lambda n: 'Satellite {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'SatABBR {0}'.format(n))
    operator_abbreviation = factory.Sequence(
        lambda n: 'SAT Operator ABBR {0}'.format(n))
    collection = factory.SubFactory(CollectionF)
    launch_date = None
    status = None
    altitude_km = 0
    orbit = ''
    revisit_time_days = 0
    reference_url = ''
    license_type = factory.SubFactory(
        'dictionaries.tests.model_factories.LicenseF'
    )


class ScannerTypeF(factory.django.DjangoModelFactory):
    """
    ScannerType factory
    """
    class Meta:
        model = ScannerType

    name = factory.Sequence(lambda n: 'ScannerType {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'ScanTypeABBR {0}'.format(n))


class ReferenceSystemF(factory.django.DjangoModelFactory):
    """
    ReferenceSystem factory
    """
    class Meta:
        model = ReferenceSystem

    name = factory.Sequence(lambda n: 'ReferenceSystem {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'RefSys {0}'.format(n))


class InstrumentTypeF(factory.django.DjangoModelFactory):
    """
    InstrumentType factory
    """
    class Meta:
        model = InstrumentType

    name = factory.Sequence(lambda n: 'InstrumentType {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'InsType {0}'.format(n))
    operator_abbreviation = factory.Sequence(
        lambda n: 'OperatorAbbr {0}'.format(n))
    is_radar = False
    is_taskable = False
    is_searchable = True
    scanner_type = factory.SubFactory(ScannerTypeF)
    base_processing_level = factory.SubFactory(ProcessingLevelF)
    default_processing_level = factory.SubFactory(ProcessingLevelF)
    reference_system = factory.SubFactory(ReferenceSystemF)
    swath_optical_km = 0
    band_count = 0
    band_type = ''
    spectral_range_list_nm = ''
    pixel_size_list_m = ''
    spatial_resolution_range = ''
    quantization_bits = 0
    image_size_km = 0
    processing_software = ''
    keywords = ''


class RadarBeamF(factory.django.DjangoModelFactory):
    """
    RadarBeam factory
    """
    class Meta:
        model = RadarBeam

    instrument_type = factory.SubFactory(InstrumentTypeF)
    band_name = factory.Sequence(lambda n: 'Band name {0}'.format(n))
    wavelength_cm = 0
    looking_distance = ''
    azimuth_direction = ''


class ImagingModeF(factory.django.DjangoModelFactory):
    """
    ImagingMode factory
    """
    class Meta:
        model = ImagingMode

    radarbeam = factory.SubFactory(RadarBeamF)
    name = factory.Sequence(lambda n: 'ImagingMode {0}'.format(n))
    incidence_angle_min = 0.0
    incidence_angle_max = 0.0
    approximate_resolution_m = 0.0
    swath_width_km = 0.0
    number_of_looks = 0
    polarization = factory.Iterator(
        ImagingMode.POLARIZATION_SET, getter=lambda c: c[0])


class SatelliteInstrumentGroupF(factory.django.DjangoModelFactory):
    """
    SatelliteInstrumentGroup factory
    """
    class Meta:
        model = SatelliteInstrumentGroup

    satellite = factory.SubFactory(SatelliteF)
    instrument_type = factory.SubFactory(InstrumentTypeF)


class SatelliteInstrumentF(factory.django.DjangoModelFactory):
    """
    SatelliteInstrument factory
    """
    class Meta:
        model = SatelliteInstrument

    name = factory.Sequence(lambda n: 'SatelliteInstrument {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'STINS {0}'.format(n))
    operator_abbreviation = factory.Sequence(
        lambda n: 'OPSATINST {0}'.format(n))
    satellite_instrument_group = factory.SubFactory(SatelliteInstrumentGroupF)


class BandF(factory.django.DjangoModelFactory):
    """
    Band factory
    """
    class Meta:
        model = Band

    instrument_type = factory.SubFactory(InstrumentTypeF)
    band_name = factory.Sequence(lambda n: 'Band {0}'.format(n))
    band_abbr = ''
    band_number = 0
    min_wavelength_nm = 0
    max_wavelength_nm = 0
    pixelsize_resampled_m = 0
    pixelsize_acquired_m = 0


class SpectralGroupF(factory.django.DjangoModelFactory):
    """
    SpectralGroup factory
    """
    class Meta:
        model = SpectralGroup

    name = factory.Sequence(lambda n: 'SpectralGroup {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'SG {0}'.format(n))


class SpectralModeF(factory.django.DjangoModelFactory):
    """
    SpectralMode factory
    """
    class Meta:
        model = SpectralMode

    name = factory.Sequence(lambda n: 'SpectralMode {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'SM {0}'.format(n))
    instrument_type = factory.SubFactory(InstrumentTypeF)
    spectralgroup = factory.SubFactory(SpectralGroupF)


class BandSpectralModeF(factory.django.DjangoModelFactory):
    """
    BandSpectralMode factory
    """
    class Meta:
        model = BandSpectralMode

    band = factory.SubFactory(BandF)
    spectral_mode = factory.SubFactory(SpectralModeF)


class InstrumentTypeProcessingLevelF(factory.django.DjangoModelFactory):
    """
    InstrumentTypeProcessingLevel factory
    """
    class Meta:
        model = InstrumentTypeProcessingLevel

    instrument_type = factory.SubFactory(InstrumentTypeF)
    processing_level = factory.SubFactory(ProcessingLevelF)
    operator_processing_level_name = ''
    operator_processing_level_abbreviation = ''


class SpectralModeProcessingCostsF(factory.django.DjangoModelFactory):
    """
    SpectralModeProcessingCosts factory
    """
    class Meta:
        model = SpectralModeProcessingCosts

    spectral_mode = factory.SubFactory(SpectralModeF)
    instrument_type_processing_level = factory.SubFactory(
        InstrumentTypeProcessingLevelF)
    cost_per_scene = 0.0
    currency = factory.SubFactory('order.model_factories.CurrencyF')
    cost_per_square_km = 0.0
    minimum_square_km = 0.0


class RadarProductProfileF(factory.django.DjangoModelFactory):
    """
    RadarProductProfile factory
    """
    class Meta:
        model = RadarProductProfile

    satellite_instrument = factory.SubFactory(SatelliteInstrumentF)
    imaging_mode = factory.SubFactory(ImagingModeF)


class OpticalProductProfileF(factory.django.DjangoModelFactory):
    """
    OpticalProductProfile factory
    """
    class Meta:
        model = OpticalProductProfile

    satellite_instrument = factory.SubFactory(SatelliteInstrumentF)
    spectral_mode = factory.SubFactory(SpectralModeF)


class ProjectionF(factory.django.DjangoModelFactory):
    """
    Projection model factory
    """
    class Meta:
        model = Projection

    name = factory.Sequence(lambda n: "Projection {}".format(n))
    epsg_code = factory.Sequence(lambda n: n)


class InstitutionF(factory.django.DjangoModelFactory):
    """
    Institution model factory
    """
    class Meta:
        model = Institution

    name = factory.Sequence(lambda n: 'Institution {0}'.format(n))
    address1 = 'Blank'
    address2 = 'Blank'
    address3 = 'Blank'
    post_code = 'Blank'


class LicenseF(factory.django.DjangoModelFactory):
    """
    License model factory
    """
    class Meta:
        model = License

    name = factory.Sequence(lambda n: 'License {0}'.format(n))
    details = ''
    type = factory.Iterator(
        License.LICENSE_TYPE_CHOICES, getter=lambda c: c[0])


class QualityF(factory.django.DjangoModelFactory):
    """
    Quality model factory
    """
    class Meta:
        model = Quality

    name = factory.Sequence(lambda n: "Quality {}".format(n))


class TopicF(factory.django.DjangoModelFactory):
    """
    Topic model factory
    """
    class Meta:
        model = Topic

    abbreviation = factory.Sequence(lambda n: "T{}".format(n))
    name = factory.Sequence(lambda n: "Topic {}".format(n))


class PlaceTypeF(factory.django.DjangoModelFactory):
    """
    PlaceType model factory
    """
    class Meta:
        model = PlaceType

    name = factory.Sequence(lambda n: "PlaceType {}".format(n))


class PlaceF(factory.django.DjangoModelFactory):
    """
    Place model factory
    """
    class Meta:
        model = Place

    name = factory.Sequence(lambda n: "Place {}".format(n))
    place_type = factory.SubFactory(
        'dictionaries.tests.model_factories.PlaceTypeF')
    geometry = 'POINT(17.54 -32.05)'


class UnitF(factory.django.DjangoModelFactory):
    """
    Unit model factory
    """
    class Meta:
        model = Unit

    abbreviation = factory.Sequence(lambda n: "U{}".format(n))
    name = factory.Sequence(lambda n: "Unit {}".format(n))


class SalesRegionF(factory.django.DjangoModelFactory):
    """
    SalesRegion model factory
    """
    class Meta:
        model = SalesRegion

    name = factory.Sequence(lambda n: "SalesRegion {}".format(n))
    abbreviation = factory.Sequence(lambda n: "SR{}".format(n))


class SubsidyTypeF(factory.django.DjangoModelFactory):
    """
    SubsidyType model factory
    """
    class Meta:
        model = SubsidyType

    name = factory.Sequence(lambda n: "SubsidyType {}".format(n))
    abbreviation = factory.Sequence(lambda n: "ST{}".format(n))


class ProductProcessStateF(factory.django.DjangoModelFactory):
    """
    ProductProcessState model factory
    """
    class Meta:
        model = ProductProcessState

    name = factory.Sequence(lambda n: "ProductProcessState {}".format(n))
