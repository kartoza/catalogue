"""
SANSA-EO Catalogue - searcher_object - tests for email functions

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
__date__ = '19/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.models import (Order,
                              User,
                              TaskingRequest)
from catalogue.views.helpers import (notifySalesStaff,
                                     notifySalesStaffOfTaskRequest)
from django.core import mail

class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
                       'from@example.com', ['to@example.com'],
                       fail_silently=False)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Subject here')


class EmailNotificationTest(TestCase):
    """
    Tests Email Notifications (see catalogue.views.helpers)
    """

    fixtures = [
        'test_user.json',
        'test_contenttypes.json'
        'test_missiongroup.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_institution.json',
        'test_license.json',
        'test_projection',
        'test_quality',
        'test_orderstatus.json',
        'test_order.json',
        'test_searchrecord.json',
        'test_sacuserprofile.json',
        'test_orderstatus.json',
        'test_marketsector.json',
        'test_creatingsoftware',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json',
        'test_datum.json',
        'test_deliverymethod.json',
        'test_fileformat.json',
        'test_resamplingmethod.json',
        'test_taskingrequest.json',
        'test_ordernotificationrecipients.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        self.user = User.objects.get(pk=2)

    def testOrderNotifications(self):
        #myUser = User.objects.get(id=1)
        #/addtocart/2277404/?xhr
        #/addtocart/2531895/?xhr
        #/addtocart/2604814/?xhr

        # Basic mail test as per django docs
        mail.send_mail('Subject here', 'Here is the message.',
                       'from@example.com',
                      ['to@example.com'], fail_silently=False)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')

        myOrderId = Order.objects.all()[0].id
        notifySalesStaff(self.user, myOrderId)
        # One email sent to the client
        # TODO: why not one sent to the staff member??? Check contentypes in
        # fixtures
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject,
                         'SANSA Order 1 status update (Placed)')
        self.assertEqual(mail.outbox[1].recipients(),
                         [u'piet@pompies.com'])


        myOrderId = TaskingRequest.objects.all()[0].id
        notifySalesStaffOfTaskRequest(self.user, myOrderId)
        # One email sent to the client and one sent to the staff member
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[2].subject,
                         'SANSA Tasking Request 1 status update (Placed)')
        self.assertEqual(mail.outbox[2].recipients(),
                        [u'tim@linfiniti.com'])
        self.assertEqual(mail.outbox[3].subject,
                         'SANSA Tasking Request 1 status update (Placed)')
        self.assertEqual(mail.outbox[3].recipients(),
                        [u'piet@pompies.com'])

