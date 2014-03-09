"""
SANSA-EO Catalogue - MarketSector_model - implements basic CRUD unittests

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

from .model_factories import MarketSectorF


class MarketSectorCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_MarketSector_create(self):
        """
        Tests MarketSector model creation
        """
        myModel = MarketSectorF.create()

        self.assertTrue(myModel.pk is not None)

    def test_MarketSector_delete(self):
        """
        Tests MarketSector model delete
        """
        myModel = MarketSectorF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_MarketSector_read(self):
        """
        Tests MarketSector model read
        """
        myModel = MarketSectorF.create(**{
            'name': 'Decline to say'
        })

        self.assertEqual(myModel.name, 'Decline to say')

    def test_MarketSector_update(self):
        """
        Tests MarketSector model update
        """

        myModel = MarketSectorF.create()

        myModel.__dict__.update({
            'name': 'Decline to say'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Decline to say')

    def test_MarketSector_repr(self):
        """
        Tests MarketSector model representation
        """
        myModel = MarketSectorF.create(**{
            'name': 'Decline to say'
        })

        self.assertEqual(unicode(myModel), 'Decline to say')