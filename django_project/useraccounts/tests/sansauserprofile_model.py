'''
SANSA-EO Catalogue - SacUserProfile_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

'''

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '10/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from ..models import SansaUserProfile


class SansaUserProfileCRUD_Test(TestCase):
    '''
    Tests models.
    '''
    fixtures = [
        'test_user.json',
        'test_sansauserprofile.json'
    ]

    def setUp(self):
        '''
        Sets up before each test
        '''
        pass

    def test_SansaUserProfile_create(self):
        '''
        Tests SansaUserProfile model creation
        '''
        myNewData = {
            'about': '',
            'post_code': '123',
            'strategic_partner': False,
            'url': '',
            'address2': 'kjkj',
            'address3': '',
            'address4': '',
            'contact_no': '123123',
            'address1': '12321 kjk',
            'organisation': 'None',
            'user_id': 999
        }
        myModel = SansaUserProfile(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(
            myModel.pk is not None,
            simpleMessage(
                myModel.pk, 'not None',
                message='Model PK should NOT equal None')
        )

    def test_SansaUserProfile_read(self):
        '''
        Tests SansaUserProfile model read
        '''
        myModelPK = 1
        myExpectedModelData = {
            'about': '',
            'post_code': '123',
            'strategic_partner': False,
            'url': '',
            'address2': 'kjkj',
            'address3': '',
            'address4': '',
            'contact_no': '123123',
            'address1': '12321 kjk',
            'organisation': 'None',
            'user_id': 1
        }

        myModel = SansaUserProfile.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(
                myModel.__dict__.get(key), val,
                simpleMessage(
                    myModel.__dict__.get(key), val,
                    message='For key %s' % key))

    def test_SansaUserProfile_update(self):
        '''
        Tests SansaUserProfile model update
        '''
        myModelPK = 1
        myModel = SansaUserProfile.objects.get(pk=myModelPK)
        myNewModelData = {
            'about': '',
            'post_code': '123123',
            'surname': 'Sutton',
            'strategic_partner': False,
            'firstname': 'Tim',
            'url': '',
            'country': None,
            'address2': 'kjkj',
            'address3': '',
            'address4': '',
            'longitude': None,
            'contact_no': '123123',
            'latitude': None,
            'location': '',
            'address1': '12321 kjk',
            'date': '2012-07-09 14:14:08',
            'organisation': 'None',
            'user_id': 999
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(
                myModel.__dict__.get(key), val,
                simpleMessage(
                    myModel.__dict__.get(key), val,
                    message='For key %s' % key))

    def test_SansaUserProfile_delete(self):
        '''
        Tests SansaUserProfile model delete
        '''
        myModelPK = 1
        myModel = SansaUserProfile.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(
            myModel.pk is None,
            simpleMessage(
                myModel.pk, None,
                message='Model PK should equal None'))
