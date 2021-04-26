"""
OS4EO ordering

http://196.35.94.243/os4eo

"""

from optparse import make_option

from mercurial import lock, error
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.db import transaction

from catalogue.models import *
from catalogue.os4eo_client import OS4EOClient
from elementsoap.ElementSOAP import SoapFault


class Command(BaseCommand):
    help = "Place orders"
    option_list = BaseCommand.option_list + (
        make_option('--test_only', '-t', dest='test_only', action='store_true',
            help='Just test, nothing will be written into the DB.', default=False),
    )

    @transaction.commit_manually
    def handle(self, *args, **options):
        """ command execution """

        try:
            lockfile = lock.lock("/tmp/os4eo_order.lock", timeout=60)
        except error.LockHeld:
            # couldn't take the lock
            raise CommandError('Could not acquire lock.')

        test_only             = options.get('test_only')
        verbose               = int(options.get('verbosity'))

        def verblog(msg, level=1):
            if verbose >= level:
                print(msg)

        verblog('Getting verbose (level=%s)... ' % verbose, 2)
        if test_only:
            verblog('Testing mode activated.', 2)

        try:
            # Creates the client
            os4eo = OS4EOClient()
            # Scan DB for pending orders
            # We must be sure they are GenericSensorProduct...
            pending_records = []
            for sr in SearchRecord.objects.exclude(order__order_status__name__in=['Cancelled', 'Awaiting info from client', 'Completed']).filter(product_ready=False):
                verblog('Processing SearchRecord %s ...' % sr, 2)
                try:
                    if sr.product.getConcreteInstance().online_storage_medium_id:
                        pending_records.append(sr)
                    else:
                        verblog('Product %s has no online_storage_medium_id value (it is not a DIMS product).' % sr.product, 2)
                except:
                    verblog('Product %s is not a GenericSensorProduct,' % sr.product, 2)

            # for each order
            for sr in pending_records:
                try:
                    # Place OS4EO order
                    # Case 1: order not placed
                    if not sr.internal_order_id:
                        try:
                            os4eo_id, os4eo_submit_status = os4eo.Submit(sr.product.getConcreteInstance().online_storage_medium_id, sr.pk)
                            sr.internal_order_id = os4eo_id
                            sr.save()
                        except SoapFault as e:
                            verblog('SoapFault error placing OS4EO order for %s' % sr)
                        finally:
                            if os4eo_submit_status != 'success':
                                verblog('Cannot place OS4EO order for %s: %s' % (sr, e))
                    # Case 2: order placed but not ready, check order status, check also if available
                    elif sr.internal_order_id and not sr.product_ready:
                        try:
                            if os4eo.GetStatus(order_record.internal_order_id) == 'Completed':
                                verblog('OS4EO order %s is completed' % sr)
                                try:
                                    result_access_status, dowload_path = os4eo.DescribeResultAccess(order_record.internal_order_id)
                                    # Store dowload_path SearchRecord
                                    sr.dowload_path = dowload_path
                                    sr.save()
                                    # Check that the order is complete
                                    if sr.order.searchrecord_set.filter(Q(internal_order_id__isnull=True) | Q(product_ready=False)).count():
                                        verblog('Order %s has pending SearchRecords: cannot set completed', 2)
                                    else:
                                        sr.order.order_status = OrderStatus.objects.get(name='Completed')
                                        sr.order.save()
                                        verblog('Marking order %s as completed.' % sr.order)
                                except SoapFault as e:
                                    verblog('OS4EO order %s is not completed (DescribeResultAccess)' % (sr, e))
                            else:
                                verblog('OS4EO order %s is not completed (GetStatus)' % sr)
                        except SoapFault as e:
                            verblog('Cannot check OS4EO order for %s: %s' % (sr, e))
                    if test_only:
                        transaction.rollback()
                        verblog("Testing only: transaction rollback.")
                    else:
                        transaction.commit()
                        verblog("Committing transaction.", 2)
                except Exception as e:
                    raise CommandError('Uncaught exception: %s' % e)
        except Exception as e:
            verblog('Rolling back transaction due to exception.')
            if test_only:
                from django.db import connection
                verblog(connection.queries)
            transaction.rollback()
            raise CommandError("%s" % e)
        finally:
            lockfile.release()
