"""
SANSA-EO Catalogue - search_rowpath - test correctness of
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


class TestSearchRowPath(TestCase):
    """
    Tests Search Row/Path
    """

    def test_RowPathRange_row(self):
        """
        Test row/path searches:
        - row 40
        """

        OpticalProductF.create(**{
            'row': 40
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'row': 45
        })

        mySearch = SearchF.create(**{
            'j_frame_row': '40'
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 1)

    def test_RowPathRange_path(self):
        """
        Test row/path searches:
        - path 144
        """

        OpticalProductF.create(**{
            'path': 144
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'path': 123
        })

        mySearch = SearchF.create(**{
            'k_orbit_path': '144'
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 1)

    def test_RowPathRange_row_and_path(self):
        """
        Test row/path searches:
        - row 40 and path 144
        """

        OpticalProductF.create(**{
            'row': 40,
            'path': 144
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'row': 45,
            'path': 123
        })

        mySearch = SearchF.create(**{
            'j_frame_row': '40',
            'k_orbit_path': '144'
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 1)

    def test_RowPathRange_combined(self):
        """
        Test row/path searches:
        - row 380-390, 391 and path 144, 100-120
        """

        OpticalProductF.create(**{
            'row': 385,
            'path': 144
        })
        OpticalProductF.create(**{
            'row': 391,
            'path': 110
        })
        OpticalProductF.create(**{
            'row': 391,
            'path': 144
        })
        OpticalProductF.create(**{
            'row': 385,
            'path': 110
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'row': 375,
            'path': 110
        })

        mySearch = SearchF.create(**{
            'j_frame_row': '380-390, 391',
            'k_orbit_path': '144, 100-120'
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 4)
