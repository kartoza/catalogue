"""
SANSA-EO Catalogue - FileFormat_model - implements basic CRUD unittests

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

from .model_factories import FileFormatF


class FileFormatCRUD_Test(TestCase):
    """
    Tests models.
    """
    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_FileFormat_create(self):
        """
        Tests FileFormat model creation
        """

        myModel = FileFormatF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_FileFormat_delete(self):
        """
        Tests FileFormat model delete
        """
        myModel = FileFormatF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_FileFormat_read(self):
        """
        Tests FileFormat model read
        """
        myModel = FileFormatF.create(**{
            'name': 'GeoTiff'
        })
        #check if data is correct
        self.assertEqual(myModel.name, 'GeoTiff')

    def test_FileFormat_update(self):
        """
        Tests FileFormat model update
        """
        myModel = FileFormatF.create()

        myModel.__dict__.update({
            'name': 'GeoTiff'
        })

        myModel.save()

        self.assertEqual(myModel.name, 'GeoTiff')

    def test_FileFormat_repr(self):
        """
        Tests FileFormat model representation
        """
        myModel = FileFormatF.create(**{
            'name': 'GeoTiff'
        })

        self.assertEqual(unicode(myModel), 'GeoTiff')
