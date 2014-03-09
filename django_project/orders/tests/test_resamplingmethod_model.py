"""
SANSA-EO Catalogue - ResamplingMethod_model - implements basic CRUD unittests

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
__date__ = '01/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import ResamplingMethodF


class ResamplingMethodCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_ResamplingMethod_create(self):
        """
        Tests ResamplingMethod model creation
        """
        myModel = ResamplingMethodF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_ResamplingMethod_delete(self):
        """
        Tests ResamplingMethod model delete
        """
        myModel = ResamplingMethodF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_ResamplingMethod_read(self):
        """
        Tests ResamplingMethod model read
        """
        myModel = ResamplingMethodF.create(**{
            'name': 'Nearest Neighbour'
        })

        self.assertEqual(myModel.name, 'Nearest Neighbour')

    def test_ResamplingMethod_update(self):
        """
        Tests ResamplingMethod model update
        """

        myModel = ResamplingMethodF.create()

        myModel.__dict__.update({
            'name': 'Nearest Neighbour'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Nearest Neighbour')

    def test_ResamplingMethod_repr(self):
        """
        Tests ResamplingMethod model representation
        """

        myModel = ResamplingMethodF.create(**{
            'name': 'Nearest Neighbour'
        })

        self.assertEqual(unicode(myModel), 'Nearest Neighbour')
