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
from catalogue.models import Order, User
from catalogue.views.helpers import notifySalesStaff


class EmailNotificationTest(TestCase):
    """
    Tests Email Notifications (see catalogue.views.helpers)
    """

    fixtures = [
        'test_user.json',
        'test_missiongroup.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        self.user = User.objects.get(pk=1)

    def test_StaffNotifications(self):
        #myUser = User.objects.get(id=1)
        myOrderId = Order.objects.all()[0].id
        notifySalesStaff(myOrderId)
