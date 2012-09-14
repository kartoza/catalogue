"""
SANSA-EO Catalogue - missionsensor_model - implements basic CRUD unittests

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
__date__ = '20/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import MissionSensor


class MissionSensorCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_missiongroup.json',
        'test_mission.json',
        'test_missionsensor.json',
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_missionsensor_create(self):
        """
        Tests MissionSensor model creation
        """
        myMissionSensorData = {
            'is_radar': False,
            'name': 'Test mission sensor',
            'description': 'None',
            'mission_id': 1,
            'abbreviation': 'TMS',
            'operator_abbreviation': 'TMS-001',
            'has_data': True,
            'is_taskable': True
        }

        myModel = MissionSensor(**myMissionSensorData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_missionsensor_read(self):
        """
        Tests MissionSensor model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'is_radar': False,
            'name': 'NOAA-14 AVHRR',
            'description': 'Advanced Very High Resolution Radiometer NOAA',
            'mission_id': 1,
            'abbreviation': 'AVH',
            'operator_abbreviation': 'AVHRR-3',
            'has_data': True,
            'is_taskable': False
        }
        myModel = MissionSensor.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_missionsensor_update(self):
        """
        Tests MissionSensor model update
        """
        myModelPK = 1
        myModel = MissionSensor.objects.get(pk=myModelPK)
        myNewModelData = {
            'is_radar': False,
            'name': 'Test mission sensor',
            'description': 'None',
            'mission_id': 1,
            'abbreviation': 'TMS',
            'operator_abbreviation': 'TMS-001',
            'has_data': True,
            'is_taskable': True
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_missionsensor_delete(self):
        """
        Tests MissionSensor model delete
        """
        myModelPK = 1
        myModel = MissionSensor.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_missionsensor_repr(self):
        """
        Tests MissionSensor model representation
        """
        myModelPKs = [1, 100]
        myExpResults = [u'NOAA-14 AVHRR', u':UMS']

        for idx, PK in enumerate(myModelPKs):
            myModel = MissionSensor.objects.get(pk=PK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx],
                simpleMessage(myModel.__unicode__(), myExpResults[idx],
                    message='Model PK %s repr:' % PK))
