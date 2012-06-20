"""
SANSA-EO Catalogue - licence_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '08/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import License


class LicenseCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_license.json',
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_license_create(self):
        """
        Tests License model creation
        """
        myLicenseData = {
            'type': 1,
            'name': 'Test license',
            'details': 'This is a test licence'
        }

        myLicense = License(**myLicenseData)
        myLicense.save()

        #check if PK exists
        self.assertTrue(myLicense.pk != None,
            simpleMessage(myLicense.pk, "not None"))

    def test_license_read(self):
        """
        Tests License model read
        """
        myLicensePK = 1
        myExpectedLicenseData = {
            'type': 3,
            'name': 'SAC Commercial License',
            'details': 'SAC Commercial License'
        }

        myLicense = License.objects.get(pk=myLicensePK)
        #check if data is correct
        for key, val in myExpectedLicenseData.items():
            self.assertEqual(myLicense.__dict__.get(key), val,
                simpleMessage(val, myLicense.__dict__.get(key),
                    message='For key "%s"' % key))

    def test_license_update(self):
        """
        Tests License model update
        """
        myLicensePK = 1
        myLicense = License.objects.get(pk=myLicensePK)
        myNewLicenseData = {
            'type': 2,
            'name': 'Test license',
            'details': 'This is a test licence'
        }

        myLicense.__dict__.update(myNewLicenseData)
        myLicense.save()

        #check if updated
        self.assertTrue(myLicense.type == 2, simpleMessage(myLicense.type, 2))
        self.assertTrue(myLicense.name == 'Test license',
            simpleMessage(myLicense.name, 'Test license'))

        self.assertTrue(myLicense.details == 'This is a test licence',
            simpleMessage(myLicense.details, 'This is a test licence'))

    def test_license_delete(self):
        """
        Tests License model delete
        """
        myLicensePK = 1
        myLicense = License.objects.get(pk=myLicensePK)

        myLicense.delete()

        #check if deleted
        self.assertTrue(myLicense.pk is None,
            simpleMessage(myLicense.pk, None))
