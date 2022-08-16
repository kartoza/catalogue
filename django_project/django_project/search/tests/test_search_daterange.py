"""
SANSA-EO Catalogue - search_bandcount - test correctness of
    search results for date ranges

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
__date__ = '23/01/2014'
__copyright__ = 'South African National Space Agency'

from datetime import datetime, date
from django.test import TestCase
from search.searcher import Searcher
from catalogue.tests.model_factories import OpticalProductF
from model_factories import SearchF, SearchDateRangeF


class TestSearchDateRange(TestCase):
    """
    Tests Search Date ranges
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_Search_date_range(self):
        """
        Test search date ranges
        """

        OpticalProductF.create(**{
            'product_acquisition_start': datetime(2010, 0o7, 15, 0, 0),
            'product_acquisition_end': None
        })
        OpticalProductF.create(**{
            'product_acquisition_start': datetime(2011, 0o7, 20, 0, 0),
            'product_acquisition_end': None
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'product_acquisition_start': datetime(2010, 0o7, 14, 0, 0),
            'product_acquisition_end': None
        })

        mySearch = SearchF.create()

        SearchDateRangeF.create(**{
            'search': mySearch,
            'start_date': date(2010, 0o7, 15),
            'end_date': date(2012, 0o7, 15)
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_Search_date_range_for_a_day(self):
        """
        Test search date ranges for a single day
        """

        OpticalProductF.create(**{
            'product_acquisition_start': datetime(2010, 0o7, 15, 0, 0),
            'product_acquisition_end': None
        })

        OpticalProductF.create(**{
            'product_acquisition_start': datetime(2010, 0o7, 16, 0, 0),
            'product_acquisition_end': None
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'product_acquisition_start': datetime(2010, 0o7, 14, 0, 0),
            'product_acquisition_end': None
        })

        mySearch = SearchF.create()

        SearchDateRangeF.create(**{
            'search': mySearch,
            'start_date': date(2010, 0o7, 15),
            'end_date': date(2010, 0o7, 15)
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)
