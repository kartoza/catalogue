__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '3/3/16'

from optparse import make_option
from django.core.management.base import BaseCommand
from catalogue.ingestors import landsat


class Command(BaseCommand):
    """
    Tool for harvesting Landsat 7/8 xml file for Landsat data.
    """

    # noinspection PyShadowingBuiltins
    help = 'Imports Landsat 7/8 records into the SANSA catalogue'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test_only',
            '-t',
            dest='test_only_flag',
            action='store_true',
            help='Just test, nothing will be written into the DB.',
            default=False)
        parser.add_argument(
            '--source_dir',
            '-d',
            dest='source_dir',
            action='store',
            help=(
                'Source directory containing DIMS IIF xml file and '
                'thumbnail to import.'),
            default=(
                '/home/web/django_project'
                '/data/landsat/'))
        parser.add_argument(
            '--halt_on_error', '-e', dest='halt_on_error_flag',
            action='store',
            help=(
                'Halt on first error that occurs and print a '
                'stacktrace'),
            default=False)
        parser.add_argument(
            '--ignore-missing-thumbs',
            '-i',
            dest='ignore_missing_thumbs_flag',
            action='store',
            help=(
                'Continue with importing records even if they miss their'
                'thumbnails.'),
            default=False)

    # noinspection PyDeprecation
    @staticmethod
    def _parameter_to_bool(parameter):
        if parameter == 'True':
            parameter = True
        else:
            parameter = False
        return parameter

    def handle(self, *args, **options):
        """ command execution """
        test_only = self._parameter_to_bool(options.get('test_only_flag'))
        source_dir = options.get('source_dir')
        verbose = int(options.get('verbosity'))
        halt_on_error = self._parameter_to_bool(
            options.get('halt_on_error_flag'))
        ignore_missing_thumbs = self._parameter_to_bool(
            options.get('ignore_missing_thumbs_flag'))

        landsat.ingest(
            source_path=source_dir,
            test_only_flag=test_only,
            verbosity_level=verbose,
            halt_on_error_flag=halt_on_error,
            ignore_missing_thumbs=ignore_missing_thumbs
        )
