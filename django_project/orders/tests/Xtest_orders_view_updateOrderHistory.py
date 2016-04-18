"""
SANSA-EO Catalogue - orders_view_updateOrderHistory - Orders views
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


from ..forms import OrderStatusHistoryForm

from core.model_factories import UserF
from .model_factories import (
    OrderF, OrderStatusHistoryF, OrderStatusF
)

from search.tests.model_factories import SearchRecordF


class OrdersViews_updateOrderHistory_Tests(TestCase):
    """
    Tests orders.py updateOrderHistory method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_updateOrderHistory_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'updateOrderHistory',
                kwargs=myKwargTest)

    def test_updateOrderHistory_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('updateOrderHistory', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            '/accounts/signin/?next=/updateorderhistory/')

    def test_updateOrderHistory_login_staff(self):
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
        myResp = myClient.get(
            reverse('updateOrderHistory', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.content, 'You can only access this view from a form POST')

        self.assertEqual(myResp.context, None)

    def test_updateOrderHistory_login_user(self):
        """
        Test view if user is normal user
        """

        UserF.create(**{
            'username': 'pompies',
            'password': 'password',
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('updateOrderHistory', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.content, 'Access denied')

        self.assertEqual(myResp.context, None)

    def test_updateOrderHistory_login_staff_post(self):
        """
        Test view if user is staff, and has valid post
        """

        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOrderStatus_old = OrderStatusF.create(**{
            'id': 2, 'name': 'An Old Order Status'
        })

        OrderStatusF.create(**{
            'id': 1, 'name': 'A New Orrder Status'
        })

        myOrder = OrderF.create(**{
            'id': 1,
            'user': myUser,
            'order_status': myOrderStatus_old
        })

        SearchRecordF.create(**{'order': myOrder})

        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [u'1'], u'notes': [u'simple notes'],
            u'order': [1]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(myResp.context['myOrder'], myOrder)
        # hack ... manually pick latest context on the stack
        self.assertEqual(len(myResp.context[-1]['myRecords']), 1)
        self.assertEqual(myResp.context['myShowSensorFlag'], True)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], True)

        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)

        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(
            myResp.context['myForm'].__class__, OrderStatusHistoryForm)
        self.assertEqual(len(myResp.context['myHistory']), 1)
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')

        # check used templates
        myExpTemplates = [
            u'<Unknown Template>', 'mail/order.txt', u'mail/base.txt',
            'mail/order.html', u'mail/base.html', 'orderPage.html',
            u'base.html', u'pipeline/css.html',
            u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html', u'order.html',
            u'cartContents.html', u'recordHeader.html', u'record.html',
            u'orderStatusHistory.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_updateOrderHistory_login_staff_post_ajax(self):
        """
        Test view if user is staff, and has valid post
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOrderStatus_old = OrderStatusF.create(**{
            'id': 2, 'name': 'An Old Order Status'
        })

        OrderStatusF.create(**{
            'id': 1, 'name': 'A New Orrder Status'
        })

        myOrder = OrderF.create(**{
            'id': 1,
            'user': myUser,
            'order_status': myOrderStatus_old
        })

        SearchRecordF.create(**{'order': myOrder})

        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [u'1'], u'notes': [u'simple notes'],
            u'order': [1]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(myResp.context['myOrder'], myOrder)
        # hack ... manually pick latest context on the stack
        self.assertEqual(len(myResp.context[-1]['myRecords']), 1)
        self.assertEqual(myResp.context['myShowSensorFlag'], True)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], True)

        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)

        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(
            myResp.context['myForm'].__class__, OrderStatusHistoryForm)
        self.assertEqual(len(myResp.context['myHistory']), 1)
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')

        # check used templates
        myExpTemplates = [
            u'<Unknown Template>', 'mail/order.txt', u'mail/base.txt',
            'mail/order.html', u'mail/base.html', 'orderStatusHistory.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_updateOrderHistory_login_staff_post_invalid_order(self):
        """
        Test view if user is staff, and has invalid post (mismatched order)
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'id': 1, 'user': myUser})

        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [u'1'], u'notes': [u'simple notes'],
            u'order': [1331]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 404)

    def test_updateOrderHistory_login_staff_post_invalid_orderstatus(self):
        """
        Test view if user is staff, and has invalid post (mismatched
            orderstatus)
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOrder = OrderF.create(**{'id': 1, 'user': myUser})
        OrderStatusHistoryF.create(**{'order': myOrder})
        SearchRecordF.create(**{'order': myOrder})

        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [-1], u'notes': [u'simple notes'],
            u'order': [1331]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 404)
