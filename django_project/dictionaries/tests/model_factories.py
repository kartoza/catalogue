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
    Collection, ProcessingLevel, Satellite, ScannerType, InstrumentType,
    ReferenceSystem, RadarBeam, ImagingMode, SatelliteInstrumentGroup,
    SatelliteInstrument, Band, SpectralGroup, SpectralMode, BandSpectralMode
)


class CollectionF(factory.django.DjangoModelFactory):
    """
    Collection model factory
    """
    FACTORY_FOR = Collection

    name = factory.Sequence(lambda n: 'Collection {0}'.format(n))
    description = 'None'
    institution = factory.SubFactory(
        'catalogue.tests.model_factories.InstitutionF'
    )


class ProcessingLevelF(factory.django.DjangoModelFactory):
    """
    Processing level factory
    """
    FACTORY_FOR = ProcessingLevel

    abbreviation = factory.Sequence(lambda n: 'AB{0}'.format(n))
    name = factory.Sequence(lambda n: 'Processing level {0}'.format(n))
    description = factory.Sequence(
        lambda n: 'Description of processing level {0}'.format(n))


class SatelliteF(factory.django.DjangoModelFactory):
    """
    Satellite factory
    """
    FACTORY_FOR = Satellite

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
    revist_time_days = 0
    reference_url = ''
    license_type = factory.SubFactory(
        'catalogue.tests.model_factories.LicenseF'
    )


class ScannerTypeF(factory.django.DjangoModelFactory):
    """
    ScannerType factory
    """
    FACTORY_FOR = ScannerType

    name = factory.Sequence(lambda n: 'ScannerType {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'ScanTypeABBR {0}'.format(n))


class ReferenceSystemF(factory.django.DjangoModelFactory):
    """
    ReferenceSystem factory
    """
    FACTORY_FOR = ReferenceSystem

    name = factory.Sequence(lambda n: 'ReferenceSystem {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'RefSys {0}'.format(n))


class InstrumentTypeF(factory.django.DjangoModelFactory):
    """
    InstrumentType factory
    """
    FACTORY_FOR = InstrumentType

    name = factory.Sequence(lambda n: 'InstrumentType {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'InsType {0}'.format(n))
    operator_abbreviation = factory.Sequence(
        lambda n: 'OperatorAbbr {0}'.format(n))
    is_radar = False
    is_taskable = False
    scanner_type = factory.SubFactory(ScannerTypeF)
    base_processing_level = factory.SubFactory(ProcessingLevelF)
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
    FACTORY_FOR = RadarBeam

    instrument_type = factory.SubFactory(InstrumentTypeF)
    band_name = factory.Sequence(lambda n: 'Band name {0}'.format(n))
    wavelength_cm = 0
    looking_distance = ''
    azimuth_direction = ''


class ImagingModeF(factory.django.DjangoModelFactory):
    """
    ImagingMode factory
    """
    FACTORY_FOR = ImagingMode

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
    FACTORY_FOR = SatelliteInstrumentGroup

    satellite = factory.SubFactory(SatelliteF)
    instrument_type = factory.SubFactory(InstrumentTypeF)


class SatelliteInstrumentF(factory.django.DjangoModelFactory):
    """
    SatelliteInstrument factory
    """
    FACTORY_FOR = SatelliteInstrument

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
    FACTORY_FOR = Band

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
    FACTORY_FOR = SpectralGroup

    name = factory.Sequence(lambda n: 'SpectralGroup {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'SG {0}'.format(n))


class SpectralModeF(factory.django.DjangoModelFactory):
    """
    SpectralMode factory
    """
    FACTORY_FOR = SpectralMode

    name = factory.Sequence(lambda n: 'SpectralMode {0}'.format(n))
    description = ''
    abbreviation = factory.Sequence(lambda n: 'SM {0}'.format(n))
    instrument_type = factory.SubFactory(InstrumentTypeF)
    spectralgroup = factory.SubFactory(SpectralGroupF)


class BandSpectralModeF(factory.django.DjangoModelFactory):
    """
    BandSpectralMode factory
    """
    FACTORY_FOR = BandSpectralMode

    band = factory.SubFactory(BandF)
    spectral_mode = factory.SubFactory(SpectralModeF)