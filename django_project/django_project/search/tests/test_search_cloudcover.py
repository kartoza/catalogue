"""
SANSA-EO Catalogue - search_cloudcover - test correctness of
    cloud cover search results

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
__date__ = '01/09/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from search.searcher import Searcher
from catalogue.tests.model_factories import OpticalProductF
from model_factories import SearchF


class TestSearchCloudCover(TestCase):
    """
    Tests Search Cloud Cover
    """

    def test_CloudCoverSearch(self):
        """
        Test cloud cover range:
        - with 50% or less
        """

        OpticalProductF.create(**{
            'cloud_cover': 40
        })
        OpticalProductF.create(**{
            'cloud_cover': 50
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'cloud_cover': 1000
        })

        mySearch = SearchF.create(**{
            'cloud_mean': 50
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_CloudCoverSearch_null(self):
        """
        Test cloud cover range:
        - with 50% or less and null
        """

        OpticalProductF.create(**{
            'cloud_cover': None
        })
        OpticalProductF.create(**{
            'cloud_cover': 50
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'cloud_cover': 1000
        })

        mySearch = SearchF.create(**{
            'cloud_mean': 50
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)
