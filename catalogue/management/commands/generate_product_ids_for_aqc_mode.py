"""
SANSA-EO Catalogue - generate_product_ids_for_aqc_mode - generate product ids
    for specific sensor acquisition mode

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
__date__ = '30/07/2012'
__copyright__ = 'South African National Space Agency'

from django.core.management.base import BaseCommand

from catalogue.models import (GenericSensorProduct, AcquisitionMode,
    SensorType, MissionSensor, Mission)


class Command(BaseCommand):

    def init():
        pass

    def handle(self, *args, **options):
        """ command execution """
        if len(args) == 4:
            self.process_products(args)
        else:
            print '''You need to specify four (4) parameters:
  * sensor acquisition mode abbreviation
  * sensor type abbreviation
  * mission sensor abbreviation
  * mission abbreviation

i.e. manage.py generate_product_ids_for_aqc_mode S4C2 M HIR S4'''

    def process_products(self, theParams):
        """ For each product with specific acquisition mode abbreviation
        generate new product_id by calling setSacProductId() """

        # check if acquisition mode abbreviation exists
        myAckMode = AcquisitionMode.objects.filter(abbreviation=theParams[0]).filter(
            sensor_type__abbreviation=theParams[1]).filter(
            sensor_type__mission_sensor__abbreviation=theParams[2]).filter(
            sensor_type__mission_sensor__mission__abbreviation=theParams[3])

        if myAckMode.count() == 1:
            print 'Selected acquisition mode: %s' % myAckMode[0]
            myProducts = GenericSensorProduct.objects.filter(
                acquisition_mode__abbreviation=theParams[0]).filter(
                acquisition_mode__sensor_type__abbreviation=theParams[1]).filter(
                acquisition_mode__sensor_type__mission_sensor__abbreviation=theParams[2]).filter(
                acquisition_mode__sensor_type__mission_sensor__mission__abbreviation=theParams[3])
            myProductsCount = myProducts.count()

            for idx, myProduct in enumerate(myProducts):
                tmpIdx = idx + 1
                myProcessingPercentage = int((tmpIdx/float(myProductsCount))*100)
                print '%s of %s (%s%%) - Current product: %s' % (tmpIdx,
                    myProductsCount, myProcessingPercentage, myProduct)

                myProduct.setSacProductId()
                #print 'New product ID: %s' % (myProduct,)
                myProduct.save()
        else:
            print 'Nothing found using: %s %s %s %s' % theParams
