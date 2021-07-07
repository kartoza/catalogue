"""
SANSA-EO Catalogue - search_bandcount - test correctness of
    search results for license types

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
__date__ = '22/01/2014'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from search.searcher import Searcher

from catalogue.tests.model_factories import OpticalProductF
from dictionaries.tests.model_factories import (
    SatelliteF, SatelliteInstrumentGroupF,
    SatelliteInstrumentF,
    OpticalProductProfileF, LicenseF
)
from model_factories import SearchF


class TestSearchLicenseType(TestCase):
    """
    Tests Search License types
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_Search_license_type(self):
        """
        Test satellite license types
        """

        licence = LicenseF.create(**{
            'name': 'My License'
        })
        sat = SatelliteF.create(**{
            'name': 'My Satellite',
            'license_type': licence
        })

        sat_inst_group = SatelliteInstrumentGroupF.create(**{
            'satellite': sat
        })

        sat_inst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': sat_inst_group
        })

        opp = OpticalProductProfileF.create(**{
            'satellite_instrument': sat_inst
        })

        OpticalProductF.create(**{
            'product_profile': opp
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create()

        search = SearchF.create(**{
            'license_types': [licence]
        })

        # create Searcher object
        searcher = Searcher(search)
        self.assertEqual(searcher.mQuerySet.count(), 1)
