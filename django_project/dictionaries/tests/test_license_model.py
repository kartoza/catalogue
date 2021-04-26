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
__version__ = '0.2'
__date__ = '31/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import LicenseF


class LicenseCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_license_create(self):
        """
        Tests License model creation
        """

        myModel = LicenseF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_license_delete(self):
        """
        Tests License model delete
        """
        myModel = LicenseF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_license_read(self):
        """
        Tests License model read
        """

        myModel = LicenseF.create(**{
            'type': 3,
            'name': 'SAC Commercial License',
            'details': 'SAC Commercial License'
        })

        self.assertEqual(myModel.type, 3)
        self.assertEqual(myModel.name, 'SAC Commercial License')
        self.assertEqual(myModel.details, 'SAC Commercial License')

    def test_license_update(self):
        """
        Tests License model update
        """
        myModel = LicenseF.create()

        myModel.__dict__.update({
            'type': 3,
            'name': 'SAC Commercial License',
            'details': 'SAC Commercial License'
        })
        myModel.save()

        self.assertEqual(myModel.type, 3)
        self.assertEqual(myModel.name, 'SAC Commercial License')
        self.assertEqual(myModel.details, 'SAC Commercial License')

    def test_license_repr(self):
        """
        Tests License model representation
        """
        myModel = LicenseF.create(**{
            'name': 'SAC License'
        })

        self.assertEqual(str(myModel), 'SAC License')
