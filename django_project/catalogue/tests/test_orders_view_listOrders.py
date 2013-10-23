"""
SANSA-EO Catalogue - orders_view_listOrders - Orders views
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

from datetime import date

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from .model_factories import OrderF


class OrdersViews_listOrders_Tests(TestCase):
    """
    Tests orders.py listOrders method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_listOrders_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'listOrders',
                kwargs=myKwargTest)

    def test_listOrders_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('listOrders', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/listorders/')

    def test_listOrders_login_staff(self):
        """
        Test view if staff user is logged in
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'user': myUser})
        OrderF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('listOrders', kwargs={}))
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myUrl'], '/listorders/')

        self.assertEqual(
            myResp.context['myCurrentMonth'], date.today())
        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), 2)

    def test_listOrders_login_user(self):
        """
        Test view if regular user is logged in
        """
        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password',
        })

        OrderF.create(**{'user': myUser})
        OrderF.create()

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('listOrders', kwargs={}))
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myUrl'], '/listorders/')

        self.assertEqual(
            myResp.context['myCurrentMonth'], date.today())
        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), 1)

    def test_listOrders_login_user_page_param_existant(self):
        """
        Test view if user is logged in, specifying page param
        """

        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password',
        })

        OrderF.create(**{'user': myUser})
        OrderF.create()

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('listOrders', kwargs={}),
            {'page': 1})
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myUrl'], '/listorders/')

        self.assertEqual(
            myResp.context['myCurrentMonth'], date.today())
        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), 1)

    def test_listOrders_login_user_page_param_nonexistant(self):
        """
        Test view if user is logged in, specifying page that does not exist
        View will default to page 1
        """
        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password',
        })

        OrderF.create(**{'user': myUser})
        OrderF.create()

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('listOrders', kwargs={}),
            {'page': 1000})
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myUrl'], '/listorders/')

        self.assertEqual(
            myResp.context['myCurrentMonth'], date.today())
        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'menu.html',
            u'useraccounts/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), 1)

    def test_listOrders_login_page_param_invalid_input(self):
        """
        Test view if user is logged in, specifying invalid page parameter
        View will default to page 1
        """
        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password',
        })

        OrderF.create(**{'user': myUser})
        OrderF.create()

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('listOrders', kwargs={}),
            {'page': 'this is a new page!'})
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myUrl'], '/listorders/')

        self.assertEqual(
            myResp.context['myCurrentMonth'], date.today())
        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), 1)

    def test_myOrders_pdf_pageSize(self):
        """
        Test view if pdf is requested
        """
        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password',
        })

        OrderF.create(**{'user': myUser})
        OrderF.create()

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('listOrders', kwargs={}),
            {'pdf': ''})
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myUrl'], '/listorders/')

        self.assertEqual(
            myResp.context['myCurrentMonth'], date.today())
        # check used templates
        myExpTemplates = ['pdf/orderListPage.html', u'pdfpage.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), 1)

        self.assertEqual(myResp['content-type'], 'application/pdf')
        self.assertEqual(
            myResp['content-disposition'], 'attachment; filename=report.pdf')
