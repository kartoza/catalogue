# -*- coding: utf-8 -*-
"""
SANSA-EO Catalogue - DIMS IIF ingestor tests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkley@sansa.org.za'
__version__ = '0.1'
__date__ = '3/09/2013'
__copyright__ = 'South African National Space Agency'

import os
from django.test import TestCase
import unittest

from django.core.management import call_command
from catalogue.models import (
    GenericProduct)
from catalogue.ingestors import dims_iif

from dictionaries.tests.model_factories import (
    SatelliteF,
    SatelliteInstrumentF,
    SpectralModeF,
    SpectralGroupF,
    InstrumentTypeF,
    SatelliteInstrumentGroupF,
    OpticalProductProfileF,
    ProjectionF,
    QualityF
)
DATA_DIR_PATH = os.path.join(
    os.path.dirname(__file__),
    'sample_files/DIMS')


class DIMSIIFIngestorTest(TestCase):
    """
    Tests IIF Ingestor
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

        oli_instrument_type = InstrumentTypeF.create(
            abbreviation='OLI',
            operator_abbreviation='OLI')
        tirs_instrument_type = InstrumentTypeF.create(
            abbreviation='TIRS',
            operator_abbreviation='TIRS')
        oli_tirs_instrument_type = InstrumentTypeF.create(
            abbreviation='OTC',
            operator_abbreviation='OLI_TIRS')
        mss_instrument_type = InstrumentTypeF.create(
            abbreviation='MSS',
            operator_abbreviation='MSS')
        etm_instrument_type = InstrumentTypeF.create(
            abbreviation='ETM',
            operator_abbreviation='ETM')
        tm_instrument_type = InstrumentTypeF.create(
            abbreviation='TM',
            operator_abbreviation='TM')

        #
        # Create satellites and their groups
        #

        l8_satellite = SatelliteF.create(
            abbreviation='L8',
            operator_abbreviation='LS-8')
        l8_oli_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=l8_satellite,
            instrument_type=oli_instrument_type
        )
        l8_tirs_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=l8_satellite,
            instrument_type=tirs_instrument_type
        )
        l8_oli_tirs_satellite_instrument_group = \
            SatelliteInstrumentGroupF.create(
                satellite=l8_satellite,
                instrument_type=oli_tirs_instrument_type
            )

        l7_satellite = SatelliteF.create(
            abbreviation='L7',
            operator_abbreviation='LS-7')
        l7_etm_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=l7_satellite,
            instrument_type=etm_instrument_type
        )

        l5_satellite = SatelliteF.create(
            abbreviation='L5',
            operator_abbreviation='LS-5')
        l5_tm_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=l5_satellite,
            instrument_type=tm_instrument_type
        )
        l5_mss_satellite_instrument_group = SatelliteInstrumentGroupF.create(
            satellite=l5_satellite,
            instrument_type=mss_instrument_type
        )

        #
        # Create SatelliteInstruments
        #
        l8_tirs_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='L8-TIRS',
            satellite_instrument_group=l8_tirs_satellite_instrument_group
        )
        l8_oli_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='L8-OLI',
            satellite_instrument_group=l8_oli_satellite_instrument_group
        )
        l8_oli_tirs_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='L8-OLI-TIRS',
            satellite_instrument_group=l8_oli_tirs_satellite_instrument_group
        )
        l7_etm_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='L7-ETM',
            satellite_instrument_group=l7_etm_satellite_instrument_group
        )
        l5_tm_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='L5-TM',
            satellite_instrument_group=l5_tm_satellite_instrument_group
        )
        l5_mss_instrument = SatelliteInstrumentF.create(
            operator_abbreviation='L5-MSS',
            satellite_instrument_group=l5_mss_satellite_instrument_group
        )

        #
        # Spectral groups
        #

        thm_spectral_group = SpectralGroupF.create(
            abbreviation='THM'
        )
        rgb_spectral_group = SpectralGroupF.create(
            abbreviation='RGB'
        )
        pan_spectral_group = SpectralGroupF.create(
            abbreviation='PAN'
        )
        ms_spectral_group = SpectralGroupF.create(
            abbreviation='MS'
        )

        #
        # Spectral modes
        #

        l5_hrf_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'HRF',
            'instrument_type': tm_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        l5_mss_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'MSS',
            'instrument_type': mss_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        l5_rgb_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'RGB',
            'instrument_type': tm_instrument_type,
            'spectralgroup': rgb_spectral_group
        })
        l5_thm_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'THM',
            'instrument_type': tm_instrument_type,
            'spectralgroup': thm_spectral_group
        })

        l7_pan_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'HPN',
            'instrument_type': etm_instrument_type,
            'spectralgroup': pan_spectral_group
        })
        l7_hrf_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'HRF',
            'instrument_type': etm_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        l7_htm_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'HTM',
            'instrument_type': etm_instrument_type,
            'spectralgroup': thm_spectral_group
        })
        l7_rgb_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'RGB',
            'instrument_type': etm_instrument_type,
            'spectralgroup': rgb_spectral_group
        })

        l8_oli_ms_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'MS',  # name OLI MS
            'instrument_type': oli_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        l8_oli_tirs_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'MS',  # name OLI TIRS MS
            'instrument_type': oli_tirs_instrument_type,
            'spectralgroup': ms_spectral_group
        })
        l8_oli_thm_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'TIRS-THM',
            'instrument_type': oli_instrument_type,
            'spectralgroup': thm_spectral_group
        })
        l8_pan_spectral_mode = SpectralModeF.create(**{
            'abbreviation': 'OLI-PAN',
            'instrument_type': oli_instrument_type,
            'spectralgroup': pan_spectral_group
        })

        # etm_spectral_mode = SpectralModeF.create(**{
        #     'abbreviation': 'RGB',
        #     'instrument_type': etm_instrument_type,
        #     'spectralgroup': rgb_spectral_group
        # })

        #
        # Product profiles
        #

        l8_oli_ms_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': l8_oli_instrument,
            'spectral_mode': l8_oli_ms_spectral_mode
        })
        l8_oli_tirs_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': l8_oli_tirs_instrument,
            'spectral_mode': l8_oli_tirs_spectral_mode
        })
        l7_etm_hrf_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': l7_etm_instrument,
            'spectral_mode': l7_hrf_spectral_mode
        })
        l5_tm_hrf_profile = OpticalProductProfileF.create(**{
            'satellite_instrument': l5_tm_instrument,
            'spectral_mode': l5_hrf_spectral_mode
        })

    # noinspection PyMethodMayBeStatic
    def test_import_using_management_command(self):
        """Test that we can ingest spot using the management command"""
        call_command('dims_iif_harvest',
                     verbosity=2,
                     source_dir=DATA_DIR_PATH,
                     theHaltOnErrorFlag=False)

    # noinspection PyMethodMayBeStatic
    def test_direct_import(self):
        """Test that we can ingest DIMS IIF using the ingestor function"""

        #
        # Test with a full load of data
        #
        dims_iif.ingest(
            source_path=DATA_DIR_PATH,
            verbosity_level=2,
            halt_on_error_flag=False)
        products = GenericProduct.objects.filter(
            original_product_id__contains='LC8')
        product_list = []
        formatted_list = ''
        for product in products:
            product_list.append(product.product_id)
            formatted_list += product.product_id + '\n'

        existing_product_id = 'LC81780702013341JSA00'
        message = 'Expected:\n%s\nTo be in:\n%s\n' % (
            existing_product_id,
            formatted_list)
        assert existing_product_id in product_list, message

        # Re-ingest and make sure that overridden owner sticks
        # Above ran in test mode so image was

        dims_iif.ingest(
            source_path=DATA_DIR_PATH,
            verbosity_level=2,
            halt_on_error_flag=False)

        product = GenericProduct.objects.get(
            original_product_id=existing_product_id)

        assert 'updating' in product.ingestion_log


if __name__ == '__main__':
    unittest.main()
