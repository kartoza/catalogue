"""
SANSA-EO Catalogue - OrderNotificationRecipients_model - implements basic CRUD unittests

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
from catalogue.models import OrderNotificationRecipients


class OrderNotificationRecipientsCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_missionsensor.json',
        'test_ordernotificationrecipients.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OrderNotificationRecipients_create(self):
        """
        Tests OrderNotificationRecipients model creation
        """
        myNewData = {
            'user_id': 1
        }
        myModel = OrderNotificationRecipients(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

        #we need to create manyTomany field separatly
        myNewDataM2M = {
            'classes': [50, 51],
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

    def test_OrderNotificationRecipients_read(self):
        """
        Tests OrderNotificationRecipients model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'user_id': 1
        }

        myModel = OrderNotificationRecipients.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key %s' % key))

        #check m2m
        myExpectedModelDataM2M = {
            'classes': [50, 54, 20, 51, 52, 21, 53, 22],
            'sensors': [4, 1]
            }
        #add M2M fields
        for field in myExpectedModelDataM2M:
            myRes = len(myModel.__getattribute__(field).all())
            myExpRes = len(myExpectedModelDataM2M.get(field))
            self.assertEqual(myRes, myExpRes,
                simpleMessage(myRes, myExpRes,
                    message='For field "%s"' % field))

    def test_OrderNotificationRecipients_update(self):
        """
        Tests OrderNotificationRecipients model update
        """
        myModelPK = 1
        myModel = OrderNotificationRecipients.objects.get(pk=myModelPK)
        myNewModelData = {
            'user_id': 1
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key %s' % key))

    def test_OrderNotificationRecipients_delete(self):
        """
        Tests OrderNotificationRecipients model delete
        """
        myModelPK = 1
        myModel = OrderNotificationRecipients.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
