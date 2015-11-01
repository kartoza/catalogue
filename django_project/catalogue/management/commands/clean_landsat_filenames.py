"""Update The existing thumbnail and world file name to our new format"""

__author__ = 'Christian Christelis christian@linfiniti.com'

from django.core.management.base import BaseCommand
from catalogue.models import OpticalProduct


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ command execution """
        """
        LT5PPPRRRYYYYDDDJSA00
        T = Thematic mapper
        5 = Landsat 5
        PPP = path
        RRR = row
        YYYY = year
        DDD = day of year e.g. 365
        JSA = Ground station (Hartebeeshoek's code)
        """

        for (landsat_mission, sac_mission_id) in [
                ('LE7', 'L7'),
                ('LT5', 'L5'),
                ('LM4', 'L4'),
                ('LM3', 'L3'),
                ('LM2', 'L2')]:

            for product in OpticalProduct.objects.filter(
                    unique_product_id__startswith=sac_mission_id):

                    original_product_id = "%s%03d%03d%4d%03dJSA" % (
                        landsat_mission,
                        product.path,
                        product.row,
                        product.product_date.year,
                        product.product_date.timetuple().tm_yday)
                    product.original_product_id = original_product_id
                    product.save()
                    product.refileProductAssets(
                        product.unique_product_id,
                        product.original_product_id,
                        product.productDirectory())
