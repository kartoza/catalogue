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
from catalogue.models import SensorType


class SensorTypeCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_missiongroup.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_sensortype.json',
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_sensortype_create(self):
        """
        Tests SensorType model creation
        """
        mySensorTypeData = {
            'abbreviation': 'NONE',
            'mission_sensor_id': 100,
            'name': 'Unknown sensor type',
            'operator_abbreviation': 'NONE'
        }

        myModel = SensorType(**mySensorTypeData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_sensortype_read(self):
        """
        Tests SensorType model read
        """
        myModelPK = 2
        myExpectedModelData = {
            'abbreviation': 'AMI',
            'mission_sensor_id': 2,
            'name': 'AMI',
            'operator_abbreviation': 'AMI'
        }
        myModel = SensorType.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                    message='For key "%s"' % key))

    def test_sensortype_update(self):
        """
        Tests SensorType model update
        """
        myModelPK = 1
        myModel = SensorType.objects.get(pk=myModelPK)
        myNewModelData = {
            'abbreviation': 'NONE',
            'mission_sensor_id': 100,
            'name': 'Unknown sensor type',
            'operator_abbreviation': 'NONE'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                message='For key "%s"' % key))

    def test_sensortype_delete(self):
        """
        Tests SensorType model delete
        """
        myModelPK = 1
        myModel = SensorType.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_sensortype_repr(self):
        """
        Tests MissionSensor model representation
        """
        myModelPKs = [1, 2]
        myExpResults = [u'AVHRR-3:Advanced Very High Resolution Radiometer',
            u'AMI-1:AMI']

        for idx, PK in enumerate(myModelPKs):
            myModel = SensorType.objects.get(pk=PK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx],
                simpleMessage(myModel.__unicode__(), myExpResults[idx],
                    message='Model PK %s repr:' % PK))
