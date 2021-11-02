__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '3/4/16'

from django.core.management.base import BaseCommand
from catalogue.ingestors import cbers


class Command(BaseCommand):
    """
    Tool for harvesting CBERS-4 xml file for CBERS data.
    """

    # noinspection PyShadowingBuiltins
    help = 'Imports CBERS-4 records into the SANSA catalogue'

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
                '/data/CBERS/'))
        parser.add_argument(
            '--halt_on_error', '-e', dest='halt_on_error_flag',
            action='store',
            help=(
                'Halt on first error that occurs and print a '
                'stacktrace'),
            default=False),
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
        test_only = self._parameter_to_bool(options['test_only_flag'])
        source_dir = options['source_dir']
        verbose = int(options['verbosity'])
        halt_on_error = self._parameter_to_bool(
            options['halt_on_error_flag'])
        ignore_missing_thumbs = self._parameter_to_bool(
            options['ignore_missing_thumbs_flag'])

        cbers.ingest(
            source_path=source_dir,
            test_only_flag=test_only,
            verbosity_level=verbose,
            halt_on_error_flag=halt_on_error,
            ignore_missing_thumbs=ignore_missing_thumbs
        )
