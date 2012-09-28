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

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '27/09/2012'
__copyright__ = 'South African National Space Agency'

import logging

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from catalogue.tests.test_utils import RequestFactory
from catalogue.views import (sendMessageToUser,
                             sendMessageToAllUsers,
                             userMessages)

class MessagingTests(TestCase):


    fixtures = [
       'test_user.json',
       ]

    def testSendMessageToUserAsStaff(self):
        """Test we can send a message to a user when logged in as staff.

        We use the factory implementation below to ensure that
        the request user is properly recognised as logged in, having
        cookies / session etc.

        """

        self.factory = RequestFactory(enforce_csrf_checks=True)
        myClient = Client()
        # First try to send a message as timlinux who IS staff
        assert self.factory.login(username='timlinux', password='password')
        self.user = User.objects.get(id=1)
        #self.factory.__setattr__('user', myUser)
        # post payload
        myPayload = {'user_id': '1',
                     'message': 'Hello'}
        # Note url below here is not used in direct view tests
        myRequest = self.factory.post('/sendMessageToUser/', myPayload)
        myRequest.user = self.user

        try:
            myRequest = sendMessageToUser(myRequest)
        except:
            myMessage = 'Probably the user session was not found'
            logging.exception(myMessage)
            self.fail(myMessage)

        myExpectedResponse = ('Message sent successfully to %s.' %
                              self.user.username)
        myMessage = 'Expected %s\n got\n %s' % (myExpectedResponse,
                                               myRequest.content)
        assert myRequest.content == myExpectedResponse, myMessage

    def testSendMessageToUserAsUser(self):
        """Test we can NOT send a message to a user when logged in as non staff.

        We use the factory implementation below to ensure that
        the request user is properly recognised as logged in, having
        cookies / session etc.

        """

        self.factory = RequestFactory(enforce_csrf_checks=True)
        myClient = Client()
        # First try to send a message as timlinux who IS staff
        assert self.factory.login(username='pompies', password='password')
        self.user = User.objects.get(id=2)
        #self.factory.__setattr__('user', myUser)
        # post payload
        myPayload = {'user_id': '1',
                     'message': 'Hello'}
        # Note url below here is not used in direct view tests
        myRequest = self.factory.post('/sendMessageToUser/', myPayload)
        myRequest.user = self.user

        try:
            myRequest = sendMessageToUser(myRequest)
            myMessage = 'Sending messages should be denied for non staff users'
            self.fail(myMessage)
        except:
            # Ok this is waht we want
            pass

    def testSendMessageToAllUsers(self):
        """Test we can send a message to all users when logged in as staff.

        We use the factory implementation below to ensure that
        the request user is properly recognised as logged in, having
        cookies / session etc.

        """

        self.factory = RequestFactory(enforce_csrf_checks=True)
        myClient = Client()
        # First try to send a message as timlinux who IS staff
        assert self.factory.login(username='timlinux', password='password')
        self.user = User.objects.get(id=1)
        #self.factory.__setattr__('user', myUser)
        # post payload
        myPayload = {'user_id': '1',
                     'message': 'Hello'}
        # Note url below here is not used in direct view tests
        myRequest = self.factory.post('/sendMessageToAllUsers/', myPayload)
        myRequest.user = self.user

        try:
            myRequest = sendMessageToAllUsers(myRequest)
        except:
            myMessage = 'Probably the user session was not found'
            logging.exception(myMessage)
            self.fail(myMessage)

        myExpectedResponse = 'Message sent successfully to all users.'
        myMessage = 'Expected %s\n got\n %s' % (myExpectedResponse,
                                                myRequest.content)
        assert myRequest.content == myExpectedResponse, myMessage


    def testUserMessages(self):
        """Test a user gets messages when we send them."""
        self.factory = RequestFactory(enforce_csrf_checks=True)
        myClient = Client()
        # First try to send a message as timlinux who IS staff
        assert self.factory.login(username='timlinux', password='password')
        self.user = User.objects.get(id=1)
        #self.factory.__setattr__('user', myUser)
        # post payload
        myPayload = {'user_id': '1',
                     'message': 'Hello'}
        # Note url below here is not used in direct view tests
        myResponse = self.factory.post('/sendMessageToAllUsers/', myPayload)
        myResponse.user = self.user

        try:
            myResponse = sendMessageToUser(myResponse)
        except:
            myMessage = 'Probably the user session was not found'
            logging.exception(myMessage)
            self.fail(myMessage)

        myExpectedResponse = ('Message sent successfully to %s.' %
                              self.user.username)
        myMessage = 'Expected %s\n got\n %s' % (myExpectedResponse,
                                                myResponse.content)
        assert myResponse.content == myExpectedResponse, myMessage

        # Now see if we can get the messages back:
        myResponse = userMessages(myResponse)
        myMessage = 'No messages obtained for user'
        assert myResponse.content != '', myMessage



