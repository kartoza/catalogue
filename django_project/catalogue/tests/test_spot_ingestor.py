# -*- coding: utf-8 -*-
"""
SANSA-EO Catalogue - searcher_object - tests for email functions

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
__date__ = '12/07/2012'
__copyright__ = 'South African National Space Agency'


import os
from django.test import TestCase
import unittest
# import factory
from django.core.management import call_command
from catalogue.models import (
    GenericProduct, OpticalProduct)
from dictionaries.tests.model_factories import (
    SatelliteF,
    SatelliteInstrumentF,
    SpectralModeF,
    SpectralGroupF,
    InstrumentTypeF,
    SatelliteInstrumentGroupF,
    OpticalProductProfileF,
    ProjectionF,
    QualityF)
from catalogue.ingestors import spot

SHAPEFILE_NAME = os.path.join(
    os.path.dirname(__file__),
    'sample_files/spot-ingestion/Africa_2012_subset.shp')


class SpotIngestorTest(TestCase):
    """
    Tests SPOT ingestor
    """
    def setUp(self):
        """
        Sets up before each test
        """
        QualityF.create(name='Unknown')
        ProjectionF.create(epsg_code=32734)
        ProjectionF.create(epsg_code=4326)
        #
        # Create Instrument types
        #

        # Spot 1,2,3
        hrv_instrument_type = InstrumentTypeF.create(
            abbreviation='HRV',
            operator_abbreviation='HRV')
        # Spot 4
        hrvir_instrument_type = InstrumentTypeF.create(
            abbreviation='HRVIR',
            operator_abbreviation='HRVIR')
        # Spot 5
        hrg_instrument_type = InstrumentTypeF.create(
            abbreviation='HRG',
            operator_abbreviation='HRG')

        #
        # Create satellites and their groups
        #

        s1_satellite = SatelliteF.create(
            abbreviation='S1',
            operator_abbreviation='SPOT-1')
        s1_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=s1_satellite,
            instrument_type=hrv_instrument_type
        )

        s2_satellite = SatelliteF.create(
            abbreviation='S2',
            operator_abbreviation='SPOT-2')
        s2_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=s2_satellite,
            instrument_type=hrv_instrument_type
        )

        s3_satellite = SatelliteF.create(
            abbreviation='S3',
            operator_abbreviation='SPOT-3')
        s3_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=s3_satellite,
            instrument_type=hrv_instrument_type
        )

        s4_satellite = SatelliteF.create(
            abbreviation='S4',
            operator_abbreviation='SPOT-4')
        s4_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=s4_satellite,
            instrument_type=hrvir_instrument_type
        )

        s5_satellite = SatelliteF.create(
            abbreviation='S5',
            operator_abbreviation='SPOT-5')
        s5_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=s5_satellite,
            instrument_type=hrg_instrument_type
        )

        #
        # Create SatelliteInstruments
        #

        # Two HRV cameras on Spot1 satellite
        s1_hrv1_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S1-HRV1',
            satellite_instrument_group=s1_satellite_instrument_group
        )
        s1_hrv2_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S1-HRV2',
            satellite_instrument_group=s1_satellite_instrument_group
        )

        # Two HRV cameras on Spot2 satellite
        s2_hrv1_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S2-HRV1',
            satellite_instrument_group=s2_satellite_instrument_group
        )
        s2_hrv2_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S2-HRV2',
            satellite_instrument_group=s2_satellite_instrument_group
        )

        # Two HRV cameras on Spot3 satellite
        s3_hrv1_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S3-HRV1',
            satellite_instrument_group=s3_satellite_instrument_group
        )
        s3_hrv2_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S3-HRV2',
            satellite_instrument_group=s3_satellite_instrument_group
        )

        # Two HRVIR cameras on Spot4 satellite
        s4_hrvir1_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S4-HRVIR1',
            satellite_instrument_group=s4_satellite_instrument_group
        )
        s4_hrvir2_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S4-HRVIR2',
            satellite_instrument_group=s4_satellite_instrument_group
        )

        # Two HRVG cameras on Spot5 satellite
        s5_hrg1_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S5-HRG1',
            satellite_instrument_group=s5_satellite_instrument_group
        )
        s5_hrg2_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='S5-HRG2',
            satellite_instrument_group=s5_satellite_instrument_group
        )

        #
        # Spectral groups
        #

        pan_spectral_group = SpectralGroupF.create(
            abbreviation='PAN'
        )
        ms_spectral_group = SpectralGroupF.create(
            abbreviation='MS'
        )

        #
        # Spectral modes
        #

        s123_x_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'X',
            'instrument_type': hrv_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        s123_p_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'P',
            'instrument_type': hrv_instrument_type,
            'spectralgroup': pan_spectral_group
        })

        s4_i_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'I',
            'instrument_type': hrvir_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        s4_m_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'M',
            'instrument_type': hrvir_instrument_type,
            'spectralgroup': pan_spectral_group
        })

        s5_a_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'A',
            'instrument_type': hrg_instrument_type,
            'spectralgroup': pan_spectral_group
        })
        s5_b_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'B',
            'instrument_type': hrg_instrument_type,
            'spectralgroup': pan_spectral_group
        })
        s5_j_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'J',
            'instrument_type': hrg_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        s5_t_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'T',
            'instrument_type': hrg_instrument_type,
            'spectralgroup': pan_spectral_group
        })

        #
        # Product profiles
        #

        ####### SPOT 1 possible products ###############

        # You can get a multispectral image from spot 1 camera hrv1
        # noinspection PyUnusedLocal
        s1_hrv1_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s1_hrv1_instrument,
            'spectral_mode': s123_x_spectral_mode
        })
        # You can get a pan image from spot 1 camera hrv1
        # noinspection PyUnusedLocal
        s1_hrv1_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s1_hrv1_instrument,
            'spectral_mode': s123_p_spectral_mode
        })

        # You can get a multispectral image from spot 1 camera hrv2
        # noinspection PyUnusedLocal
        s1_hrv2_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s1_hrv2_instrument,
            'spectral_mode': s123_x_spectral_mode
        })
        # You can get a pan image from spot 1 camera hrv2
        # noinspection PyUnusedLocal
        s1_hrv2_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s1_hrv2_instrument,
            'spectral_mode': s123_p_spectral_mode
        })

        ####### SPOT 2 possible products ###############

        # You can get a multispectral image from spot 2 camera hrv1
        # noinspection PyUnusedLocal
        s2_hrv1_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s2_hrv1_instrument,
            'spectral_mode': s123_x_spectral_mode
        })
        # You can get a pan image from spot 2 camera hrv1
        # noinspection PyUnusedLocal
        s2_hrv1_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s2_hrv1_instrument,
            'spectral_mode': s123_p_spectral_mode
        })

        # You can get a multispectral image from spot 2 camera hrv2
        # noinspection PyUnusedLocal
        s2_hrv2_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s2_hrv2_instrument,
            'spectral_mode': s123_x_spectral_mode
        })
        # You can get a pan image from spot 2 camera hrv2
        # noinspection PyUnusedLocal
        s2_hrv2_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s2_hrv2_instrument,
            'spectral_mode': s123_p_spectral_mode
        })

        ####### SPOT 3 possible products ###############

        # You can get a multispectral image from spot 3 camera hrv1
        # noinspection PyUnusedLocal
        s3_hrv1_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s3_hrv1_instrument,
            'spectral_mode': s123_x_spectral_mode
        })
        # You can get a pan image from spot 3 camera hrv1
        # noinspection PyUnusedLocal
        s3_hrv1_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s3_hrv1_instrument,
            'spectral_mode': s123_p_spectral_mode
        })

        # You can get a multispectral image from spot 3 camera hrv2
        # noinspection PyUnusedLocal
        s3_hrv2_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s3_hrv2_instrument,
            'spectral_mode': s123_x_spectral_mode
        })
        # You can get a pan image from spot 3 camera hrv2
        # noinspection PyUnusedLocal
        s3_hrv2_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s3_hrv2_instrument,
            'spectral_mode': s123_p_spectral_mode
        })

        ####### SPOT 4 possible products ###############

        # You can get a multispectral image from spot 4 camera hrvir1
        # noinspection PyUnusedLocal
        s4_hrvir1_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s4_hrvir1_instrument,
            'spectral_mode': s4_i_spectral_mode
        })
        # You can get a pan image from spot 4 camera hrvir1
        # noinspection PyUnusedLocal
        s4_hrvir1_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s4_hrvir1_instrument,
            'spectral_mode': s4_m_spectral_mode
        })

        # You can get a multispectral image from spot 4 camera hrvir2
        # noinspection PyUnusedLocal
        s4_hrvir2_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s4_hrvir2_instrument,
            'spectral_mode': s4_i_spectral_mode
        })
        # You can get a pan image from spot 4 camera hrvir2
        # noinspection PyUnusedLocal
        s4_hrvir2_pan_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s4_hrvir2_instrument,
            'spectral_mode': s4_m_spectral_mode
        })

        ####### SPOT 5 possible products ###############

        # You can get a multispectral image from spot 5 camera hrg1
        # noinspection PyUnusedLocal
        s5_hrg1_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg1_instrument,
            'spectral_mode': s5_j_spectral_mode
        })
        # You can get a pan T image from spot 5 camera hrg1
        # noinspection PyUnusedLocal
        s5_hrg1_pan_t_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg1_instrument,
            'spectral_mode': s5_t_spectral_mode
        })
        # You can get a pan A image from spot 5 camera hrg1
        # noinspection PyUnusedLocal
        s5_hrg1_pan_a_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg1_instrument,
            'spectral_mode': s5_a_spectral_mode
        })
        # You can get a pan B image from spot 5 camera hrg1
        # noinspection PyUnusedLocal
        s5_hrg1_pan_b_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg1_instrument,
            'spectral_mode': s5_b_spectral_mode
        })

        # You can get a multispectral image from spot 5 camera hrg2
        # noinspection PyUnusedLocal
        s5_hrg2_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg2_instrument,
            'spectral_mode': s5_j_spectral_mode
        })
        # You can get a pan T image from spot 5 camera hrg2
        # noinspection PyUnusedLocal
        s5_hrg2_pan_t_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg2_instrument,
            'spectral_mode': s5_t_spectral_mode
        })
        # You can get a pan A image from spot 5 camera hrg2
        # noinspection PyUnusedLocal
        s5_hrg2_pan_a_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg2_instrument,
            'spectral_mode': s5_a_spectral_mode
        })
        # You can get a pan B image from spot 5 camera hrg2
        # noinspection PyUnusedLocal
        s5_hrg2_pan_b_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': s5_hrg2_instrument,
            'spectral_mode': s5_b_spectral_mode
        })

    # noinspection PyMethodMayBeStatic
    def test_import_using_management_command(self):
        """Test that we can ingest spot using the management command"""
        call_command(
            'spot_harvest',
            verbosity=2,
            shapefile=SHAPEFILE_NAME)

    def test_import_directly(self):
        """Test that we can ingest spot using the ingestor function"""

        #
        # Test with a full load of data
        #
        spot.ingest(shapefile=SHAPEFILE_NAME,
                    verbosity_level=1,
                    halt_on_error_flag=False)

        # Test that 'H' and 'T' Color products are NOT ingested
        # (they would have the same product id as below and would normally
        # overwrite it so if we see we are on HRG2 then we know there
        # was no attempted imported.
        expected_product_id = '51003681205100903102J'
        product = OpticalProduct.objects.get(
            original_product_id__contains=expected_product_id)
        self.assertTrue(product.metadata.find('MODE=COLOR'))
        self.assertTrue(product.metadata.find('TYPE=J'))

        # Test that 'T' Grayscale products ARE  ingested
        expected_product_id = '51003681205100903082A'
        products = GenericProduct.objects.filter(
            original_product_id__contains=expected_product_id)
        result_list = []
        formatted_list = ''
        for product in products:
            result_list.append(product.product_id)
            formatted_list += product.product_id + '\n'

        message = 'Expected:\n%s\nTo be in:\n%s\n' % (
            expected_product_id,
            formatted_list)
        self.assertTrue(expected_product_id in result_list, message)

        # Check that if we get two records with the same ID in A21
        # but that are A (5m BW) and T (2.5m BW) they are ingested as
        # separate products. See notes in ingestor for more details.
        expected_ids = ['51204201301160834432A', '51204201301160834432T']
        products = GenericProduct.objects.filter(
            original_product_id__in=expected_ids)
        self.assertEqual(products.count(), 2)

    def test_area_filtering(self):
        """Test that AOI filtering works"""
        #
        # Test importing only recs in an area of interest
        #
        area = (
            'POLYGON('
            '(16.206099 -5.592359,'
            '16.206099 -6.359587,'
            '17.293880 -6.359587,'
            '17.293880 -5.592359,'
            '16.206099 -5.592359))')
        print area
        product_count = GenericProduct.objects.count()
        spot.ingest(shapefile=SHAPEFILE_NAME,
                    verbosity_level=3,
                    area_of_interest=area)
        new_product_count = GenericProduct.objects.count()
        self.assertEqual(product_count + 4, new_product_count)


if __name__ == '__main__':
    unittest.main()
