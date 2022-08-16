"""
SANSA-EO Catalogue - search_only_searchable - test if the searcher only returns
    products which are searchable

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
__date__ = '29/01/2014'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from search.searcher import Searcher
from catalogue.tests.model_factories import OpticalProductF
from dictionaries.tests.model_factories import (
    SatelliteF, SatelliteInstrumentGroupF,
    SatelliteInstrumentF,
    OpticalProductProfileF, InstrumentTypeF
)
from model_factories import SearchF


class TestSearchOnlySearchable(TestCase):
    """
    Test searcher - returns only searchable products
    """

    def test_only_searchable(self):
        """
        Test searcher - returns only searchable products
        """

        mySat = SatelliteF.create(**{
            'name': 'My Satellite'
        })

        myInstrumentType = InstrumentTypeF.create(**{
            'is_searchable': False
        })

        mySatInstGroup = SatelliteInstrumentGroupF.create(**{
            'satellite': mySat,
            'instrument_type': myInstrumentType
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInstGroup
        })

        myOPP = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst
        })

        # create a test product which should not be searchable
        OpticalProductF.create(**{
            'product_profile': myOPP
        })

        # create a generic product which is seachable
        OpticalProductF.create(**{})
        OpticalProductF.create(**{})

        mySearch = SearchF.create()

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)
