"""
SANSA-EO Catalogue - utmzonecalc_module - tests correctness of
    utmZoneFromLatLon method

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
__date__ = '10/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.utmzonecalc import utmZoneFromLatLon


class utmZoneFromLatLon_Test(TestCase):
    """
    Tests utmzonecalc module
    """

    def test_inputValues(self):
        """
        Tests if utmZoneFromLatLon will throw an exception on wrong input
        """
        #test searches pk
        myTestValues = [(-190, 0), (0, -100), (190, 100)]

        for idx, testVal in enumerate(myTestValues):
            #check if exception is raised
            self.assertRaises(ValueError, utmZoneFromLatLon, testVal[0], testVal[1])

    def test_returnResult(self):
        """
        Tests if utmZoneFromLatLon will throw an exception on wrong input
        """
        myTestValues = [(-179, 0), (0, -80), (179, 89), (0, 0)]
        myExpectedResults = [[('32701', 'UTM01S')], [('32731', 'UTM31S')],
        [('32660', 'UTM60N')], [('32731', 'UTM31S')]]

        for idx, testVal in enumerate(myTestValues):
            myRes = utmZoneFromLatLon(*testVal)
            myExpRes = myExpectedResults[idx]

            self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes))

    def test_returnResultWithBuffer(self):
        """
        Tests if utmZoneFromLatLon will throw an exception on wrong input
        """
        myTestValues = [(-32, -64, 0), (-32, -64, 1), (-32, -64, 2)]
        myExpectedResults = [[('32725', 'UTM25S')], [('32724', 'UTM24S'), ('32725', 'UTM25S'), ('32726', 'UTM26S')],
                [('32723', 'UTM23S'), ('32724', 'UTM24S'), ('32725', 'UTM25S'), ('32726', 'UTM26S'), ('32727', 'UTM27S')]]

        for idx, testVal in enumerate(myTestValues):
            myRes = utmZoneFromLatLon(*testVal)
            myExpRes = myExpectedResults[idx]

            self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes))
