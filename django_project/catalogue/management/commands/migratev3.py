"""
SANSA-EO Catalogue - migrate catalogue to version 3.0

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
__date__ = '11/02/2013'
__copyright__ = 'South African National Space Agency'

import os
from optparse import make_option
import subprocess

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate catalogue db from v2.x to v3.0, uses default database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--migrations', metavar="MIGRATION_TYPE", default='all',
            help=(
                'Selectively migrate parts of the database, comma "," '
                'delimited list of migrations (backup_tasks, new_dicts, '
                'userprofiles, search, remove_spot, processing_levels, '
                'unique_product_id, product_schema_changes, pycsw, orders, '
                'exchange, cleanup defaults to "all"'
            )
        )

    def handle(self, *args, **options):
        self.db = settings.DATABASES['default']['NAME']
        myMigrations = options.get('migrations').split(',')

        if 'all' in myMigrations:
            self.migrate_backup_tasks()
            self.migrate_new_dicts()
            self.migrate_userprofiles()
            self.migrate_search()
            self.migrate_remove_spot()
            self.migrate_proc_levels()
            self.migrate_unique_product_ids()
            self.migrate_product_models()
            self.migrate_pycsw()
            self.migrate_orders()
            self.migrate_exchange()
            self.migrate_cleanup()

        if 'backup_tasks' in myMigrations:
            self.migrate_backup_tasks()

        if 'new_dicts' in myMigrations:
            self.migrate_new_dicts()

        if 'userprofiles' in myMigrations:
            self.migrate_userprofiles()

        if 'search' in myMigrations:
            self.migrate_search()

        if 'remove_spot' in myMigrations:
            self.migrate_remove_spot()

        if 'processing_levels' in myMigrations:
            self.migrate_proc_levels()

        if 'unique_product_id' in myMigrations:
            self.migrate_unique_product_ids()

        if 'product_schema_changes' in myMigrations:
            self.migrate_product_models()

        if 'pycsw' in myMigrations:
            self.migrate_pycsw()

        if 'orders' in myMigrations:
            self.migrate_orders()

        if 'exchange' in myMigrations:
            self.migrate_exchange()

        if 'cleanup' in myMigrations:
            self.migrate_cleanup()

    def migrate_backup_tasks(self):
        print('* Starting backup tasks migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing backup tasks scripts...')
        subprocess.call(['sh', '000_backup_tasks.sh', self.db])
        os.chdir(origWD)

    def migrate_product_models(self):
        print('* Starting product models migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing product schema change scripts...')
        subprocess.call(['sh', '020_product_schema_changes.sh', self.db])
        os.chdir(origWD)

    def migrate_new_dicts(self):
        print('* Starting new_dicts migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '001_new_dicts.sh', self.db])
        os.chdir(origWD)

    def migrate_userprofiles(self):
        print('* Starting profile migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '002_profile_migration.sh', self.db])
        os.chdir(origWD)
        print('* Checking user permission (might take awhile)...')
        call_command('check_permissions')

    def migrate_search(self):
        print('* Starting search app migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '003_search_migration.sh', self.db])
        os.chdir(origWD)

    def migrate_remove_spot(self):
        print('* Starting remove_spot migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '008_remove_spot_migration.sh', self.db])
        os.chdir(origWD)

    def migrate_pycsw(self):
        print('* Starting pycsw app migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '100_pycsw_integration.sh', self.db])
        os.chdir(origWD)

    def migrate_proc_levels(self):
        print('* Starting processing_levels migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '010_processing_level.sh', self.db])
        os.chdir(origWD)

    def migrate_unique_product_ids(self):
        print('* Starting unique_product_id migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '015_unique_product_id.sh', self.db])
        os.chdir(origWD)

    def migrate_cleanup(self):
        print('* Starting general cleanup migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '999_cleanup.sh', self.db])
        os.chdir(origWD)

    def migrate_orders(self):
        print('* Starting orders app migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '200_orders.sh', self.db])
        os.chdir(origWD)

    def migrate_exchange(self):
        print('* Starting exchange app migration...')
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'resources', 'sql', 'new_master'))
        print('* Executing database migration scripts...')
        subprocess.call(['sh', '250_exchange.sh', self.db])
        os.chdir(origWD)
