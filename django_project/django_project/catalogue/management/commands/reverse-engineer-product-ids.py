from catalogue.models import GenericSensorProduct
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def init():
        pass

    def handle(self, *args, **options):
        """ command execution """
        for p in GenericSensorProduct.objects.filter(product_id__startswith='L'):
            p.productIdReverse(force=True)
            p.save()
