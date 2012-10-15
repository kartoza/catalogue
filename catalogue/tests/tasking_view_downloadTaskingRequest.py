"""
SANSA-EO Catalogue - tasking_view_downloadTaskingRequest - Tasking views
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
__date__ = '14/10/2012'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class TaskingViews_downloadTaskingRequest_Tests(TestCase):
    """
    Tests tasking.py downloadTaskingRequest method/view
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

    def test_downloadTaskingRequest_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadTaskingRequest',
                kwargs=myKwargTest)

    def test_downloadTaskingRequest_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                'http://testserver/accounts/login/?next=/'
                'downloadtaskingrequest/1/'))

    def test_downloadTaskingRequest_login_staff_shp(self):
        """
        Test view if staff user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_1.zip')

    def test_downloadTaskingRequest_login_staff_kml(self):
        """
        Test view if staff user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'kml': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kml+xml')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_1.kml')

    def test_downloadTaskingRequest_login_staff_kmz(self):
        """
        Test view if staff user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'kmz': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kmz')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_1.kmz')

    def test_downloadTaskingRequest_login_user(self):
        """
        Test view if regular user is logged in
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 2}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_2.zip')

    def test_downloadTaskingRequest_login_user_notowned(self):
        """
        Test view if regular user is logged in, but not owner of target object
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(myResp['content-type'], 'application/javascript')
        #check the length of returned script
        self.assertEqual(len(myResp.content), 108)

    def test_downloadTaskingRequest_login_staff_notowned(self):
        """
        Test view if staff user is logged in, but not owner of target object
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 2}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_2.zip')

    def test_downloadTaskingRequest_login_staff_invalidrequest(self):
        """
        Test view if staff user is logged in, but using invalid request params
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myTestParams = [{}, {'test': ''}, {'json': ''}]

        for myTestParam in myTestParams:
            myResp = myClient.get(
                reverse('downloadTaskingRequest', kwargs={'theId': 1}),
                myTestParam)

            self.assertEqual(myResp.status_code, 404)
