"""
SANSA-EO Catalogue - Catalogue model factories

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
__date__ = '01/02/2014'
__copyright__ = 'South African National Space Agency'

import factory

from ..models import (
    Order, OrderStatus, DeliveryMethod, DeliveryDetail, Datum,
    ResamplingMethod, FileFormat, MarketSector, OrderStatusHistory,
    OrderNotificationRecipients
)


class OrderStatusF(factory.django.DjangoModelFactory):
    """
    OrderStatus model factory
    """
    FACTORY_FOR = OrderStatus

    name = factory.Sequence(lambda n: "Status {}".format(n))


class DeliveryMethodF(factory.django.DjangoModelFactory):
    """
    DeliveryMethod model factory
    """
    FACTORY_FOR = DeliveryMethod

    name = factory.Sequence(lambda n: "Delivery method {}".format(n))


class DatumF(factory.django.DjangoModelFactory):
    """
    Datum model factory
    """
    FACTORY_FOR = Datum

    name = factory.Sequence(lambda n: "Datum {}".format(n))


class ResamplingMethodF(factory.django.DjangoModelFactory):
    """
    ResamplingMethod model factory
    """
    FACTORY_FOR = ResamplingMethod

    name = factory.Sequence(lambda n: "Resampling method {}".format(n))


class FileFormatF(factory.django.DjangoModelFactory):
    """
    FileFormat model factory
    """
    FACTORY_FOR = FileFormat

    name = factory.Sequence(lambda n: "File format {}".format(n))


class MarketSectorF(factory.django.DjangoModelFactory):
    """
    MarketSector model factory
    """
    FACTORY_FOR = MarketSector

    name = factory.Sequence(lambda n: "Market sector {}".format(n))


class DeliveryDetailF(factory.django.DjangoModelFactory):
    """
    DeliveryDetail model factory
    """
    FACTORY_FOR = DeliveryDetail

    user = factory.SubFactory('core.model_factories.UserF')
    processing_level = factory.SubFactory(
        'dictionaries.tests.model_factories.ProcessingLevelF')
    projection = factory.SubFactory(
        'dictionaries.tests.model_factories.ProjectionF')
    datum = factory.SubFactory(DatumF)
    resampling_method = factory.SubFactory(ResamplingMethodF)
    file_format = factory.SubFactory(FileFormatF)
    geometry = None


class OrderF(factory.django.DjangoModelFactory):
    """
    Order model factory
    """
    FACTORY_FOR = Order

    user = factory.SubFactory('core.model_factories.UserF')
    notes = ''
    order_status = factory.SubFactory(OrderStatusF)
    delivery_method = factory.SubFactory(DeliveryMethodF)
    delivery_detail = factory.SubFactory(DeliveryDetailF)
    market_sector = factory.SubFactory(MarketSectorF)
    order_date = None


class OrderStatusHistoryF(factory.django.DjangoModelFactory):
    """
    OrderStatusHistory model factory
    """
    FACTORY_FOR = OrderStatusHistory

    user = factory.SubFactory('core.model_factories.UserF')
    order = factory.SubFactory(OrderF)
    notes = ''
    old_order_status = factory.SubFactory(OrderStatusF)
    new_order_status = factory.SubFactory(OrderStatusF)


class OrderNotificationRecipientsF(factory.django.DjangoModelFactory):
    """
    OrderNotificationRecipients model factory
    """
    FACTORY_FOR = OrderNotificationRecipients

    user = factory.SubFactory('core.model_factories.UserF')

    @factory.post_generation
    def add_satellite_instrument_groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for sat_inst_group in extracted:
                self.satellite_instrument_group.add(sat_inst_group)

    @factory.post_generation
    def add_classes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for klass in extracted:
                self.classes.add(klass)