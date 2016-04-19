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
__version__ = '0.2'
__date__ = '19/08/2013'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


from core.model_factories import UserF


class OrdersViews_ordersSummary_Tests(TestCase):
    """
    Tests orders.py ordersSummary method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_ordersSummary_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

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
            '/accounts/signin/?next=/orderssummary/')

    def test_ordersSummary_login_staff(self):
        """
        Test view if user is staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('ordersSummary', kwargs={}))

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(len(myResp.context['myOrderStatus']), 0)
        self.assertEqual(myResp.context['myOrderInstrumentType'], None)
        self.assertEqual(myResp.context['myOrderSatellite'], None)

        # check used templates
        myExpTemplates = [
            'ordersSummary.html', u'base.html',
            u'pipeline/css.html', None, u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
