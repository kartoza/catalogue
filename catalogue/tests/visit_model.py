"""
SANSA-EO Catalogue - Visit_model - implements basic CRUD unittests

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
from catalogue.models import Visit
from datetime import datetime


class VisitCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_visit.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Visit_create(self):
        """
        Tests Visit model creation
        """
        myNewData = {
            'city': 'New Unknown city',
            'country': 'New Unknown conutry',
            'ip_address': '10.10.10.10',
            'ip_position': 'POINT(28.2294006347656 -25.7068996429443)',
            'visit_date': '2010-11-10 10:23:37',
            'user_id': 1
        }
        myModel = Visit(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_Visit_read(self):
        """
        Tests Visit model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'city': 'Unknown city',
            'country': 'Unknown conutry',
            'ip_address': '10.10.10.10',
            'ip_position': '0101000020E6100000F9FFFFFFB93A3C40F6FFFF5FF7B439C0',
            'visit_date': datetime.strptime('2010-11-10 10:23:37', '%Y-%m-%d %H:%M:%S'),
            'user_id': 1
        }

        myModel = Visit.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_Visit_update(self):
        """
        Tests Visit model update
        """
        myModelPK = 1
        myModel = Visit.objects.get(pk=myModelPK)
        myNewModelData = {
            'city': 'New Unknown city',
            'country': 'New Unknown conutry',
            'ip_address': '10.10.10.10',
            'ip_position': 'POINT (28.2294006347656001 -25.7068996429443004)',
            # we don't test visit date as it's auto now field
            #'visit_date': '2010-11-10 10:23:37',
            'user_id': 1
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_Visit_delete(self):
        """
        Tests Visit model delete
        """
        myModelPK = 1
        myModel = Visit.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
