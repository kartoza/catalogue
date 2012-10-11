"""
SANSA-EO Catalogue - products_model_helpermethods - implements unittests for
    product models helper functions

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
__date__ = '1/10/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import (
    coordIsOnBounds,
    sortCandidates,
    SortCandidateException)


class Product_HelperMethods_Test(TestCase):
    """
    Test Product model helper methods
    """
    fixtures = []

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_product_helpermethod_coordIsOnBounds(self):
        """
        Tests products model helper method coordIsOnBounds
        """

        myTestCoords = [(10, 10), (20, 20), (22, 22)]
        myTestExtents = (10, 20, 10, 20)
        #we need to bound results
        myExpectedResults = [True, True, False]
        #check if PK exists
        for idx, myCoord in enumerate(myTestCoords):
            myTestResult = coordIsOnBounds(myCoord, myTestExtents)
            self.assertEquals(
                myTestResult, myExpectedResults[idx],
                simpleMessage(
                    myTestResult, myExpectedResults[idx],
                    message='coordIsOnBounds incorrect for test %i' % idx))

    def test_product_helpermethod_sortCandidates(self):
        """
        Tests products model helper method sortCandidates
        """

        myTestCandidates = [
            [(10, 10), (10, 20), (20, 20), (20, 10), (10, 10)],
            [(10, 10), (10, 20), (9, 20), (20, 20), (20, 10), (9, 10)]]
        myTestExtents = (10, 20, 10, 20)  # not actually used
        myTestCentorid = (15, 15)

        myExpectedResults = [
            [(10, 20), (20, 20), (20, 10), (10, 10)],
            [(9, 20), (20, 20), (20, 10), (10, 10)]]

        for idx, myCoord in enumerate(myTestCandidates):
            myTestResult = sortCandidates(
                myCoord, myTestExtents, myTestCentorid)
            self.assertEquals(
                myTestResult, myExpectedResults[idx],
                simpleMessage(
                    myTestResult, myExpectedResults[idx],
                    message='sortCandidates incorrect for test %i' % idx))

    def test_product_helpermethod_sortCandidates_exception(self):
        """
        Tests products model helper method sortCandidates
        """

        myTestCandidates = [
            [(10, 10), (10, 20), (20, 20), (20, 10), (10, 10)],
            [(100, 100), (100, 200), (200, 200), (200, 100), (100, 100)]]
        myTestExtents = (10, 20, 10, 20)  # not actually used
        myTestCentorid = (25, 25)

        for idx, myCoord in enumerate(myTestCandidates):
            #check if exception is raised
            self.assertRaises(
                SortCandidateException, sortCandidates,
                myCoord, myTestExtents, myTestCentorid)
