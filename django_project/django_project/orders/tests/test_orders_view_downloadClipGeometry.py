"""
SANSA-EO Catalogue - orders_view_downloadClipGeometry - Orders views
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

from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from .model_factories import OrderF


class TestOrdersViewsDownloadClipGeometry(TestCase):
    """
    Tests orders.py downloadClipGeometry method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadClipGeometry_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadClipGeometry',
                kwargs=myKwargTest)

    def test_downloadClipGeometry_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadClipGeometry', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)

    def test_downloadClipGeometry_login_staff_shp(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadClipGeometry', kwargs={'theId': 1}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=clip_geometry_order_1.zip')

    def test_downloadClipGeometry_login_staff_kml(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadClipGeometry', kwargs={'theId': 1}),
            {'kml': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kml+xml')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=clip_geometry_order_1.kml')

    def test_downloadClipGeometry_login_staff_kmz(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadClipGeometry', kwargs={'theId': 1}),
            {'kmz': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kmz')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=clip_geometry_order_1.kmz')

    def test_downloadClipGeometry_login_staff_unkformat(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadClipGeometry', kwargs={'theId': 1}),
            {'unkformat': ''})

        self.assertEqual(myResp.status_code, 404)
