"""
SANSA-EO Catalogue - search_inclinationangle - test correctness of
    search results for inclinationangle

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


class TestSearchIncliantionAngle(TestCase):
    """
    Tests Search Inclination Angle
    """

    def test_InclinationAngleRange_positive(self):
        """
        Test inclination angle range:
            - 0-90 (positive)
            - -90-0 (negative)
            - -10-10 (normal)
        """
        OpticalProductF.create(**{
            'sensor_inclination_angle': 40
        })
        OpticalProductF.create(**{
            'sensor_inclination_angle': 30
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'sensor_inclination_angle': 55
        })

        mySearch = SearchF.create(**{
            'sensor_inclination_angle_start': 30,
            'sensor_inclination_angle_end': 50
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_InclinationAngleRange_negative(self):
        """
        Test inclination angle range:
            - 0-90 (positive)
            - -90-0 (negative)
            - -10-10 (normal)
        """
        OpticalProductF.create(**{
            'sensor_inclination_angle': -40
        })
        OpticalProductF.create(**{
            'sensor_inclination_angle': -30
        })

        # create an optical product that should not appear in the results
        OpticalProductF.create(**{
            'sensor_inclination_angle': -25
        })

        mySearch = SearchF.create(**{
            'sensor_inclination_angle_start': -50,
            'sensor_inclination_angle_end': -30
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 2)

    def test_InclinationAngleRange_inverted(self):
        """
        Test inclination angle range:
            - 0-90 (positive)
            - -90-0 (negative)
            - -10-10 (normal)
        """
        OpticalProductF.create(**{
            'sensor_inclination_angle': 40
        })
        OpticalProductF.create(**{
            'sensor_inclination_angle': 30
        })
        OpticalProductF.create(**{
            'sensor_inclination_angle': 80
        })

        mySearch = SearchF.create(**{
            'sensor_inclination_angle_start': 50,
            'sensor_inclination_angle_end': 30
        })

        # create Searcher object
        mySearcher = Searcher(mySearch)
        self.assertEqual(mySearcher.mQuerySet.count(), 0)
