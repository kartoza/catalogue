"""
SANSA-EO Catalogue - Dictionaries SpectralGroup - basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '23/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import SpectralGroupF


class TestSpectralGroupCRUD(TestCase):
    """
    Tests SpectralGroup model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_SpectralGroup_create(self):
        """
        Tests SpectralGroup model creation
        """
        myModel = SpectralGroupF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SpectralGroup_delete(self):
        """
        Tests SpectralGroup model delete
        """
        myModel = SpectralGroupF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SpectralGroup_read(self):
        """
        Tests SpectralGroup model read
        """

        myModel = SpectralGroupF.create(**{
            'name': 'New Spectral Group',
            'description': 'No description',
            'abbreviation': 'NSG'
        })

        self.assertEqual(myModel.name, 'New Spectral Group')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NSG')

    def test_SpectralGroup_update(self):
        """
        Tests SpectralGroup model update
        """

        myModel = SpectralGroupF.create()

        myModel.__dict__.update(**{
            'name': 'New Spectral Group',
            'description': 'No description',
            'abbreviation': 'NSG'
        })

        myModel.save()

        self.assertEqual(myModel.name, 'New Spectral Group')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NSG')

    def test_SpectralGroup_repr(self):
        """
        Tests SpectralGroup model repr
        """

        myModel = SpectralGroupF.create(**{
            'name': 'New Spectral Group'
        })

        self.assertEqual(
            str(myModel), 'New Spectral Group')
