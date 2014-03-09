"""
SANSA-EO Catalogue - projection_model - implements basic CRUD unittests

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
__date__ = '01/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import ProjectionF


class ProjectionCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_projection_create(self):
        """
        Tests Projection model creation
        """
        myModel = ProjectionF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_projection_delete(self):
        """
        Tests Projection model delete
        """
        myModel = ProjectionF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_projection_read(self):
        """
        Tests Projection model read
        """
        myModel = ProjectionF.create(**{
            'name': 'Flatland projection',
            'epsg_code': 13377331
        })

        self.assertEqual(myModel.name, 'Flatland projection')
        self.assertEqual(myModel.epsg_code, 13377331)

    def test_projection_update(self):
        """
        Tests Projection model update
        """
        myModel = ProjectionF.create()

        myModel.__dict__.update({
            'name': 'Flatland projection',
            'epsg_code': 13377331
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Flatland projection')
        self.assertEqual(myModel.epsg_code, 13377331)

    def test_projection_repr(self):
        """
        Tests Projection model repr
        """
        myModel = ProjectionF.create(**{
            'name': 'Flatland projection',
            'epsg_code': 13377331
        })

        self.assertEqual(
            unicode(myModel), 'EPSG: 13377331 Flatland projection')
