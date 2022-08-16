"""
SANSA-EO Catalogue - quality_model - implements basic CRUD unittests

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

from .model_factories import QualityF


class QualityCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_quality_create(self):
        """
        Tests Quality model creation
        """
        myModel = QualityF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_quality_delete(self):
        """
        Tests Quality model delete
        """
        myModel = QualityF.create()

        myModel.delete()

        self.assertTrue(myModel.pk is None)

    def test_quality_read(self):
        """
        Tests Quality model read
        """

        myModel = QualityF.create(**{
            'name': 'Super quality'
        })

        self.assertEqual(myModel.name, 'Super quality')

    def test_quality_update(self):
        """
        Tests Quality model update
        """
        myModel = QualityF.create()

        myModel.__dict__.update({
            'name': 'Super quality'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Super quality')

    def test_quality_repr(self):
        """
        Tests Quality model repr
        """

        myModel = QualityF.create(**{
            'name': 'Super quality'
        })

        self.assertEqual(str(myModel), 'Super quality')
