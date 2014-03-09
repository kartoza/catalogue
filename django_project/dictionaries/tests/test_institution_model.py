"""
SANSA-EO Catalogue - institution_model - implements basic CRUD unittests

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

from model_factories import InstitutionF


class InstitutionCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_institution_create(self):
        """
        Tests Institution model creation
        """
        myModel = InstitutionF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_institution_delete(self):
        """
        Tests Institution model delete
        """
        myModel = InstitutionF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_institution_read(self):
        """
        Tests Institution model read
        """
        myModel = InstitutionF.create(**{
            'address1': 'Hartebeeshoek',
            'address2': 'Gauteng',
            'address3': 'South Africa',
            'name': 'Satellite Applications Centre',
            'post_code': '0000'
        })

        self.assertEqual(myModel.address1, 'Hartebeeshoek')
        self.assertEqual(myModel.address2, 'Gauteng')
        self.assertEqual(myModel.address3, 'South Africa')
        self.assertEqual(myModel.name, 'Satellite Applications Centre')
        self.assertEqual(myModel.post_code, '0000')

    def test_institution_update(self):
        """
        Tests Institution model update
        """
        myModel = InstitutionF.create()

        myModel.__dict__.update({
            'address1': 'Hartebeeshoek',
            'address2': 'Gauteng',
            'address3': 'South Africa',
            'name': 'Satellite Applications Centre',
            'post_code': '0000'
        })
        myModel.save()

        self.assertEqual(myModel.address1, 'Hartebeeshoek')
        self.assertEqual(myModel.address2, 'Gauteng')
        self.assertEqual(myModel.address3, 'South Africa')
        self.assertEqual(myModel.name, 'Satellite Applications Centre')
        self.assertEqual(myModel.post_code, '0000')

    def test_Institution_repr(self):
        """
        Tests Institution model representation
        """
        myModel = InstitutionF.create(**{
            'name': 'Satellite Applications Centre'
        })

        self.assertEqual(unicode(myModel), 'Satellite Applications Centre')
