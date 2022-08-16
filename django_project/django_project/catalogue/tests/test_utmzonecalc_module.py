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
__version__ = '0.2'
__date__ = '07/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from catalogue.utmzonecalc import utmZoneFromLatLon, utmZoneOverlap


class utmZoneFromLatLon_Test(TestCase):
    """
    Tests utmzonecalc module, utmZoneFromLatLon function
    """

    def test_inputValues(self):
        """
        Tests if utmZoneFromLatLon will throw an exception on wrong input
        """
        #test searches pk
        myTestValues = [(-190, 0), (0, -100), (190, 100)]

        for idx, testVal in enumerate(myTestValues):
            #check if exception is raised
            self.assertRaises(
                ValueError, utmZoneFromLatLon, testVal[0], testVal[1])

    def test_returnResult(self):
        """
        Tests if utmZoneFromLatLon with correct input values
        """
        myTestValues = [(-179, 0), (0, -80), (179, 89), (0, 0)]
        myExpectedResults = [
            ('32701', 'UTM01S'), ('32731', 'UTM31S'),
            ('32660', 'UTM60N'), ('32731', 'UTM31S')
        ]

        for idx, testVal in enumerate(myTestValues):
            myRes = utmZoneFromLatLon(*testVal)
            myExpRes = myExpectedResults[idx]

            self.assertEqual(myRes, myExpRes)


class utmZoneOverlap_Test(TestCase):
    """
    Tests utmzonecalc module, utmZoneOverlap function
    """

    def test_utmZoneOverlap(self):
        """
        Tests if utmZoneFromLatLon will throw an exception on wrong input
        """
        myTestValues = [
            (-34, -64, -35, -52), (-34, -64, -30, -62), (-40, -64, -30, -52),
            (-80, -64, -30, -52)]
        myExpectedResults = [
            [('32725', 'UTM25S')],
            [('32725', 'UTM25S'), ('32726', 'UTM26S')],
            [('32724', 'UTM24S'), ('32725', 'UTM25S'), ('32726', 'UTM26S')],
            [
                ('32717', 'UTM17S'), ('32718', 'UTM18S'), ('32719', 'UTM19S'),
                ('32720', 'UTM20S'), ('32721', 'UTM21S'), ('32722', 'UTM22S'),
                ('32723', 'UTM23S'), ('32724', 'UTM24S'), ('32725', 'UTM25S'),
                ('32726', 'UTM26S')
            ]
        ]

        for idx, testVal in enumerate(myTestValues):
            myRes = utmZoneOverlap(*testVal)
            myExpRes = myExpectedResults[idx]

            self.assertEqual(myRes, myExpRes)
