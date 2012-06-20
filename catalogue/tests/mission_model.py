"""
SANSA-EO Catalogue - mission_model - implements basic CRUD unittests

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
from catalogue.models import Mission


class MissionCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_missiongroup.json',
        'test_mission.json',
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_mission_create(self):
        """
        Tests Mission model creation
        """
        myMissionData = {
            'abbreviation': 'MIT',
            'owner': 'Unknown',
            'mission_group_id': 1,
            'name': 'Mission Name Unknown Test',
            'operator_abbreviation': 'UNK-1'
        }

        myModel = Mission(**myMissionData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_mission_read(self):
        """
        Tests Mission model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'abbreviation': 'N14',
            'owner': 'NOAA',
            'mission_group_id': 1,
            'name': 'National Oceanic and Atmospheric Administration Satellite\
 14',
            'operator_abbreviation': 'NOAA-14'
        }
        myModel = Mission.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key)))

    def test_mission_update(self):
        """
        Tests License model update
        """
        myModelPK = 1
        myModel = Mission.objects.get(pk=myModelPK)
        myNewModelData = {
            'abbreviation': 'MIT',
            'owner': 'Unknown',
            'mission_group_id': 1,
            'name': 'Mission Name Unknown Test',
            'operator_abbreviation': 'UNK-1'
        }

        myModel = Mission(**myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key)))

    def test_mission_delete(self):
        """
        Tests MissionGroup model delete
        """
        myModelPK = 1
        myModel = Mission.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_mission_repr(self):
        """
        Tests MissionGroup model representation
        """
        myModelPKs = [1, 100]
        myExpResults = [u'NOAA-14', u'SSU']

        for idx, missionPK in enumerate(myModelPKs):
            myModel = Mission.objects.get(pk=missionPK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx])

