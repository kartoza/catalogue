"""
SANSA-EO Catalogue - acquisitionMode_model - implements basic CRUD unittests

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
from catalogue.models import AcquisitionMode


class AcquisitionModeCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_missiongroup.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_sensortype.json',
        'test_acquisitionmode.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_acquisitionmode_create(self):
        """
        Tests AcquisitionMode model creation
        """
        myNewModelData = {
            'name': 'ZeroSpectral',
            'spatial_resolution': 1000,
            'is_grayscale': False,
            'band_count': 231,
            'abbreviation': 'ZS',
            'sensor_type_id': 1,
            'operator_abbreviation': 'ZS'
        }

        myModel = AcquisitionMode(**myNewModelData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_acquisitionmode_read(self):
        """
        Tests AcquisitionMode model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'name': 'Multispectral',
            'spatial_resolution': 0,
            'is_grayscale': False,
            'band_count': 0,
            'abbreviation': 'MS',
            'sensor_type_id': 1,
            'operator_abbreviation': 'MS'
        }
        myModel = AcquisitionMode.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                    message='For key "%s"' % key))

    def test_acquisitionmode_update(self):
        """
        Tests AcquisitionMode model update
        """
        myModelPK = 1
        myModel = AcquisitionMode.objects.get(pk=myModelPK)
        myNewModelData = {
            'name': 'ZeroSpectral',
            'spatial_resolution': 1000,
            'is_grayscale': False,
            'band_count': 231,
            'abbreviation': 'ZS',
            'sensor_type_id': 1,
            'operator_abbreviation': 'ZS'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                message='For key "%s"' % key))

    def test_acquisitionmode_delete(self):
        """
        Tests AcquisitionMode model delete
        """
        myModelPK = 1
        myModel = AcquisitionMode.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_acquisitionmode_repr(self):
        """
        Tests MissionSensor model representation
        """
        myModelPKs = [1, 2]
        myExpResults = [u'AVHRR-3:Multispectral',
            u'AMI-1:Vertical Vertical Polarisation']

        for idx, PK in enumerate(myModelPKs):
            myModel = AcquisitionMode.objects.get(pk=PK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx],
                simpleMessage(myModel.__unicode__(), myExpResults[idx],
                    message='Model PK %s repr:' % PK))
