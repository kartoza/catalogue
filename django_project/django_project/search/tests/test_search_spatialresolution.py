"""
SANSA-EO Catalogue - search_spatialresolution - test correctness of
    search results for spatial resolution

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


class TestSearchSpatialResolution(TestCase):
    """
    Tests Search spatial resolution
    """

    def test_SpatialResolution_0(self):
        """
        Test spatial resolution:
        -   0 - '<= 1m',
        """

        OpticalProductF.create(**{
            'spatial_resolution': 0.5
        })
        OpticalProductF.create(**{
            'spatial_resolution': 1
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'spatial_resolution': -1
        })

        mySearch = SearchF.create(**{
            'spatial_resolution': 0
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_SpatialResolution_1(self):
        """
        Test spatial resolution:
        -   1 - '1m - 2m',
        """

        OpticalProductF.create(**{
            'spatial_resolution': 1.1
        })
        OpticalProductF.create(**{
            'spatial_resolution': 2
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'spatial_resolution': 5
        })

        mySearch = SearchF.create(**{
            'spatial_resolution': 1
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_SpatialResolution_2(self):
        """
        Test spatial resolution:
        -   2 - '2m - 6m',
        """

        OpticalProductF.create(**{
            'spatial_resolution': 2.1
        })
        OpticalProductF.create(**{
            'spatial_resolution': 6
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'spatial_resolution': 1
        })

        mySearch = SearchF.create(**{
            'spatial_resolution': 2
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_SpatialResolution_3(self):
        """
        Test spatial resolution:
        -   3 - '6m - 20m',
        """

        OpticalProductF.create(**{
            'spatial_resolution': 6.1
        })
        OpticalProductF.create(**{
            'spatial_resolution': 20
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'spatial_resolution': 5
        })

        mySearch = SearchF.create(**{
            'spatial_resolution': 3
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_SpatialResolution_4(self):
        """
        Test spatial resolution:
        -   4 - '20m - 35m',
        """

        OpticalProductF.create(**{
            'spatial_resolution': 20.1
        })
        OpticalProductF.create(**{
            'spatial_resolution': 35
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'spatial_resolution': 36
        })

        mySearch = SearchF.create(**{
            'spatial_resolution': 4
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_SpatialResolution_5(self):
        """
        Test spatial resolution:
        -   5 - '35m - 60m'
        """

        OpticalProductF.create(**{
            'spatial_resolution': 35.1
        })
        OpticalProductF.create(**{
            'spatial_resolution': 60
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'spatial_resolution': 66
        })

        mySearch = SearchF.create(**{
            'spatial_resolution': 5
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)
