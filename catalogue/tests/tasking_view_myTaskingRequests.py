"""
SANSA-EO Catalogue - tasking_view_myTaskingRequests - Tasking views unittests

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
__date__ = '14/10/2012'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class TaskingViews_myTaskingRequests_Tests(TestCase):
    """
    Tests tasking.py myTaskingRequests method/view
    """
    fixtures = [
        'test_user.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_missionsensor.json',
        'test_order.json',
        'test_taskingrequest.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_myTaskingRequests_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'myTaskingRequests',
                kwargs=myKwargTest)

    def test_myTaskingRequests_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('myTaskingRequests', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/mytaskingrequests/')

    def test_myTaskingRequests_login(self):
        """
        Test view if user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myTaskingRequests', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], 'mytaskingrequests')

        # check used templates
        myExpTemplates = [
            'taskingRequestPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

    def test_myTaskingRequests_login_ajax(self):
        """
        Test view if user is logged in, if the request is an AJAX request
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myTaskingRequests', kwargs={}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], 'mytaskingrequests')

        # check used templates
        myExpTemplates = 'taskingRequestList.html'
        myUsedTemplates = myResp.template.name
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

    def test_myTaskingRequests_login_page_param_existant(self):
        """
        Test view if user is logged in, specifying page param
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myTaskingRequests', kwargs={}),
            {'page': '1'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], 'mytaskingrequests')

        # check used templates
        myExpTemplates = [
            'taskingRequestPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

    def test_myTaskingRequests_login_page_param_nonexistant(self):
        """
        Test view if user is logged in, specifying page that does not exist
        View will default to page 1
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myTaskingRequests', kwargs={}),
            {'page': '1000'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], 'mytaskingrequests')

        # check used templates
        myExpTemplates = [
            'taskingRequestPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

    def test_myTaskingRequests_login_page_param_invalid_input(self):
        """
        Test view if user is logged in, specifying invalid page parameter
        View will default to page 1
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myTaskingRequests', kwargs={}),
            {'page': 'this is a new page'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], 'mytaskingrequests')

        # check used templates
        myExpTemplates = [
            'taskingRequestPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)
