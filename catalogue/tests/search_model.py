"""
SANSA-EO Catalogue - Search_model - implements basic CRUD unittests

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
__date__ = '29/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import Search
from datetime import datetime


class SearchCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_acquisitionmode.json',
        'test_sensortype.json',
        'test_processinglevel.json',
        'test_searchdaterange.json',
        'test_search.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Search_create(self):
        """
        Tests Search model creation
        """
        myNewData = {
            'record_count': None,
            'use_cloud_cover': False,
            'sensor_inclination_angle_end': None,
            'search_date': '2010-07-15 09:21:38',
            'mission_id': None,
            'sensor_type_id': None,
            'keywords': '',
            'guid': '69d814b7-TEST-42b9-9530-50ae77806da9',
            'sensor_inclination_angle_start': None,
            'acquisition_mode': None,
            'ip_position': None,
            'polarising_mode': None,
            'deleted': False,
            'spatial_resolution': None,
            'k_orbit_path': None,
            'band_count': None,
            'user_id': 1,
            'geometry': 'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 -34.65, 17.54 -32.05))',
            'j_frame_row': None,
            'search_type': 1,
            'cloud_mean': 5,
            'license_type': None
        }

        myModel = Search(**myNewData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

        #we need to create manyTomany field separatly
        myNewDataM2M = {
            'processing_level': [],
            'sensors': [4]
        }
        #add M2M fields
        for field, vals in myNewDataM2M.iteritems():
            for value in vals:
                myModel.__getattribute__(field).add(value)

        #check if M2M models were added
        for field in myNewDataM2M:
            myRes = myModel.__getattribute__(field).count()
            myExpRes = len(myNewDataM2M.get(field))
            self.assertTrue(myRes == myExpRes,
                simpleMessage(myRes, myExpRes,
                    message='Model M2M field "%s" count:' % field))

    def test_Search_read(self):
        """
        Tests Search model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'record_count': None,
            'use_cloud_cover': False,
            'sensor_inclination_angle_end': None,
            'search_date': datetime.strptime('2010-07-15 09:21:38', '%Y-%m-%d %H:%M:%S'),
            'mission_id': None,
            'sensor_type_id': None,
            'keywords': '',
            'guid': '69d814b7-3164-42b9-9530-50ae77806da9',
            'sensor_inclination_angle_start': None,
            'acquisition_mode_id': None,
            'ip_position': None,
            'polarising_mode': None,
            'deleted': False,
            'spatial_resolution': None,
            'k_orbit_path': None,
            'band_count': None,
            'user_id': 1,
            'geometry': '0103000020E6100000010000000500000000000000408A314000000000A00740C00000000000D6344000000000A03440C000000000004F344000000000009741C00000000000D9314000000000805341C000000000408A314000000000A00740C0',
            'j_frame_row': None,
            'search_type': 1,
            'cloud_mean': 5,
            'license_type': None
        }
        myModel = Search.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

        #check m2m
        myExpectedModelDataM2M = {
            'processing_level': [],
            'sensors': [
                4
            ]
            }
        #add M2M fields
        for field in myExpectedModelDataM2M:
            myRes = len(myModel.__getattribute__(field).all())
            myExpRes = len(myExpectedModelDataM2M.get(field))
            self.assertEqual(myRes, myExpRes,
                simpleMessage(myRes, myExpRes,
                    message='For field "%s"' % field))
        #import ipdb;ipdb.set_trace()

    def test_Search_update(self):
        """
        Tests Search model update
        """
        myModelPK = 1
        myModel = Search.objects.get(pk=myModelPK)
        myNewModelData = {
            'user_id': 1,
            'order_id': 1,
            'product_id': 1960810,
            'delivery_detail_id': None,
            'internal_order_id': None,
            'download_path': 'Some path',
            'product_ready': True
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_Search_delete(self):
        """
        Tests Search model delete
        """
        myModelPK = 1
        myModel = Search.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_Search_getDictionaryMap(self):
        """
        Tests Search model getDictionaryMap method
        """
        myParams = ['sensor_type', 'mission_sensor', 'mission']
        myExpResults = ['acquisition_mode__sensor_type',
        'acquisition_mode__sensor_type__mission_sensor',
        'acquisition_mode__sensor_type__mission_sensor__mission']

        for idx, param in enumerate(myParams):
            myRes = Search.getDictionaryMap(param)
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model getDictionaryMap(\'%s\'):' % param))

    def test_Search_sensorsAsString(self):
        """
        Tests Search model sensorsAsString method
        """
        myModelPKs = [1, 2, 4, 7]
        myExpResults = ['MSS-1', 'AVHRR-3, TM-4, AMI-1, ETM+, MSS-1, Xi, Xs, Pan, M',
        'TM-4', '']

        for idx, PK in enumerate(myModelPKs):
            myModel = Search.objects.get(pk=PK)
            myRes = myModel.sensorsAsString()
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s sensorsAsString:' % PK))

    def test_Search_datesAsString(self):
        """
        Tests Search model datesAsString method
        """
        myModelPKs = [1, 2, 4, 7]
        myExpResults = ['01-01-1901 : 31-12-2100', '01-01-2009 : 31-12-2012',
        '01-01-2000 : 31-12-2005', '01-01-1900 : 31-12-2100']

        for idx, PK in enumerate(myModelPKs):
            myModel = Search.objects.get(pk=PK)
            myRes = myModel.datesAsString()
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s datesAsString:' % PK))

    def test_Search_getRowChoices(self):
        """
        Tests Search model getRowChoices method
        """
        myModelPKs = [23, 24, 25, 26]
        myExpResults = [[391], [], [412],
        [380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391]]

        for idx, PK in enumerate(myModelPKs):
            myModel = Search.objects.get(pk=PK)
            myRes = myModel.getRowChoices()
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s getRowChoices:' % PK))

    def test_Search_getPathChoices(self):
        """
        Tests Search model getPathChoices method
        """
        myModelPKs = [23, 24, 25, 26]
        myExpResults = [[], [144], [137],
        [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 144]]

        for idx, PK in enumerate(myModelPKs):
            myModel = Search.objects.get(pk=PK)
            myRes = myModel.getPathChoices()
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s getPathChoices:' % PK))
