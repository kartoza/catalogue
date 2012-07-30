"""
SANSA-EO Catalogue - genericproduct_model - implements basic CRUD unittests

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
__date__ = '26/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import GenericProduct
from datetime import datetime


class GenericProductCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_genericproduct.json',
        #'test_genericimageryproduct.json',
        #'test_genericsensorproduct.json',
        #'test_opticalproduct.json',
        #'test_radarproduct.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_genericproduct_create(self):
        """
        Tests GenericProduct model creation
        """
        myNewData = {
            'product_date': '2100-01-01 12:00:00',
            'spatial_coverage': 'POLYGON ((21.3566000000000145 -27.2013999999999783, 21.4955000000000496 -26.6752999999999929, 22.0914000000000215 -26.7661999999999978, 21.9554000000000542 -27.2926999999999964, 21.3566000000000145 -27.2013999999999783))',
            'projection_id': 89,
            'license_id': 1,
            'original_product_id': '11204048606190846322X',
            'local_storage_path': None,
            'creating_software_id': 1,
            'remote_thumbnail_url': '',
            'product_revision': None,
            'owner_id': 1,
            'metadata': '',
            'quality_id': 1,
            'processing_level_id': 16,
            'product_id': 'S1-_HRV_X--_S1C2_0120_00_0404_00_000101_084632_1B--_ORBIT-'
        }

        myModel = GenericProduct(**myNewData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_genericproduct_read(self):
        """
        Tests GenericProduct model read
        """
        myModelPK = 1960810
        myExpectedModelData = {
            'product_date': datetime.strptime('1987-04-28 08:23:29', '%Y-%m-%d %H:%M:%S'),
            'spatial_coverage': '0103000020E61000000100000005000000C0490C022B373F4000CE1951DA3B33C020F241CF66553F408038D6C56DB432C0E85817B7D1004040C8CCCCCCCCCC32C060D1915CFEE33F4080A757CA325433C0C0490C022B373F4000CE1951DA3B33C0',
            'projection_id': 89,
            'license_id': 1,
            'original_product_id': '11363888704280823292P',
            'local_storage_path': None,
            'creating_software_id': 1,
            'remote_thumbnail_url': 'http://sirius.spotimage.fr/url/catalogue.aspx?ID=-1&ACTION=Scenes%3AgetQuicklook&CODEA21=11363888704280823292P&SEGMENT=43953&SAT=0',
            'product_revision': None,
            'owner_id': 1,
            'metadata': 'A21=11363888704280823292P\nSC_NUM=9205615\nSEG_NUM=43953\nSATEL=1\nANG_INC=24.766\nANG_ACQ=21.0\nDATE_ACQ=28/04/1987\nMONTH_ACQ=04\nTIME_ACQ=08:23:29\nCLOUD_QUOT=BBBBBBBB\nCLOUD_PER=5.0\nSNOW_QUOT=********\nLAT_CEN=-19.01\nLON_CEN=31.6047\nLAT_UP_L=-18.7\nLON_UP_L=31.3336\nLAT_UP_R=-18.8\nLON_UP_R=32.0064\nLAT_LO_L=-19.23\nLON_LO_L=31.2155\nLAT_LO_R=-19.32\nLON_LO_R=31.8906\nRESOL=10.0\nMODE=BW\nTYPE=P\nURL_QL=http://sirius.spotimage.fr/url/catalogue.aspx?ID=-1&ACTION=Scenes%3AgetQuicklook&CODEA21=11363888704280823292P&SEGMENT=43953&SAT=0',
            'quality_id': 1,
            'processing_level_id': 16,
            'product_id': 'S1-_HRV_P--_S1C2_0136_00_0388_00_870428_082329_1B--_ORBIT-'
        }
        myModel = GenericProduct.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_genericproduct_update(self):
        """
        Tests GenericProduct model update
        """
        myModelPK = 1960810
        myModel = GenericProduct.objects.get(pk=myModelPK)
        myNewModelData = {
            'product_date': '2100-01-01 12:00:00',
            'spatial_coverage': 'POLYGON ((21.3566000000000145 -27.2013999999999783, 21.4955000000000496 -26.6752999999999929, 22.0914000000000215 -26.7661999999999978, 21.9554000000000542 -27.2926999999999964, 21.3566000000000145 -27.2013999999999783))',
            'projection_id': 89,
            'license_id': 1,
            'original_product_id': '11204048606190846322X',
            'local_storage_path': None,
            'creating_software_id': 1,
            'remote_thumbnail_url': '',
            'product_revision': None,
            'owner_id': 1,
            'metadata': '',
            'quality_id': 1,
            'processing_level_id': 16,
            'product_id': 'S1-_HRV_X--_S1C2_0120_00_0404_00_000101_084632_1B--_ORBIT-'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_genericproduct_delete(self):
        """
        Tests GenericProduct model delete
        """
        myModelPK = 1960810
        myModel = GenericProduct.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_genericproduct_repr(self):
        """
        Tests GenericProduct model representation
        """
        myModelPKs = [1960810, 2143443, 1001218]
        myExpResults = [u'S1-_HRV_P--_S1C2_0136_00_0388_00_870428_082329_1B--_ORBIT-',
        u'S1-_HRV_X--_S1C1_0116_00_0360_00_920621_085718_1B--_ORBIT-',
        u'S1-_Pan_P--_CAM2_0126_00_0387_00_920703_082948_L2A-_UTM35S']

        for idx, PK in enumerate(myModelPKs):
            myModel = GenericProduct.objects.get(pk=PK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx],
                simpleMessage(myModel.__unicode__(), myExpResults[idx],
                    message='Model PK %s repr:' % PK))

    def test_genericproduct_tidySacId(self):
        """
        Tests GenericProduct model tidySacId
        """
        myModelPKs = [1960810, 2143443, 1001218]
        myExpResults = [u'S1 HRV P S1C2 0136 00 0388 00 870428',
        u'S1 HRV X S1C1 0116 00 0360 00 920621',
        u'S1 Pan P CAM2 0126 00 0387 00 920703']

        for idx, PK in enumerate(myModelPKs):
            myModel = GenericProduct.objects.get(pk=PK)
            self.assertEqual(myModel.tidySacId(), myExpResults[idx],
                simpleMessage(myModel.tidySacId(), myExpResults[idx],
                    message='Model PK %s tidySacId:' % PK))

    def test_genericproduct_getUTMZones(self):
        """
        Tests GenericProduct model getUTMZones
        """
        myModelPKs = [1960810, 2143443, 1001218]
        #overlapping
        myBufferParm = [0, 1, 5]
        myExpResults = [set([('32736', 'UTM36S')]),
        set([('32734', 'UTM34S'), ('32736', 'UTM36S'), ('32735', 'UTM35S')]),
        set([('32734', 'UTM34S'), ('32739', 'UTM39S'), ('32730', 'UTM30S'),
            ('32732', 'UTM32S'), ('32731', 'UTM31S'), ('32737', 'UTM37S'),
            ('32738', 'UTM38S'), ('32740', 'UTM40S'), ('32733', 'UTM33S'),
            ('32736', 'UTM36S'), ('32735', 'UTM35S')])]

        for idx, PK in enumerate(myModelPKs):
            myModel = GenericProduct.objects.get(pk=PK)
            myRes = myModel.getUTMZones(myBufferParm[idx])
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s getUTMZones:' % PK))

    def test_genericproduct_pad(self):
        """
        Tests GenericProduct model pad, this is a utility method
        """
        myInput = [u'12', u'HRG', u'HRG', u'']
        myPadParm = [5, 2, 6, 3]
        myExpResults = [u'12---', u'HRG', u'HRG---', u'---']

        for idx, inp in enumerate(myInput):
            myModel = GenericProduct()
            myRes = myModel.pad(inp, myPadParm[idx])
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx]))

    def test_genericproduct_zeroPad(self):
        """
        Tests GenericProduct model zeroPad, this is a utility method
        """
        myInput = [u'12', u'HRG', u'HRG', u'']
        myPadParm = [5, 2, 6, 3]
        myExpResults = [u'00012', u'HRG', u'000HRG', u'000']

        for idx, inp in enumerate(myInput):
            myModel = GenericProduct()
            myRes = myModel.zeroPad(inp, myPadParm[idx])
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx]))