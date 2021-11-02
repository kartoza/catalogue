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
__version__ = '0.2'
__date__ = '09/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from core.model_factories import UserF
from model_factories import SansaUserProfileF


class TestSansaUserProfileCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SansaUserProfile_create(self):
        """
        Tests SansaUserProfile model creation
        """
        myModel = SansaUserProfileF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SansaUserProfile_delete(self):
        """
        Tests SansaUserProfile model delete
        """
        myModel = SansaUserProfileF.create()

        myModel.delete()

        # check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SansaUserProfile_read(self):
        """
        Tests SansaUserProfile model read
        """

        myModel = SansaUserProfileF.create(**{
            'about': '',
            'post_code': '123',
            'strategic_partner': False,
            'url': '',
            'address2': 'kjkj',
            'address3': '',
            'address4': '',
            'contact_no': '123123',
            'address1': '12321 kjk',
            'organisation': 'None'
        })

        self.assertEqual(myModel.about, '')
        self.assertEqual(myModel.post_code, '123')
        self.assertEqual(myModel.strategic_partner, False)
        self.assertEqual(myModel.url, '')
        self.assertEqual(myModel.address2, 'kjkj')
        self.assertEqual(myModel.address3, '')
        self.assertEqual(myModel.address4, '')
        self.assertEqual(myModel.contact_no, '123123')
        self.assertEqual(myModel.address1, '12321 kjk')
        self.assertEqual(myModel.organisation, 'None')

    def test_SansaUserProfile_update(self):
        """
        Tests SansaUserProfile model update
        """
        myModel = SansaUserProfileF.create()

        myModel.__dict__.update({
            'about': '',
            'post_code': '123',
            'strategic_partner': False,
            'url': '',
            'address2': 'kjkj',
            'address3': '',
            'address4': '',
            'contact_no': '123123',
            'address1': '12321 kjk',
            'organisation': 'None'
        })
        myModel.save()

        self.assertEqual(myModel.about, '')
        self.assertEqual(myModel.post_code, '123')
        self.assertEqual(myModel.strategic_partner, False)
        self.assertEqual(myModel.url, '')
        self.assertEqual(myModel.address2, 'kjkj')
        self.assertEqual(myModel.address3, '')
        self.assertEqual(myModel.address4, '')
        self.assertEqual(myModel.contact_no, '123123')
        self.assertEqual(myModel.address1, '12321 kjk')
        self.assertEqual(myModel.organisation, 'None')

    def test_SansaUserProfile_properties(self):
        """
        Tests SansaUserProfile model properties
        """
        myUser = UserF.create(**{
            'first_name': 'Tim',
            'last_name': 'Cetina'
        })
        myModel = SansaUserProfileF.create(**{
            'user': myUser
        })

        self.assertEqual(myModel.first_name(), 'Tim')
        self.assertEqual(myModel.last_name(), 'Cetina')

    def test_SansaUserProfile_repr(self):
        """
        Tests SansaUserProfile repr
        """
        myUser = UserF.create(**{
            'username': 'tcetina',
            'first_name': 'Tim',
            'last_name': 'Cetina'
        })
        myModel = SansaUserProfileF.create(**{
            'user': myUser
        })

        self.assertEqual(str(myModel), 'tcetina, (Tim Cetina)')
