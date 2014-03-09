"""
SANSA-EO Catalogue - OrderNotificationRecipients_model - implements basic CRUD
unittests

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

from django.contrib.contenttypes.models import ContentType

from core.model_factories import UserF

from dictionaries.tests.model_factories import (
    SatelliteF, InstrumentTypeF, SatelliteInstrumentGroupF,
    OpticalProductProfileF, SatelliteInstrumentF
)

from catalogue.tests.model_factories import OpticalProductF

from .model_factories import OrderNotificationRecipientsF

from ..models import OrderNotificationRecipients


class OrderNotificationRecipientsCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OrderNotificationRecipients_create(self):
        """
        Tests OrderNotificationRecipients model creation
        """
        myModel = OrderNotificationRecipientsF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_OrderNotificationRecipients_delete(self):
        """
        Tests OrderNotificationRecipients model delete
        """
        myModel = OrderNotificationRecipientsF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_OrderNotificationRecipients_read(self):
        """
        Tests OrderNotificationRecipients model read
        """
        myUser = UserF.create(**{
            'username': 'Samsung'
        })
        myModel = OrderNotificationRecipientsF.create(**{
            'user': myUser
        })

        self.assertEqual(myModel.user.username, 'Samsung')

    def test_OrderNotificationRecipients_update(self):
        """
        Tests OrderNotificationRecipients model update
        """

        myUser = UserF.create(**{
            'username': 'Samsung'
        })
        myModel = OrderNotificationRecipientsF.create()

        myModel.user = myUser

        myModel.save()

        self.assertEqual(myModel.user.username, 'Samsung')

    def test_OrderNotificationRecipients_repr(self):
        """
        Tests OrderNotificationRecipients model repr
        """
        myUser = UserF.create(**{
            'username': 'Samsung'
        })
        myModel = OrderNotificationRecipientsF.create(**{
            'user': myUser
        })

        self.assertEqual(unicode(myModel), 'Samsung')

    def test_OrderNotificationRecipients_getUsersForProduct(self):
        """
        Tests OrderNotificationRecipients model getUsersForProduct method
        """
        myUser = UserF.create(**{
            'username': 'Samsung'
        })

        myOtherUser = UserF.create(**{
            'username': 'Sony'
        })

        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'ITOP 1'
        })
        mySatellite = SatelliteF.create(**{
            'operator_abbreviation': 'ST 1'
        })

        mySatInstGroup = SatelliteInstrumentGroupF.create(**{
            'instrument_type': myInstType,
            'satellite': mySatellite
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInstGroup
        })

        myOPP = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst
        })

        # first user is registered to a product
        myProduct = OpticalProductF.create(**{
            'product_profile': myOPP
        })

        myContentType = ContentType.objects.get_for_model(myProduct.__class__)

        OrderNotificationRecipientsF.create(**{
            'user': myUser,
            'add_classes': [myContentType]
        })

        # second user is registered to a sat_inst_group

        OrderNotificationRecipientsF.create(**{
            'user': myOtherUser,
            'add_satellite_instrument_groups': [mySatInstGroup]
        })

        self.assertEqual(
            len(OrderNotificationRecipients.getUsersForProduct(myProduct)),
            2
        )
