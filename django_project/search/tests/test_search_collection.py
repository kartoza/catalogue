"""
SANSA-EO Catalogue - search_bandcount - test correctness of
    search results for collections

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
    CollectionF, SatelliteF, SatelliteInstrumentGroupF, SatelliteInstrumentF,
    OpticalProductProfileF
)
from .model_factories import SearchF


class SearchCollection_Test(TestCase):
    """
    Tests Search Collection
    """
    def setUp(self):
        """
        Set up before each test
        """

    def test_Search_bandcount_pan(self):
        """
        Test collection searches
        """

        myCollection = CollectionF.create(**{
            'name': 'My collection'
        })

        mySat = SatelliteF.create(**{
            'collection': myCollection
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

        OpticalProductF.create(**{
            'product_profile': myOPP
        })

        mySearch = SearchF.create(**{
            'collections': [myCollection]
        })

        #create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 1)
