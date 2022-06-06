"""
SANSA-EO Catalogue - search_bandcount - test correctness of
    search results for spectral group

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
    SpectralGroupF, OpticalProductProfileF,
    SpectralModeF
)
from model_factories import SearchF


class TestSearchSpectralGroup(TestCase):
    """
    Tests Search Spectral Group
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_Search_spectral_group(self):
        """
        Test spectral group searches
        """

        mySpecGroup = SpectralGroupF.create(**{
            'name': 'My Spectral Group'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'spectralgroup': mySpecGroup
        })

        myOPP = OpticalProductProfileF.create(**{
            'spectral_mode': mySpecMode
        })

        OpticalProductF.create(**{
            'product_profile': myOPP
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create()

        mySearch = SearchF.create(**{
            'spectral_groups': [mySpecGroup]
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 1)
