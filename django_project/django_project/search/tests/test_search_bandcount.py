"""
SANSA-EO Catalogue - search_bandcount - test correctness of
    search results for band counts

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.2'
__date__ = '18/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from search.searcher import Searcher

from catalogue.tests.model_factories import OpticalProductF
from .model_factories import SearchF


class TestSearchBandCount(TestCase):
    """
    Tests Search Band Count
    """
    def setUp(self):
        """
        Set up before each test
        """

    def test_Search_bandcount_pan(self):
        """
        Test band count searches:
        - Panchromatic band count, range 0-2
        """

        OpticalProductF.create(**{
            'band_count': 1
        })
        OpticalProductF.create(**{
            'band_count': 2
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'band_count': -1
        })

        mySearch = SearchF.create(**{
            'band_count': 0
        })

        #create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_Search_bandcount_truecolor(self):
        """
        Test band count searches:
        - Truecolor band count, range 3
        """

        OpticalProductF.create(**{
            'band_count': 3
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'band_count': -1
        })

        mySearch = SearchF.create(**{
            'band_count': 1
        })

        #create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 1)

    def test_Search_bandcount_multi(self):
        """
        Test band count searches:
        - Multispectral band count, range 4-8
        """

        OpticalProductF.create(**{
            'band_count': 4
        })

        OpticalProductF.create(**{
            'band_count': 8
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'band_count': -1
        })

        mySearch = SearchF.create(**{
            'band_count': 2
        })

        #create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_Search_bandcount_super(self):
        """
        Test band count searches:
        - Superspectral band count, range 9-40
        """

        OpticalProductF.create(**{
            'band_count': 9
        })
        OpticalProductF.create(**{
            'band_count': 40
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'band_count': -1
        })

        mySearch = SearchF.create(**{
            'band_count': 3
        })

        #create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_Search_bandcount_hyper(self):
        """
        Test band count searches:
        - Hyperspectral band count, range 41-1000
        """

        OpticalProductF.create(**{
            'band_count': 41
        })
        OpticalProductF.create(**{
            'band_count': 1000
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'band_count': -1
        })

        mySearch = SearchF.create(**{
            'band_count': 4
        })

        #create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)
