"""
SANSA-EO Catalogue - AllUsersMessage_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, linda@sansa.org.za'
__version__ = '0.1'
__date__ = '31/10/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from offline_messages.models import OfflineMessage

from catalogue.models import AllUsersMessage


class AllUsersMesageCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = ['test_user.json']

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_AllUsersMessage_create(self):
        """
        Tests AllUsersMessage model creation
        """

        myModel = AllUsersMessage(message='Hello')
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

        myCount = OfflineMessage.objects.count()
        myMessage = ('Expected there to be OfflineMessages after making '
                     'a broadcast message')
        self.assertGreater (myCount, 0, myMessage)

    def test_AllUsersMessage_read(self):
        """
        Tests AllUsersMessage model read
        """
        myModel = AllUsersMessage(message='Hello')
        myModel.save()
        myModelPK = myModel.id
        myModel = AllUsersMessage.objects.get(pk=myModelPK)
        #check if data is correct
        self.assertEqual(myModel.message, 'Hello')

    def test_AllUsersMessage_update(self):
        """
        Tests AllUsersMessage model update
        """
        myModel = AllUsersMessage(message='Hello')
        myModel.save()
        myModelPK = myModel.id
        myModel = AllUsersMessage.objects.get(pk=myModelPK)
        myMessages = OfflineMessage.objects
        myCount = myMessages.count()
        #check if data is correct
        self.assertEqual(myModel.message, 'Hello')
        myModel.message = 'Foo'
        myModel.save()
        myModel = AllUsersMessage.objects.get(pk=myModelPK)
        self.assertEqual(myModel.message, 'Foo')
        myMessages = OfflineMessage.objects
        myMessage = ('Expected there to be more OfflineMessages after '
                     'changing a broadcast message')
        self.assertGreater (myMessages.count(), myCount, myMessage)

    def test_AllUsersMessage_delete(self):
        """
        Tests AllUsersMessage model delete
        """
        myModel = AllUsersMessage(message='Hello')
        myModel.save()
        myModelPK = myModel.id
        myModel.delete()
        try:
            myModel = AllUsersMessage.objects.get(pk=myModelPK)
            assert False, 'AllUsersMessageObject was not deleted'
        except:
            pass
