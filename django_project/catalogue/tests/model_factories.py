"""
SANSA-EO Catalogue - Catalogue model factories

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '16/07/2013'
__copyright__ = 'South African National Space Agency'

import factory
from datetime import datetime

from catalogue.models import (
    GenericProduct,
    GenericImageryProduct,
    GenericSensorProduct,
    OpticalProduct, RadarProduct,
    GeospatialProduct, OrdinalProduct,
    ContinuousProduct, Visit, WorldBorders
)


class GenericProductF(factory.django.DjangoModelFactory):
    """
    GenericProduct model factory
    """

    class Meta:
        model = GenericProduct

    product_date = factory.LazyAttribute(lambda d: datetime.now())
    spatial_coverage = (
        'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 '
        '-34.65, 17.54 -32.05))')
    projection = factory.SubFactory(
        'dictionaries.tests.model_factories.ProjectionF')
    quality = factory.SubFactory('dictionaries.tests.model_factories.QualityF')
    unique_product_id = factory.Sequence(
        lambda n: "unique_product_id_{}".format(n))
    original_product_id = factory.Sequence(
        lambda n: "Original_product_id_{}".format(n))
    local_storage_path = ''
    metadata = ''
    remote_thumbnail_url = ''
    ingestion_log = ''


class GenericImageryProductF(GenericProductF):
    """
    GenericImageryProduct model factory
    """

    class Meta:
        model = GenericImageryProduct

    spatial_resolution = 0.0
    spatial_resolution_x = 0.0
    spatial_resolution_y = 0.0
    radiometric_resolution = 0.0
    band_count = 0


class GenericSensorProductF(GenericImageryProductF):
    """
    GenericSensorProduct model factory
    """

    class Meta:
        model = GenericSensorProduct

    product_acquisition_start = datetime(2008, 1, 1, 12, 00)
    product_acquisition_end = datetime(2008, 1, 1, 13, 00)
    geometric_accuracy_mean = 5.0
    geometric_accuracy_1sigma = 2.0
    geometric_accuracy_2sigma = 3.0
    radiometric_signal_to_noise_ratio = 0.0
    radiometric_percentage_error = 0.0
    spectral_accuracy = 20.0
    orbit_number = 1
    path = 123
    path_offset = 0
    row = 321
    row_offset = 0
    offline_storage_medium_id = ''
    online_storage_medium_id = ''


class OpticalProductF(GenericSensorProductF):
    """
    OpticalProduct model factory
    """

    class Meta:
        model = OpticalProduct

    product_profile = factory.SubFactory(
        'dictionaries.tests.model_factories.OpticalProductProfileF')
    cloud_cover = 0
    sensor_inclination_angle = 0.0
    sensor_viewing_angle = 0.0
    gain_name = ''
    gain_value_per_channel = ''
    gain_change_per_channel = ''
    bias_per_channel = ''
    solar_zenith_angle = 0.0
    solar_azimuth_angle = 0.0
    earth_sun_distance = 0.0


class RadarProductF(GenericSensorProductF):
    """
    RadarProduct model factory
    """

    class Meta:
        model = RadarProduct

    product_profile = factory.SubFactory(
        'dictionaries.tests.model_factories.RadarProductProfileF'
    )
    imaging_mode = ''
    look_direction = factory.Iterator(
        RadarProduct.LOOK_DIRECTION_CHOICES, getter=lambda c: c[0])
    antenna_receive_configuration = factory.Iterator(
        RadarProduct.RECEIVE_CONFIGURATION_CHOICES, getter=lambda c: c[0])
    polarising_mode = factory.Iterator(
        RadarProduct.POLARISING_MODE_CHOICES, getter=lambda c: c[0])
    polarising_list = ''
    slant_range_resolution = 0.0
    azimuth_range_resolution = 0.0
    orbit_direction = factory.Iterator(
        RadarProduct.ORBIT_DIRECTION_CHOICES, getter=lambda c: c[0])
    calibration = ''
    incidence_angle = 0.0


class GeospatialProductF(GenericProductF):
    """
    GeospatialProduct model factory
    """

    class Meta:
        model = GeospatialProduct

    name = factory.Sequence(lambda n: "GeospatialProduct {}".format(n))
    description = ''
    processing_notes = ''
    equivalent_scale = 1000000
    data_type = factory.Iterator(
        GeospatialProduct.GEOSPATIAL_GEOMETRY_TYPE_CHOICES,
        getter=lambda c: c[0])
    temporal_extent_start = datetime(2008, 1, 1, 12, 00)
    temporal_extent_end = datetime(2008, 1, 1, 13, 00)
    place_type = factory.SubFactory(
        'dictionaries.tests.model_factories.PlaceTypeF')
    place = factory.SubFactory('dictionaries.tests.model_factories.PlaceF')
    primary_topic = factory.SubFactory(
        'dictionaries.tests.model_factories.TopicF')


class OrdinalProductF(GenericProductF):
    """
    OrdinalProduct model factory
    """

    class Meta:
        model = OrdinalProduct

    class_count = 0
    confusion_matrix = '1,2,3'
    kappa_score = 0.0


class ContinuousProductF(GenericProductF):
    """
    ContinuousProduct model factory
    """

    class Meta:
        model = ContinuousProduct

    range_min = 0.0
    range_max = 0.0
    unit = factory.SubFactory('dictionaries.tests.model_factories.UnitF')


class VisitF(factory.django.DjangoModelFactory):
    """
    Visit model factory
    """

    class Meta:
        model = Visit

    city = ''
    country = ''
    ip_address = '0.0.0.0'
    ip_position = 'POINT(0.0 0.0)'
    user = factory.SubFactory('core.model_factories.UserF')


class WorldBordersF(factory.django.DjangoModelFactory):
    """
    OrderNotificationRecipients model factory
    """

    class Meta:
        model = WorldBorders

    iso2 = 'ZA'
    iso3 = 'ZAF'
    name = 'South Africa'
    geometry = 'MULTIPOLYGON(((-180 90, 180 90, 180 -90, -180 -90, -180 90)))'
