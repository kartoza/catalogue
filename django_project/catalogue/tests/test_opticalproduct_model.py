"""
SANSA-EO Catalogue - opticalproduct_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.3'
__date__ = '26/07/2013'
__copyright__ = 'South African National Space Agency'


import logging
logger = logging.getLogger(__name__)
from datetime import datetime

from django.test import TestCase

from dictionaries.tests.model_factories import (
    ProcessingLevelF, OpticalProductProfileF, SatelliteInstrumentF,
    SpectralModeF, InstrumentTypeF, SatelliteF, SatelliteInstrumentGroupF
)

from .model_factories import (
    OpticalProductF, InstitutionF, ProjectionF, QualityF
)


class OpticalProductCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OpticalProduct_create(self):
        """
        Tests OpticalProduct model creation

        As this is sub classed model, we need to include 'parent' model
        attributes. Django will handle parent model creation automatically
        """
        myModel = OpticalProductF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_OpticalProduct_delete(self):
        """
        Tests OpticalProduct model delete
        """
        myModel = OpticalProductF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_OpticalProduct_read(self):
        """
        Tests OpticalProduct model read
        """
        myModel = OpticalProductF.create(**{
            'solar_azimuth_angle': 0.0,
            'gain_change_per_channel': None,
            'gain_value_per_channel': None,
            'cloud_cover': 5,
            'bias_per_channel': None,
            'solar_zenith_angle': 0.0,
            'sensor_viewing_angle': 2.0,
            'sensor_inclination_angle': 2.21492,
            'gain_name': None,
            'earth_sun_distance': None
        })

        self.assertEqual(myModel.solar_azimuth_angle, 0.0)
        self.assertEqual(myModel.gain_change_per_channel, None)
        self.assertEqual(myModel.gain_value_per_channel, None)
        self.assertEqual(myModel.cloud_cover, 5)
        self.assertEqual(myModel.bias_per_channel, None)
        self.assertEqual(myModel.solar_zenith_angle, 0.0)
        self.assertEqual(myModel.sensor_viewing_angle, 2.0)
        self.assertEqual(myModel.sensor_inclination_angle, 2.21492)
        self.assertEqual(myModel.gain_name, None)
        self.assertEqual(myModel.earth_sun_distance, None)

    def test_OpticalProduct_update(self):
        """
        Tests OpticalProduct model update
        """
        myModel = OpticalProductF.create()

        myModel.__dict__.update(**{
            'solar_azimuth_angle': 0.0,
            'gain_change_per_channel': None,
            'gain_value_per_channel': None,
            'cloud_cover': 5,
            'bias_per_channel': None,
            'solar_zenith_angle': 0.0,
            'sensor_viewing_angle': 2.0,
            'sensor_inclination_angle': 2.21492,
            'gain_name': None,
            'earth_sun_distance': None
        })
        myModel.save()

        self.assertEqual(myModel.solar_azimuth_angle, 0.0)
        self.assertEqual(myModel.gain_change_per_channel, None)
        self.assertEqual(myModel.gain_value_per_channel, None)
        self.assertEqual(myModel.cloud_cover, 5)
        self.assertEqual(myModel.bias_per_channel, None)
        self.assertEqual(myModel.solar_zenith_angle, 0.0)
        self.assertEqual(myModel.sensor_viewing_angle, 2.0)
        self.assertEqual(myModel.sensor_inclination_angle, 2.21492)
        self.assertEqual(myModel.gain_name, None)
        self.assertEqual(myModel.earth_sun_distance, None)

    def test_OpticalProduct_getMetadataDict(self):
        """
        Tests OpticalProduct model getMetadataDict method
        """
        myInstitution = InstitutionF.create(**{
            u'address1': u'Hartebeeshoek', u'address2': u'Gauteng',
            u'address3': u'South Africa', u'name': u'SANSA',
            u'post_code': u'0000'
        })

        myProjection = ProjectionF.create(**{
            u'name': u'UTM37S', u'epsg_code': 32737
        })

        myProcessingLevel = ProcessingLevelF.create(**{
            u'abbreviation': u'L1A'
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })

        myInstType = InstrumentTypeF.create(**{
            'name': 'INSTYPE1'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'instrument_type': myInstType
        })

        myOPP = OpticalProductProfileF.create(**{
            u'spectral_mode': mySpecMode, u'satellite_instrument': mySatInst
        })

        myQuality = QualityF.create(**{'name': 'SuperQuality'})

        myModel = OpticalProductF.create(**{
            'unique_product_id': '123 Product ID 123',
            'owner': myInstitution,
            'projection': myProjection,
            'processing_level': myProcessingLevel,
            'product_profile': myOPP,
            'quality': myQuality,
            'product_acquisition_start': datetime(2012, 12, 12, 12, 00),
            'product_acquisition_end': datetime(2012, 12, 12, 14, 00),
            'solar_azimuth_angle': 0.0,
            'gain_change_per_channel': None,
            'gain_value_per_channel': None,
            'cloud_cover': 5,
            'bias_per_channel': None,
            'solar_zenith_angle': 0.0,
            'sensor_viewing_angle': 2.0,
            'sensor_inclination_angle': 2.21492,
            'gain_name': None,
            'earth_sun_distance': None
        })

        myExpResult = {
            'product_date': '2012-12-12T00:00:00',
            'institution_address': u'Hartebeeshoek', 'institution_region': '',
            'image_quality_code': 'SuperQuality', 'vertical_cs': u'UTM37S',
            'processing_level_code': u'L1A', 'cloud_cover_percentage': 5,
            'file_identifier': '123 Product ID 123',
            'spatial_coverage': (
            '17.54,-32.05 20.83,-32.41 20.3,-35.17 17.84,-34.65 '
            '17.54,-32.05'),
            'bbox_east': 20.83, 'md_abstract': '',
            'md_product_date': '2012-12-12T00:00:00',
            'institution_city': u'Gauteng', 'bbox_north': -32.05,
            'institution_name': u'SANSA',
            'institution_country': u'South Africa', 'bbox_west': 17.54,
            'institution_postcode': u'0000',
            'md_data_identification': (
            u'SATIN 1 -- Temp Spectral mode - INSTYPE1'),
            'bbox_south': -35.17
        }

        myRes = myModel.getMetadataDict()
        self.assertEqual(myRes, myExpResult)

    def test_OpticalProduct_thumbnailDirectory(self):
        """
        Tests OpticalProduct model thumbnailDirectory method
        """

        mySat = SatelliteF.create(**{
            'abbreviation': 'mySAT'
        })

        mySatInstGroup = SatelliteInstrumentGroupF.create(**{
            'satellite': mySat
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInstGroup
        })

        myOPP = OpticalProductProfileF.create(**{
            u'satellite_instrument': mySatInst
        })

        myModel = OpticalProductF.create(**{
            'product_profile': myOPP,
            'product_acquisition_start': datetime(2012, 12, 12, 12, 00),
        })

        myExpResult = 'mySAT/2012/12/12'

        myRes = myModel.thumbnailDirectory()
        self.assertEqual(myRes, myExpResult)

    def test_OpticalProduct_productDirectory(self):
        """
        Tests OpticalProduct model productDirectory method
        """

        mySat = SatelliteF.create(**{
            'abbreviation': 'mySAT'
        })

        mySatInstGroup = SatelliteInstrumentGroupF.create(**{
            'satellite': mySat
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInstGroup
        })

        myProcessingLevel = ProcessingLevelF.create(**{
            u'abbreviation': u'L1A'
        })

        myOPP = OpticalProductProfileF.create(**{
            u'satellite_instrument': mySatInst
        })

        myModel = OpticalProductF.create(**{
            'processing_level': myProcessingLevel,
            'product_profile': myOPP,
            'product_acquisition_start': datetime(2012, 12, 12, 12, 00),
        })

        myExpResult = 'mySAT/L1A/2012/12/12'

        myRes = myModel.productDirectory()
        self.assertEqual(myRes, myExpResult)