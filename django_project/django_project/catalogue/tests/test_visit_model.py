"""
SANSA-EO Catalogue - Visit_model - implements basic CRUD unittests

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

from .model_factories import VisitF


class VisitCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Visit_create(self):
        """
        Tests Visit model creation
        """
        myModel = VisitF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_Visit_delete(self):
        """
        Tests Visit model delete
        """
        myModel = VisitF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Visit_read(self):
        """
        Tests Visit model read
        """

        myModel = VisitF.create(**{
            'city': 'Unknown city',
            'country': 'Unknown conutry',
            'ip_address': '10.10.10.10',
            'ip_position': 'POINT(28.2294006347656 -25.7068996429443)'
        })

        self.assertEqual(myModel.city, 'Unknown city')
        self.assertEqual(myModel.country, 'Unknown conutry')
        self.assertEqual(myModel.ip_address, '10.10.10.10')
        self.assertEqual(
            myModel.ip_position.hex,
            '0101000000F9FFFFFFB93A3C40F6FFFF5FF7B439C0'
        )

    def test_Visit_update(self):
        """
        Tests Visit model update
        """
        myModel = VisitF.create()

        myModel.__dict__.update({
            'city': 'Unknown city',
            'country': 'Unknown conutry',
            'ip_address': '10.10.10.10',
            'ip_position': 'POINT(28.2294006347656 -25.7068996429443)'
        })
        myModel.save()

        self.assertEqual(myModel.city, 'Unknown city')
        self.assertEqual(myModel.country, 'Unknown conutry')
        self.assertEqual(myModel.ip_address, '10.10.10.10')
        self.assertEqual(
            myModel.ip_position.hex,
            '0101000000F9FFFFFFB93A3C40F6FFFF5FF7B439C0'
        )
