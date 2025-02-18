import os
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Creates or replaces the pycsw_catalogue_view using an external SQL file."

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sql_file = os.path.join(base_dir, 'pycsw_catalogue_view.sql')
        
        if not os.path.exists(sql_file):
            self.stderr.write(self.style.ERROR(
                f"SQL file not found: {sql_file}"))
            return

        with open(sql_file, 'r') as f:
            sql = f.read()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write(
            self.style.SUCCESS(
                "pycsw_catalogue_view has been created or replaced successfully."
                )
          )
import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Creates or replaces the pycsw_catalogue_view. By default, it creates a regular view. " \
           "Use --materialized to create a materialized view, and optionally specify a --limit (default 100)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--materialized',
            action='store_true',
            dest='materialized',
            default=False,
            help='If set, create a materialized view instead of a regular view.'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='When creating a materialized view, specify a limit for the number of rows (default is 100 if not provided).'
        )

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute("DROP MATERIALIZED VIEW IF EXISTS pycsw_catalogue_view;")
        except Exception as e:
            if 'not a materialized view' in str(e):
                with connection.cursor() as cursor:
                    cursor.execute("DROP VIEW IF EXISTS pycsw_catalogue_view;")
            else:
                raise e
        self.stdout.write(self.style.WARNING("Existing view/materialized view dropped (if existed)."))

        base_dir = os.path.dirname(os.path.abspath(__file__))
        if options['materialized']:
            sql_file = os.path.join(base_dir, 'pycsw_catalogue_view_mat.sql')
            limit = options['limit'] if options['limit'] is not None else 100
        else:
            sql_file = os.path.join(base_dir, 'pycsw_catalogue_view.sql')
            limit = None

        if not os.path.exists(sql_file):
            self.stderr.write(self.style.ERROR(f"SQL file not found: {sql_file}"))
            return

        with open(sql_file, 'r') as f:
            sql = f.read()

        if options['materialized']:
            sql = sql.format(limit=limit)

        with connection.cursor() as cursor:
            cursor.execute(sql)

        if options['materialized']:
            self.stdout.write(self.style.SUCCESS(
                f"Materialized view 'pycsw_catalogue_view' has been created with limit {limit}."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                "View 'pycsw_catalogue_view' has been created or replaced successfully."
            ))
