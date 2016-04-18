# coding=utf-8
"""
SPOT harvesting command.

Tool for harvesting catalogue records from SPOT coverage maps

http://catalog.spotimage.com

From the menu of above site, go:

My Searches - Download of Coverages

This script is written based on the Africa* shp coverages,
though it should work on others too.

Tim Sutton May 2011
"""

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import transaction
from catalogue.ingestors import spot


class Command(BaseCommand):
    """Management command to import SPOT data from a SPOT catalogue shpfile.
    """
    help = "Imports SPOT packages into the SANSA catalogue"
    option_list = BaseCommand.option_list + (
        make_option(
            '--file',
            '-f',
            dest='shapefile',
            action='store',
            help='Shapefile containing spot coverage data.',
            default=False),
        make_option(
            '--download-thumbs',
            '-d',
            dest='download_thumbs_flag',
            action='store',
            help='Whether thumbnails should be fetched to. If not '
                 'fetched now they will be fetched on demand as needed.',
            default=False),
        make_option(
            '--test_only',
            '-t',
            dest='test_only_flag',
            action='store_true',
            help='Just test, nothing will be written into the DB.',
            default=False),
        make_option(
            '--area',
            '-a',
            dest='area',
            action='store',
            help=(
                'Area of interest, images which are external to this'
                ' area will not be imported (WKT Polygon, SRID=4326)')),
        make_option(
            '--halt_on_error',
            '-e',
            dest='halt_on_error_flag',
            action='store',
            help=(
                'Halt on first error that occurs and print a stacktrace'),
            default=False),
        make_option(
            '--start-from',
            '-s',
            dest='start_from',
            action='store',
            help='Start from a specific original ID')
    )

    # noinspection PyDeprecation
    @staticmethod
    def _parameter_to_bool(parameter):
        if parameter == 'True':
            parameter = True
        else:
            parameter = False
        return parameter

    @transaction.atomic
    def handle(self, *args, **options):
        """ command execution
        :param args:
        :param options:
        """
        shapefile = options.get('shapefile')
        download_thumbs_flag = self._parameter_to_bool(
            options.get('download_thumbs_flag'))
        test_only_flag = self._parameter_to_bool(
            options.get('test_only_flag'))
        verbose = int(options.get('verbosity'))
        area = options.get('area')
        halt_on_error = self._parameter_to_bool(
            options.get('halt_on_error_flag'))
        start_from = options.get('start_from')

        spot.ingest(
            shapefile=shapefile,
            download_thumbs_flag=download_thumbs_flag,
            area_of_interest=area,
            test_only_flag=test_only_flag,
            verbosity_level=verbose,
            halt_on_error_flag=halt_on_error,
            start_from=start_from)
