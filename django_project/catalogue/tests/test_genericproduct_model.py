"""
SANSA-EO Catalogue - genericproduct_model - implements basic CRUD unittests

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
__date__ = '25/07/2013'
__copyright__ = 'South African National Space Agency'

from datetime import datetime

from django.test import TestCase

from .model_factories import GenericProductF


class TestGenericProductCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_genericproduct_create(self):
        """
        Tests GenericProduct model creation
        """

        myModel = GenericProductF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_genericproduct_delete(self):
        """
        Tests GenericProduct model delete
        """
        myModel = GenericProductF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_genericproduct_read(self):
        """
        Tests GenericProduct model read
        """

        myModel = GenericProductF.create(**{
            u'product_date': datetime.strptime(
                '1987-04-28 08:46:32', '%Y-%m-%d %H:%M:%S'),
            u'spatial_coverage': (
                u'POLYGON ((21.3566000000000145 -27.2013999999999783, '
                '21.4955000000000496 -26.6752999999999929, 22.0914000000000215'
                ' -26.7661999999999978, 21.9554000000000542 '
                '-27.2926999999999964, 21.3566000000000145 '
                '-27.2013999999999783))'),
            u'unique_product_id': (
                u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'),
            u'remote_thumbnail_url': u'http://sirius.spotimage.fr/',
            u'original_product_id': u'11204048606190846322X',
        })

        self.assertEqual(str(myModel.product_date), '1987-04-28 08:46:32')

        self.assertEqual(myModel.spatial_coverage.hex, (
            '01030000000100000005000000F0C039234A5B3540106A4DF38E333BC0102B871'
            '6D97E354020FDF675E0AC3AC0C0DA8AFD65173640F831E6AE25C43AC040992A18'
            '95F43540088A1F63EE4A3BC0F0C039234A5B3540106A4DF38E333BC0')
        )

        self.assertEqual(myModel.unique_product_id, (
            u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'))

    def test_genericproduct_update(self):
        """
        Tests GenericProduct model update
        """

        myModel = GenericProductF.create()

        myNewModelData = {
            u'product_date': datetime.strptime(
                '1987-04-28 08:46:32', '%Y-%m-%d %H:%M:%S'),
            u'spatial_coverage': (
                u'POLYGON ((21.3566000000000145 -27.2013999999999783, '
                '21.4955000000000496 -26.6752999999999929, 22.0914000000000215'
                ' -26.7661999999999978, 21.9554000000000542 '
                '-27.2926999999999964, 21.3566000000000145 '
                '-27.2013999999999783))'),
            # u'projection': 89, u'license': 1, u'quality': 1,
            # u'creating_software': 1,
            u'unique_product_id': (
                u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'),
            u'remote_thumbnail_url': u'http://sirius.spotimage.fr/',
            u'product_revision': None,  # u'owner': 1,
            u'original_product_id': u'11204048606190846322X',
            # u'processing_level': 2,
            u'local_storage_path': None
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        self.assertEqual(str(myModel.product_date), '1987-04-28 08:46:32')

        self.assertEqual(myModel.spatial_coverage.hex, (
            '01030000000100000005000000F0C039234A5B3540106A4DF38E333BC0102B871'
            '6D97E354020FDF675E0AC3AC0C0DA8AFD65173640F831E6AE25C43AC040992A18'
            '95F43540088A1F63EE4A3BC0F0C039234A5B3540106A4DF38E333BC0')
        )

        self.assertEqual(myModel.unique_product_id, (
            u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'))

    def test_genericproduct_repr(self):
        """
        Tests GenericProduct model representation
        """

        myModel = GenericProductF.create(**{
            u'product_date': datetime.strptime(
                '1987-04-28 08:46:32', '%Y-%m-%d %H:%M:%S'),
            u'spatial_coverage': (
                u'POLYGON ((21.3566000000000145 -27.2013999999999783, '
                '21.4955000000000496 -26.6752999999999929, 22.0914000000000215'
                ' -26.7661999999999978, 21.9554000000000542 '
                '-27.2926999999999964, 21.3566000000000145 '
                '-27.2013999999999783))'),
            u'unique_product_id': (
                u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'),
            u'remote_thumbnail_url': u'http://sirius.spotimage.fr/',
            u'original_product_id': u'11204048606190846322X',
        })

        myExpResult = (
            u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-')

        self.assertEqual(unicode(myModel), myExpResult)

    def test_genericproduct_tidySacId(self):
        """
        Tests GenericProduct model tidySacId
        """
        myModel = GenericProductF.create(**{
            u'product_date': datetime.strptime(
                '1987-04-28 08:46:32', '%Y-%m-%d %H:%M:%S'),
            u'spatial_coverage': (
                u'POLYGON ((21.3566000000000145 -27.2013999999999783, '
                '21.4955000000000496 -26.6752999999999929, 22.0914000000000215'
                ' -26.7661999999999978, 21.9554000000000542 '
                '-27.2926999999999964, 21.3566000000000145 '
                '-27.2013999999999783))'),
            u'unique_product_id': (
                u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'),
            u'remote_thumbnail_url': u'http://sirius.spotimage.fr/',
            u'original_product_id': u'11204048606190846322X',
        })

        myExpResult = u'11204048606190846322X'

        self.assertEqual(myModel.tidySacId(), myExpResult),

    def test_genericproduct_getUTMZones(self):
        """
        Tests GenericProduct model getUTMZones
        """

        myModel = GenericProductF.create(**{
            u'product_date': datetime.strptime(
                '1987-04-28 08:46:32', '%Y-%m-%d %H:%M:%S'),
            u'spatial_coverage': (
                u'POLYGON ((21.3566000000000145 -27.2013999999999783, '
                '21.4955000000000496 -26.6752999999999929, 22.0914000000000215'
                ' -26.7661999999999978, 21.9554000000000542 '
                '-27.2926999999999964, 21.3566000000000145 '
                '-27.2013999999999783))'),
            u'unique_product_id': (
                u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'),
            u'remote_thumbnail_url': u'http://sirius.spotimage.fr/',
            u'original_product_id': u'11204048606190846322X',
        })

        myRes = myModel.getUTMZones()
        self.assertEqual(myRes, [('32734', 'UTM34S')])
