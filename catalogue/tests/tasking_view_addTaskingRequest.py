"""
SANSA-EO Catalogue - tasking_view_addTaskingRequest - Tasking views
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

from catalogue.forms import (
    TaskingRequestForm,
    TaskingRequestDeliveryDetailForm,
)

from catalogue.models import (
    TaskingRequest,
    DeliveryDetail
)


class TaskingViews_addTaskingRequest_Tests(TestCase):
    """
    Tests tasking.py addTaskingRequest method/view
    """
    fixtures = [
        'test_user.json',
        'test_sacuserprofile.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_order.json',
        'test_taskingrequest.json',
        'test_resamplingmethod.json',
        'test_projection.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_addTaskingRequest_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'addTaskingRequest',
                kwargs=myKwargTest)

    def test_addTaskingRequest_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('addTaskingRequest', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                'http://testserver/accounts/profile/edit/personal/'
                '?next=/addtaskingrequest/'))

    def test_addTaskingRequest_login_user_with_profile(self):
        """
        Test view if user is logged in, and has valid profile
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('addTaskingRequest', kwargs={}))
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myTitle'], 'Create a new tasking request')
        self.assertEqual(
            myResp.context['mySubmitLabel'], 'Submit Tasking Request')
        self.assertEqual(myResp.context['myTaskingRequestFlag'], True)
        self.assertEqual(
            myResp.context['myTaskingForm'].__class__, TaskingRequestForm)
        self.assertEqual(
            myResp.context['myTaskingDeliveryDetailsForm'].__class__,
            TaskingRequestDeliveryDetailForm)

        self.assertEqual(myResp.context['myLayersList'], (
            '[zaSpot10mMosaic2010,zaSpot10mMosaic2009,zaSpot10mMosaic2008,'
            'zaSpot10mMosaic2007,zaRoadsBoundaries]')
        )
        # check number of elements in a list
        self.assertEqual(len(myResp.context['myLayerDefinitions']), 5)

        # check used templates
        myExpTemplates = [
            'addPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'add.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_addTaskingRequest_login_user_without_profile(self):
        """
        Test view if user is logged in, and has invalid profile
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('addTaskingRequest', kwargs={}))

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                'http://testserver/accounts/profile/edit/personal/'
                '?next=/addtaskingrequest/'))

    def test_addTaskingRequest_login_user_post_valid(self):
        """
        Test view if user is logged in, and has valid profile
        and has posted valid form data
        """
        # get initial counts
        myTaskingRequests_count = len(TaskingRequest.objects.all())
        myDeliveryDetail_count = len(DeliveryDetail.objects.all())
        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'geometry_file': [u''], u'projection': [u'3'],
            u'geometry': [(
            u'SRID=4326;POLYGON((22.807620312583 -32.186801708128,24.345706250'
            '021 -31.776776743422,23.906253125039 -32.261154538247,22.80762031'
            '2583 -32.186801708128))')],
            u'target_date': [u'01-10-2012'], u'notes': [u''], u'ref_id': [u''],
            u'resampling_method': [u'2'],
            u'baseLayers': [u'2m Mosaic 2010 TC'], u'mission_sensor': [u'10'],
            u'delivery_method': [u'1'], u'market_sector': [u'1'],
            u'task_geometry': [u'task_geometry']
        }
        myResp = myClient.post(
            reverse('addTaskingRequest', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], 'http://testserver/viewtaskingrequest/4')

        # check if tasking request is in the database
        myNewTaskingRequests_count = len(TaskingRequest.objects.all())
        self.assertEqual(
            myNewTaskingRequests_count, myTaskingRequests_count + 1)

        myNewDeliveryDetail_count = len(DeliveryDetail.objects.all())
        self.assertEqual(
            myNewDeliveryDetail_count, myDeliveryDetail_count + 1)

    def test_addTaskingRequest_login_user_post_invalid(self):
        """
        Test view if user is logged in, and has valid profile
        and has posted invalid form data
        """

        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'target_date': [u'01-10-2012']
        }
        myResp = myClient.post(
            reverse('addTaskingRequest', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

                # check response object
        self.assertEqual(
            myResp.context['myTitle'], 'Create a new tasking request')
        self.assertEqual(
            myResp.context['mySubmitLabel'], 'Submit Tasking Request')
        self.assertEqual(myResp.context['myTaskingRequestFlag'], True)
        self.assertEqual(
            myResp.context['myTaskingForm'].__class__, TaskingRequestForm)
        self.assertEqual(
            myResp.context['myTaskingDeliveryDetailsForm'].__class__,
            TaskingRequestDeliveryDetailForm)

        self.assertEqual(myResp.context['myLayersList'], (
            '[zaSpot10mMosaic2010,zaSpot10mMosaic2009,zaSpot10mMosaic2008,'
            'zaSpot10mMosaic2007,zaRoadsBoundaries]')
        )
        # check number of elements in a list
        self.assertEqual(len(myResp.context['myLayerDefinitions']), 5)

        # check used templates
        myExpTemplates = [
            'addPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'add.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_addTaskingRequest_login_user_post_valid_geomfile(self):
        """
        Test view if user is logged in, and has valid profile
        and has posted valid form data, with geomfile
        """
        # get initial counts
        myTaskingRequests_count = len(TaskingRequest.objects.all())
        myDeliveryDetail_count = len(DeliveryDetail.objects.all())

        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area.zip', 'rb')
        #myUploadFile.close()
        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'geometry_file': myUploadFile, u'projection': [u'3'],
            u'geometry': [],
            u'target_date': [u'01-10-2012'], u'notes': [u''], u'ref_id': [u''],
            u'resampling_method': [u'2'],
            u'baseLayers': [u'2m Mosaic 2010 TC'], u'mission_sensor': [u'10'],
            u'delivery_method': [u'1'], u'market_sector': [u'1'],
            u'task_geometry': [u'task_geometry']
        }
        myResp = myClient.post(
            reverse('addTaskingRequest', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], 'http://testserver/viewtaskingrequest/4')

        # check if tasking request is in the database
        myNewTaskingRequests_count = len(TaskingRequest.objects.all())
        self.assertEqual(
            myNewTaskingRequests_count, myTaskingRequests_count + 1)

        myNewDeliveryDetail_count = len(DeliveryDetail.objects.all())
        self.assertEqual(
            myNewDeliveryDetail_count, myDeliveryDetail_count + 1)

    def test_addTaskingRequest_login_user_post_invalid_geomfile(self):
        """
        Test view if user is logged in, and has valid profile
        and has posted valid form data, with invalid geomfile
        """
        # get initial counts
        # myTaskingRequests_count = len(TaskingRequest.objects.all())
        # myDeliveryDetail_count = len(DeliveryDetail.objects.all())

        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area-invalid.zip', 'rb')
        #myUploadFile.close()
        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'geometry_file': myUploadFile, u'projection': [u'3'],
            u'geometry': [],
            u'target_date': [u'01-10-2012'], u'notes': [u''], u'ref_id': [u''],
            u'resampling_method': [u'2'],
            u'baseLayers': [u'2m Mosaic 2010 TC'], u'mission_sensor': [u'10'],
            u'delivery_method': [u'1'], u'market_sector': [u'1'],
            u'task_geometry': [u'task_geometry']
        }
        myResp = myClient.post(
            reverse('addTaskingRequest', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

                # check response object
        self.assertEqual(
            myResp.context['myTitle'], 'Create a new tasking request')
        self.assertEqual(
            myResp.context['mySubmitLabel'], 'Submit Tasking Request')
        self.assertEqual(myResp.context['myTaskingRequestFlag'], True)
        self.assertEqual(
            myResp.context['myTaskingForm'].__class__, TaskingRequestForm)
        self.assertEqual(
            myResp.context['myTaskingDeliveryDetailsForm'].__class__,
            TaskingRequestDeliveryDetailForm)

        self.assertEqual(myResp.context['myLayersList'], (
            '[zaSpot10mMosaic2010,zaSpot10mMosaic2009,zaSpot10mMosaic2008,'
            'zaSpot10mMosaic2007,zaRoadsBoundaries]')
        )
        # check number of elements in a list
        self.assertEqual(len(myResp.context['myLayerDefinitions']), 5)

        # check used templates
        myExpTemplates = [
            'addPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'add.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)
