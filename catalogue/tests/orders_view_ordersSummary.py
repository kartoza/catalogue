"""
SANSA-EO Catalogue - orders_view_ordersSummary - Orders views
    unittests

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
__date__ = '23/10/2012'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from django.db.models import Count

from catalogue.models import (
    OrderStatus,
    MissionSensor
)


class OrdersViews_ordersSummary_Tests(TestCase):
    """
    Tests orders.py ordersSummary method/view
    """

    fixtures = [
        'test_mission.json',
        'test_missionsensor.json',
        # 'test_search.json',
        # 'test_searchdaterange.json',
        # 'test_processinglevel.json',
        # 'test_sensortype.json',
        # 'test_acquisitionmode.json',
        # 'test_genericproduct.json',
        # 'test_genericimageryproduct.json',
        # 'test_genericsensorproduct.json',
        # 'test_opticalproduct.json',
        'test_user.json',
        'test_orderstatus.json',
        'test_orderstatushistory.json',
        'test_marketsector.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_ordersSummary_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'ordersSummary',
                kwargs=myKwargTest)

    def test_ordersSummary_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('ordersSummary', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/orderssummary/')

    def test_ordersSummary_login_staff(self):
        """
        Test view if user is staff
        """
        myOrderStatusObj = OrderStatus.objects.annotate(
            num_orders=Count('order__id'))

        myOrderProductTypeObj = MissionSensor.objects.annotate(
            num_orders=Count('taskingrequest__order_ptr__id'))

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('ordersSummary', kwargs={}))

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            len(myResp.context['myOrderStatus']), len(myOrderStatusObj))
        self.assertEqual(
            len(myResp.context['myOrderProductType']),
            len(myOrderProductTypeObj))

        # check used templates
        myExpTemplates = [
            'ordersSummary.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)
