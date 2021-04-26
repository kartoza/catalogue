"""
SANSA-EO Catalogue - Clip_model - implements basic CRUD unittests

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
__date__ = '17/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import ClipF


class TestClipCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Clip_create(self):
        """
        Tests Clip model creation
        """
        myModel = ClipF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_Clip_read(self):
        """
        Tests Clip model read
        """
        myExpectedModelData = {
            'image': 'zaSpot2mMosaic2009',
            'status': 'submitted',
            'result_url': 'http://example.com/unittest'
        }
        myModel = ClipF.create()
        #check if data is correct
        for key, val in list(myExpectedModelData.items()):
            self.assertEqual(myModel.__dict__.get(key), val)

        self.assertEqual(
            myModel.geometry.hex,
            '0103000000010000000500000000000000408A314000000000A00740C00000000'
            '000D6344000000000A03440C000000000004F344000000000009741C000000000'
            '00D9314000000000805341C000000000408A314000000000A00740C0'
        )

        self.assertTrue(
            myModel.owner.pk is not None)

    def test_Clip_update(self):
        """
        Tests Clip model update
        """
        myModel = ClipF.create()
        myNewModelData = {
            'guid': '1',
            'image': 'zaSpot2mMosaic2009',
            'geometry': (
                'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 '
                '-34.65, 17.54 -32.05))'),
            'status': 'in process',
            'result_url': 'http://example.com/unittest'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in list(myNewModelData.items()):
            if key != 'geometry':
                self.assertEqual(myModel.__dict__.get(key), val)

        self.assertEqual(
            myModel.geometry.hex,
            '010300000001000000050000000AD7A3703D8A314066666666660640C014AE47E'
            '17AD4344014AE47E17A3440C0CDCCCCCCCC4C3440F6285C8FC29541C0D7A3703D'
            '0AD7314033333333335341C00AD7A3703D8A314066666666660640C0'
        )

    def test_Clip_delete(self):
        """
        Tests Clip model delete
        """
        myModel = ClipF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)
