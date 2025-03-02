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
from exchange.models import Currency, ExchangeRate

from orders.models import (
    Order,
    OrderStatus,
    DeliveryMethod,
    Datum,
    ResamplingMethod,
    FileFormat,
    MarketSector,
    OrderStatusHistory,
    OrderNotificationRecipients,
    NonSearchRecord
)


class CurrencyF(factory.django.DjangoModelFactory):
    """
    Factory for exchange.Currency
    """
    class Meta:
        model = Currency

    code = factory.Sequence(lambda n: "%s" % n)
    name = factory.Sequence(lambda n: "Currency %s" % n)


class ExchangeRateF(factory.django.DjangoModelFactory):
    """
    Factory for exchange.ExchangeRate
    """
    class Meta:
        model = ExchangeRate

    source = factory.SubFactory(CurrencyF)
    target = factory.SubFactory(CurrencyF)
    rate = 0.0


class OrderStatusF(factory.django.DjangoModelFactory):
    """
    OrderStatus model factory
    """
    class Meta:
        model = OrderStatus

    name = factory.Sequence(lambda n: "Status {}".format(n))


class DeliveryMethodF(factory.django.DjangoModelFactory):
    """
    DeliveryMethod model factory
    """
    class Meta:
        model = DeliveryMethod

    name = factory.Sequence(lambda n: "Delivery method {}".format(n))


class DatumF(factory.django.DjangoModelFactory):
    """
    Datum model factory
    """
    class Meta:
        model = Datum

    name = factory.Sequence(lambda n: "Datum {}".format(n))


class ResamplingMethodF(factory.django.DjangoModelFactory):
    """
    ResamplingMethod model factory
    """
    class Meta:
        model = ResamplingMethod

    name = factory.Sequence(lambda n: "Resampling method {}".format(n))


class FileFormatF(factory.django.DjangoModelFactory):
    """
    FileFormat model factory
    """
    class Meta:
        model = FileFormat

    name = factory.Sequence(lambda n: "File format {}".format(n))


class MarketSectorF(factory.django.DjangoModelFactory):
    """
    MarketSector model factory
    """
    class Meta:
        model = MarketSector

    name = factory.Sequence(lambda n: "Market sector {}".format(n))


class OrderF(factory.django.DjangoModelFactory):
    """
    Order model factory
    """
    class Meta:
        model = Order

    user = factory.SubFactory(UserF)
    notes = ''
    order_status = factory.SubFactory(OrderStatusF)
    delivery_method = factory.SubFactory(DeliveryMethodF)
    market_sector = factory.SubFactory(MarketSectorF)
    order_date = None
    datum = factory.SubFactory(DatumF)
    resampling_method = factory.SubFactory(ResamplingMethodF)
    file_format = factory.SubFactory(FileFormatF)
    subsidy_type_requested = factory.SubFactory(
        'dictionaries.tests.model_factories.SubsidyTypeF')
    subsidy_type_assigned = factory.SubFactory(
        'dictionaries.tests.model_factories.SubsidyTypeF')


class OrderStatusHistoryF(factory.django.DjangoModelFactory):
    """
    OrderStatusHistory model factory
    """
    class Meta:
        model = OrderStatusHistory

    user = factory.SubFactory('core.model_factories.UserF')
    order = factory.SubFactory(OrderF)
    notes = ''
    old_order_status = factory.SubFactory(OrderStatusF)
    new_order_status = factory.SubFactory(OrderStatusF)


class OrderNotificationRecipientsF(factory.django.DjangoModelFactory):
    """
    OrderNotificationRecipients model factory
    """
    class Meta:
        model = OrderNotificationRecipients

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


class NonSearchRecordF(factory.django.DjangoModelFactory):
    """
    NonSearchRecord model factory
    """
    class Meta:
        model = NonSearchRecord

    user = factory.SubFactory('core.model_factories.UserF')
    order = factory.SubFactory(OrderF)
    product_description = factory.Sequence(
        lambda n: 'Product description {}'.format(n))
    download_path = factory.Sequence(lambda n: 'Download path // {}'.format(n))
    cost_per_scene = 0.0
    currency = factory.SubFactory(
        CurrencyF
    )
    rand_cost_per_scene = 0.0
