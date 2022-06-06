# -*- coding: utf-8 -*-
"""
SANSA-EO Catalogue - searcher_object - tests for email functions

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '12/07/2012'
__copyright__ = 'South African National Space Agency'

import os
import unittest
from django.test import TestCase
from django.core.management import call_command
from catalogue.models import (
    GenericProduct
)

from dictionaries.models import Institution
from catalogue.ingestors import spot


SHAPEFILE_NAME = os.path.join(
    os.path.dirname(__file__),
    'sample_files/spot-ingestion/Africa_2012_subset.shp')


class SpotIngestorTest(TestCase):
    """
    Tests SPOT ingestor
    """

    fixtures = [
        'test_user.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_institution.json',
        'test_license.json',
        'test_projection.json',
        'test_quality.json',
        'test_orderstatus.json',
        'test_order.json',
        'test_searchrecord.json',
        'test_sansauserprofile.json',
        'test_orderstatus.json',
        'test_marketsector.json',
        'test_creatingsoftware.json',
        # new dicts
        'test_radarbeam.json',
        'test_imagingmode.json',
        'test_spectralgroup.json',
        'test_spectralmode.json',
        'test_scannertype.json',
        'test_instrumenttype.json',
        'test_collection.json',
        'test_satellite.json',
        'test_satelliteinstrument.json',
        'test_radarproductprofile.json',
        'test_opticalproductprofile.json',

        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json',
        'test_datum.json',
        'test_deliverymethod.json',
        'test_fileformat.json',
        'test_resamplingmethod.json',
        'test_deliverydetail.json']

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def testImportUsingManagementCommand(self):
        """Test that we can ingest spot using the management command"""
        call_command(
            'spot_harvest',
            verbosity=2,
            shapefile=SHAPEFILE_NAME)

    def testImportDirectly(self):
        """Test that we can ingest spot using the ingestor function"""

        #
        # Test with a full load of data
        #
        spot.ingest(theShapeFile=SHAPEFILE_NAME,
                    theVerbosityLevel=1)
        myProducts = GenericProduct.objects.filter(product_id__contains='S5')
        myList = []
        myFormattedList = ''
        for myProduct in myProducts:
            myList.append(myProduct.product_id)
            myFormattedList += myProduct.product_id + '\n'

        # Test that 'T' Color products are not ingested
        myExpectedProductId = (
            'S5-_HRG_T--_S5C2_0100_00_0368_00'
            '_120510_090310_1B--_ORBIT-')
        myMessage = 'Expected:\n%s\nTo be in:\n%s\n' % (
            myExpectedProductId,
            myFormattedList)
        assert myExpectedProductId not in myList, myMessage

        # Test that 'T' Grayscale products ARE  ingested
        myExpectedProductId = (
            'S5-_HRG_T--_S5C2_0100_00_0368_00'
            '_120510_090308_1B--_ORBIT-')
        myMessage = 'Expected:\n%s\nTo be in:\n%s\n' % (
            myExpectedProductId,
            myFormattedList)
        assert myExpectedProductId in myList, myMessage

        # Test that Spot products are not owned by RapidEye
        myBadOwner = Institution.objects.get(id=3)
        myProduct = GenericProduct.objects.get(product_id=myExpectedProductId)
        assert myProduct.owner is not myBadOwner

        #Reingesst and make sure that overridden owner sticks

        spot.ingest(theShapeFile=SHAPEFILE_NAME,
                    theOwner='Foobar')
        myProduct = GenericProduct.objects.get(
            product_id=(myExpectedProductId))
        assert myProduct.owner.name == 'Foobar'

    def testAreaFiltering(self):
        """Test that AOI filtering works"""
        #
        # Test importing only recs in an area of interest
        #
        myArea = (
            'POLYGON('
            '(16.206099 -5.592359,'
            '16.206099 -6.359587,'
            '17.293880 -6.359587,'
            '17.293880 -5.592359,'
            '16.206099 -5.592359))')
        print(myArea)
        myProductCount = GenericProduct.objects.count()
        spot.ingest(theShapeFile=SHAPEFILE_NAME,
                    theVerbosityLevel=1,
                    theArea=myArea)
        myNewProductCount = GenericProduct.objects.count()
        self.assertEqual(myProductCount + 4, myNewProductCount)

    def testAcquisitionCreation(self):
        """Test that acquisistion modes are made on demand"""
        #
        # Test importing only recs in an area of interest
        #
        myAcquisitionMode = AcquisitionMode.objects.get(id=22)
        myAcquisitionMode.delete()
        myAcquisitionMode = AcquisitionMode.objects.get(id=23)
        myAcquisitionMode.delete()
        mySensorType = SensorType.objects.get(id=29)
        mySensorType.delete()
        mySensorTypeCount = SensorType.objects.all().count()
        myAcquisitionModeCount = AcquisitionMode.objects.all().count()
        spot.ingest(theShapeFile=SHAPEFILE_NAME,
                    theVerbosityLevel=1)
        myNewSensorTypeCount = SensorType.objects.all().count()
        myNewAcquisitionModeCount = AcquisitionMode.objects.all().count()
        #there should be two more than before HRV-2:P and HRV-2:X
        self.assertEqual(mySensorTypeCount + 2, myNewSensorTypeCount)
        #there should be four more than before
        self.assertEqual(myAcquisitionModeCount + 4, myNewAcquisitionModeCount)

if __name__ == '__main__':
    unittest.main()
