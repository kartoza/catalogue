"""
SANSA-EO Catalogue - featurereaders_return - tests correct parsing of
    geometry files (SHP, KML, KMZ)

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

from catalogue.featureReaders import (
    getFeaturesFromZipFile, processGeometriesType
)


class FeatureReaders_Test(TestCase):
    """
    Tests FeatureReaders returned geometry type
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_read_simple_shape(self):
        """
        Tests file reader for Polygon
        """
        myExpGeomType = 'Polygon'
        myExpNumPoints = 7
        myExpExtent = (
            28.69104367281659, -22.34292118429061,
            28.70027636054984, -22.336069729032527)

        myFile = 'catalogue/fixtures/search-area.zip'
        myFeatures = getFeaturesFromZipFile(myFile, 'Polygon')
        myResult = processGeometriesType(myFeatures)

        #test common geometry attributes
        self.assertEqual(myResult.geom_type, myExpGeomType)

        self.assertEqual(myResult.num_points, myExpNumPoints)

        self.assertEqual(myResult.extent, myExpExtent)

    def test_read_multi_shape(self):
        """
        Tests SHP file reader for MultiPolygon
        """
        myExpGeomType = 'Polygon'
        myExpNumPoints = 5
        myExpExtent = (
            28.681750340899242, -22.34292118429061,
            28.70027636054984, -22.33066577657862)

        myFile = 'catalogue/fixtures/multipart-search-area.zip'
        myFeatures = getFeaturesFromZipFile(myFile, 'Polygon')
        myResult = processGeometriesType(myFeatures)

        #test common geometry attributes
        self.assertEqual(myResult.geom_type, myExpGeomType)

        self.assertEqual(myResult.num_points, myExpNumPoints)

        self.assertEqual(myResult.extent, myExpExtent)

    def test_fix_for_story137(self):
        """
        Tests file reader for story137 issue
        """
        myExpGeomType = 'Polygon'
        myExpNumPoints = 8
        myExpExtent = (
            34.33069277482281, -24.657561281028393,
            35.557607225177264, -23.759412256205678)

        myFile = 'catalogue/fixtures/Ala_Minaar_Hatch.zip'
        myFeatures = getFeaturesFromZipFile(myFile, 'Polygon')
        myResult = processGeometriesType(myFeatures)

        #test common geometry attributes
        self.assertEqual(myResult.geom_type, myExpGeomType)

        self.assertEqual(myResult.num_points, myExpNumPoints)

        self.assertEqual(myResult.extent, myExpExtent)
