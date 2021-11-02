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

from model_factories import OrderNotificationRecipientsF

from orders.models import OrderNotificationRecipients


class TestOrderNotificationRecipientsCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_order_notification_recipients_create(self):
        """
        Tests OrderNotificationRecipients model creation
        """
        model = OrderNotificationRecipientsF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_order_notification_recipients_delete(self):
        """
        Tests OrderNotificationRecipients model delete
        """
        model = OrderNotificationRecipientsF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_order_notification_recipients_read(self):
        """
        Tests OrderNotificationRecipients model read
        """
        user = UserF.create(**{
            'username': 'Samsung'
        })
        model = OrderNotificationRecipientsF.create(**{
            'user': user
        })

        self.assertEqual(model.user.username, 'Samsung')

    def test_order_notification_recipients_update(self):
        """
        Tests OrderNotificationRecipients model update
        """

        user = UserF.create(**{
            'username': 'Samsung'
        })
        model = OrderNotificationRecipientsF.create()
        model.user = user
        model.save()
        self.assertEqual(model.user.username, 'Samsung')

    def test_order_notification_recipients_repr(self):
        """
        Tests OrderNotificationRecipients model repr
        """
        user = UserF.create(**{
            'username': 'Samsung'
        })
        model = OrderNotificationRecipientsF.create(**{
            'user': user
        })

        self.assertEqual(str(model), 'Samsung')

    def test_order_notification_recipients_get_users_for_product(self):
        """
        Tests OrderNotificationRecipients model getUsersForProduct method
        """
        user = UserF.create(**{
            'username': 'Samsung'
        })

        other_user = UserF.create(**{
            'username': 'Sony'
        })

        inst_type = InstrumentTypeF.create(**{
            'operator_abbreviation': 'ITOP 1'
        })
        satellite = SatelliteF.create(**{
            'operator_abbreviation': 'ST 1'
        })

        sat_inst_group = SatelliteInstrumentGroupF.create(**{
            'instrument_type': inst_type,
            'satellite': satellite
        })

        sat_inst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': sat_inst_group
        })

        opp = OpticalProductProfileF.create(**{
            'satellite_instrument': sat_inst
        })

        # first user is registered to a product
        product = OpticalProductF.create(**{
            'product_profile': opp
        })

        content_type = ContentType.objects.get_for_model(product.__class__)

        OrderNotificationRecipientsF.create(**{
            'user': user,
            'add_classes': [content_type]
        })

        # second user is registered to a sat_inst_group

        OrderNotificationRecipientsF.create(**{
            'user': other_user,
            'add_satellite_instrument_groups': [sat_inst_group]
        })

        self.assertEqual(
            len(OrderNotificationRecipients.getUsersForProduct(product)),
            2
        )
