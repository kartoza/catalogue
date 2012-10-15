"""
SANSA-EO Catalogue - shopping_cart_view_downloadCartMetadata - Shopping cart
    views unittests

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
__date__ = '15/10/2012'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class ShoppingCart_downloadCartMetadata_Tests(TestCase):
    """
    Tests tasking.py downloadCartMetadata method/view
    """

    fixtures = [
        'test_user.json',
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
        'test_user.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadCartMetadata_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'theId': 'testtest'}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadCartMetadata',
                kwargs=myKwargTest)

    def test_downloadCartMetadata_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadCartMetadata', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/downloadcartmetadata/')

    def test_downloadCartMetadata_login_staff(self):
        """
        Test view if user is staff
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('downloadCartMetadata', kwargs={}), {})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=SANSA-Cart-timlinux-Metadata.zip')

    def test_downloadCartMetadata_login_staff_html(self):
        """
        Test view if user is staff, html param
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadCartMetadata', kwargs={}),
            {'html': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=SANSA-Cart-timlinux-Metadata.zip')
