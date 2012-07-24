"""
SPOT harvesting

Tool for harvesting catalogue records from SPOT coverage maps

http://catalog.spotimage.com

From the menu of above site, go:

My Searches - Download of Coverages

This script is written based on the Africa* shp coverages,
though it should work on others too.

Tim Sutton May 2011

Sample data from one record:
  wkt_geom   POLYGON((5.381600 15.316700,5.507500 15.847000,6.055500 15.725200,5.928300 15.195200,5.381600 15.316700))
  A21        50673191101191017402J
  SC_NUM     17670901
  SEG_NUM    6729479
  SATEL      5
  ANG_INC    5.884188
  ANG_ACQ    5.2
  DATE_ACQ   19/01/2011
  MONTH_ACQ  01
  TIME_ACQ   10:17:40
  CLOUD_QUOT AAAAAAAA
  CLOUD_PER  0
  SNOW_QUOT  00000000
  LAT_CEN    15.521
  LON_CEN    5.7172
  LAT_UP_L   15.847
  LON_UP_L   5.5075
  LAT_UP_R   15.725
  LON_UP_R   6.0555
  LAT_LO_L   15.316
  LON_LO_L   5.3816
  LAT_LO_R   15.195
  LON_LO_R   5.9283
  RESOL      2.5
  MODE       COLOR
  TYPE       T
  URL_QL     http://sirius.spotimage.fr/url/catalogue.aspx?ID=-1&ACTION=Scenes%3AgetQuicklook&CODEA21=50673191101191017402J&SEGMENT=6524011&SAT=0



"""

import os
from optparse import make_option
import tempfile
import subprocess
from mercurial import lock, error

from django.core.management.base import BaseCommand
from django.db import transaction
from catalogue.ingestors import spot


def get_row_path_from_polygon(poly, as_int=False, no_compass=False):
    """
    Given a polygon, returns row, row_shift, path, path_shift
    informations of the centroid as a string
    As indicated in the docs (8.1.3)
    """
    path, path_shift = ("%.2f" % poly.centroid.x).split('.')
    row, row_shift = ("%.2f" % poly.centroid.y).split('.')
    if as_int:
        return int(path), int(path_shift), int(row), int(row_shift)
    if no_compass:
        return path, path_shift, row, row_shift
    if poly.centroid.x < 0:
        path = "%sW" % path
    else:
        path = "%sE" % path
    if poly.centroid.y < 0:
        row = "%sS" % row
    else:
        row = "%sN" % row
    return path, path_shift, row, row_shift

class Command(BaseCommand):
    help = "Imports RapidEye packages into the SAC catalogue"
    option_list = BaseCommand.option_list + (
        make_option('--file', '-f', dest='shapefile', action='store',
                    help='Shapefile containing spot coverage data.',
                    default=False),
        make_option('--download-thumbs', '-d', dest='download_thumbs',
                    action='store',
                    help='Whether thumbnails should be fetched to. If not '
                         'fetched now they will be fetched on demand as needed.'
                    , default=False),
        make_option('--test_only', '-t', dest='test_only', action='store_true',
                    help='Just test, nothing will be written into the DB.',
                    default=False),
        make_option('--owner', '-o', dest='owner', action='store',
                    help=('Name of the Institution package owner. '
                          'Defaults to: Astrium.'), default='Astrium'),
        make_option('--creating_software', '-s',
                    dest='creating_software', action='store',
                    help='Name of the creating software. Defaults to: TS5.',
                    default='TS5'),
        make_option('--license', '-l', dest='license', action='store',
                    default='SANSA Commercial License',
                    help=('Name of the license. Defaults to: SAC Commercial '
                         'License'))
        ,
        make_option('--area', '-a', dest='area', action='store',
                    help='Area of interest, images which are external to this' \
                         ' area will not be imported (WKT Polygon, SRID=4326)')
        ,
        make_option('--quality', '-q', dest='quality', action='store',
                    help='Quality code (will be created if does not exists). ' \
                         'Defaults to: Unknown'
                    , default='Unknown'),
        # We should use 1A here but we need to write migration
        # logic for all existing records and rename all existing thumnbs
        make_option('--processing_level', '-r', dest='processing_level',
                    action='store',
                    help=(
                    'Processing level code (will be created if does not exists).'
                    'Defaults to: 1B'), default='1B'),
        )


    @transaction.commit_manually
    def handle(self, *args, **options):
        """ command execution """
        def verblog(msg, level=1):
            if verbose >= level:
                print msg

        shapefile             = options.get('shapefile')
        download_thumbs       = options.get('download_thumbs')
        test_only             = options.get('test_only')
        verbose               = int(options.get('verbosity'))
        license               = options.get('license')
        owner                 = options.get('owner')
        software              = options.get('creating_software')
        area                  = options.get('area')
        quality               = options.get('quality')
        processing_level      = options.get('processing_level')

        spot.ingest(theShapeFile=shapefile,
                    myDownloadThumbsFlag=download_thumbs,
                    theTestOnlyFlag=test_only,
                    theVerbosityLevel=verbose,
                    theLicense=license,
                    theOwner=owner,
                    theSoftware=software,
                    theArea=area,
                    theQuality=quality,
                    theProcessingLevel=processing_level
        )
