"""
SANSA-EO Catalogue - orders_view_viewOrder - Orders views
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
__date__ = '14/08/2013'
__copyright__ = 'South African National Space Agency'

from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


from orders.forms import OrderStatusHistoryForm

from core.model_factories import UserF
from search.tests.model_factories import SearchRecordF
from model_factories import OrderF, OrderStatusHistoryF


class TestOrdersViewsViewOrder(TestCase):
    """
    Tests orders.py viewOrder method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_viewOrder_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'viewOrder',
                kwargs=myKwargTest)

    def test_viewOrder_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            '/accounts/signin/?next=/vieworder/1/')

    def test_viewOrder_login_staff(self):
        """
        Test view if user is staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOrder = OrderF.create(**{'id': 1})
        OrderStatusHistoryF.create(**{'order': myOrder})

        SearchRecordF.create(**{'order': myOrder})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('viewOrder', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(myResp.context['myOrder'], myOrder)
        self.assertEqual(len(myResp.context['myRecords']), 1)
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(myResp.context['myDownloadOrderFlag'], True)
        self.assertEqual(
            myResp.context['myForm'].__class__, OrderStatusHistoryForm)

        self.assertEqual(len(myResp.context['myHistory']), 1)
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')
        self.assertEqual(myResp.context['myCoverage'], {
            'CentroidZone': 'UTM34S (EPSG:32734)', 'ProductArea': 79894321621
        })

        # check used templates
        myExpTemplates = [
            'orderPage.html', 'base.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html',
            'useraccounts/menu_content.html', 'order.html',
            'cartContents.html', 'recordHeader.html', 'record.html',
            'orderStatusHistory.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_viewOrder_login_user(self):
        """
        Test view if user is normal user
        """

        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        myOrder = OrderF.create(**{'id': 1, 'user': myUser})
        OrderStatusHistoryF.create(**{'order': myOrder})

        SearchRecordF.create(**{'order': myOrder})

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(myResp.context['myOrder'], myOrder)
        self.assertEqual(len(myResp.context['myRecords']), 1)
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(myResp.context['myDownloadOrderFlag'], True)
        self.assertEqual(myResp.context['myForm'], None)
        self.assertEqual(len(myResp.context['myHistory']), 1)
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')
        self.assertEqual(myResp.context['myCoverage'], {
            'CentroidZone': 'UTM34S (EPSG:32734)', 'ProductArea': 79894321621
        })

        # check used templates
        myExpTemplates = [
            'orderPage.html', 'base.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html',
            'useraccounts/menu_content.html', 'order.html',
            'cartContents.html', 'recordHeader.html', 'record.html',
            'orderStatusHistory.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_viewOrder_login_user_notowned(self):
        """
        Test view if user is normal user, not owned order
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })
        OrderF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 404)

    def test_showCartContents_login_staff_ajax(self):
        """
        Test view if user is staff, and request is ajax
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOrder = OrderF.create(**{'id': 1})
        OrderStatusHistoryF.create(**{'order': myOrder})

        SearchRecordF.create(**{'order': myOrder})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': 1}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(myResp.context['myOrder'], myOrder)
        self.assertEqual(len(myResp.context['myRecords']), 1)
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(myResp.context['myDownloadOrderFlag'], True)
        self.assertEqual(
            myResp.context['myForm'].__class__, OrderStatusHistoryForm)
        self.assertEqual(len(myResp.context['myHistory']), 1)
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')
        self.assertEqual(myResp.context['myCoverage'], {
            'CentroidZone': 'UTM34S (EPSG:32734)', 'ProductArea': 79894321621
        })
        # check used templates
        myExpTemplates = [
            'orderPageAjax.html', 'emptytemplate.html', 'order.html',
            'cartContents.html', 'recordHeader.html', 'record.html',
            'orderStatusHistory.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
