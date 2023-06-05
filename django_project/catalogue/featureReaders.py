"""
SANSA-EO Catalogue - Read geometry from features in spatial files

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import os
from zipfile import ZipFile
import traceback
import logging
from django.contrib.gis.gdal import DataSource
from django.conf import settings
# python logging support to django logging middleware

from django.contrib.gis.geos import GEOSGeometry

logger = logging.getLogger(__name__)


###########################################################
#
# Try to extract a geometry if a shp or kml was uploaded
#
###########################################################


def get_geometry_from_uploaded_file(request, form, file_field):
    """
    Retrieve an uploaded geometry from a file. Note in order for this to work,
    you must have set your form to use multipart encoding type e.g.
    <form enctype="multipart/form-data" action="/search/" method="post"
        id="search_form">
    """
    logger.debug('Form cleaned data: ' + str(form.cleaned_data))
    if request.FILES.get(file_field):
        logger.debug('Using geometry from file.')

        # use last part of filename as extension
        extension = (
            form.cleaned_data[file_field].name.split('.')[-1].lower())
        if not (extension == 'zip' or extension == 'kml' or
                extension == 'kmz'):
            logger.info(
                'Wrong format for uploaded geometry. Please select a valid '
                'file (ZIP, KML, KMZ.')
            # render_to_response is done by the renderWithContext decorator
            # @TODO return a clearer error spotmap just like Alert for the
            # missing dates
            return False

        # read geometry
        file = form.cleaned_data[file_field]
        out_file = '/tmp/%s' % file.name
        destination = open(out_file, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        if extension == 'zip':
            extracted_geometries = get_features_from_zip_file(
                out_file, 'Polygon', 1)
        else:
            extracted_geometries = get_features_from_kml_file(
                out_file, 'Polygon', 1)

        if len(extracted_geometries) == 0:
            logger.info('No geometries found...')
            return None
        else:
            return process_geometries_type(extracted_geometries).wkt


def process_geometries_type(geometries):
    # get first geometry from setof geometries (they are in wkt)
    geometry = GEOSGeometry(geometries[0])
    # check it is a single part polygon. If it isn't we use its envelope...
    if geometry.geom_type != 'Polygon':
        logger.info(
            'Uploaded geometry is not a polygon (its a %s) - using its '
            'evenlope instead: ' % str(geometry.geom_type))
        geometry = geometry.envelope
    return geometry


def get_features_from_zip_file(zip_file, geometry, features="all"):
    """
    Takes a zip archive and extracts N features of the specified geometry type.
    """
    # inspect the zip file
    zipped_shape = None
    try:
        logger.debug('Extracting...%s' % zip_file)
        zipped_shape = ZipFile(zip_file)
        logger.debug('extract done...')
    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.debug("ZipFile Failed: %s" % e)
    # check if the contents of the archive are the usual 3 files with no
    # subdirectories.
    logger.debug('checking zip contents are a shp, shx, dbf...')
    if any([f.endswith('/') for f in zipped_shape.namelist()]):
        logger.debug('Extract failed due to subdirs present')
        raise RuntimeError(
            'The archive contains subdirectories. Please zip only the shp, '
            '.shx, .dbf[, .prj] files.')
    extensions_list = [
        fullname.split('.')[-1] for fullname in zipped_shape.namelist()]
    present_extensions = set(extensions_list).intersection(
        set(['shp', 'shx', 'dbf']))
    logger.debug('contents ok...')
    if len(present_extensions) < 3:
        logger.debug('Extract failed due to less than 3 files present in zip')
        raise RuntimeError('At least one of .shp, .shx, .dbf is missing.')
    # extract - for Python 2.5. Python 2.6 has a nice ZipFile.extract()
    for each in zipped_shape.namelist():
        destination_file = os.path.join(settings.SHP_UPLOAD_DIR, each)
        data = zipped_shape.read(each)
        f = open(destination_file, 'w')
        f.write(data)
        f.close()
    zipped_shape.close()
    logger.debug('Shapefiles written to  %s ' % settings.SHP_UPLOAD_DIR)
    shp_name = [
        elem for elem in zipped_shape.namelist() if elem[-3:] == 'shp'].pop()
    shp_file_on_disk_path = os.path.join(settings.SHP_UPLOAD_DIR, shp_name)
    logger.debug('Uploaded shp is %s' % shp_file_on_disk_path)
    # load the shapefile in GeoDjango
    data_source = None
    try:
        logger.debug('loading shapes as a datasource...')
        data_source = DataSource(shp_file_on_disk_path)
    except Exception as e:
        logger.debug(str(traceback.format_exc()))
        logger.debug('datasource loading failed :-(')
        logger.debug('Failed: %s' % e)
        raise RuntimeError('Loading shp failed')
    logger.debug('Datasource loaded ok')

    # extract the first polygon if any
    first_layer = None
    if data_source[0].geom_type == geometry:
        logger.debug('Extracting poly')
        try:
            first_layer = data_source[0]
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.debug('')
            logger.debug('Crashed: %s' % e)
        logger.debug('Extracting poly done')
    else:
        logger.debug('Failed - no polygon data')
        # cleanup before exiting
        for each in zipped_shape.namelist():
            logger.debug('Failed - removing shps')
            os.remove(os.path.join(settings.SHP_UPLOAD_DIR, each))
        raise RuntimeError(
            'The geometry %s is not available in this shapefile.' % geometry)

    # some info.
    logger.debug('Zip archive name: %s' % zipped_shape.filename)
    logger.debug('Shapefile name: %s ' % shp_name)
    logger.debug('Full datasource name: %s' % data_source.name)
    logger.debug('Number of available features: %s' % str(
        data_source[0].num_feat))
    logger.debug('Geometry type: %s' % first_layer.geom_type.name)
    logger.debug('Number of extracted features: %s' % str(features))

    # extract the N geometries, otherwise all of them
    if features != 'all':
        geometries_list = [
                              pt.wkt for pt in first_layer.get_geoms()][0:features]
    else:
        geometries_list = [pt.wkt for pt in first_layer.get_geoms()]

    # cleanup of dezipped files
    for each in zipped_shape.namelist():
        logger.debug('Removing shps')
        os.remove(os.path.join(settings.SHP_UPLOAD_DIR, each))

    # return the data
    return geometries_list


def get_features_from_kml_file(zip_file, geometry, features='all'):
    """
    Takes a KML or KMZ file and extracts N features of the specified geometry
    type.
    """
    # inspect the KML file
    geom_file = None
    if zip_file.split('.')[1] == 'kmz':
        try:
            logger.debug('Extracting...%s' % zip_file)
            tmp_zip = ZipFile(zip_file)
            # read first file in unzipped kmz, which is kml
            geom_file = tmp_zip.read(tmp_zip.namelist()[0])
            logger.debug('extract done...')
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.debug('ZipFile Failed: %s' % e)
    else:
        # if plain KML file, read data
        tmp_data = open(zip_file, 'r')
        geom_file = tmp_data.read()
        tmp_data.close()

    # temporary store unpacked files
    destination = os.path.join(settings.SHP_UPLOAD_DIR, zip_file)
    f = open(destination, 'w')
    f.write(geom_file)
    f.close()

    try:
        logger.debug('loading KML as a datasource...')
        data_source = DataSource(destination)
    except Exception as e:
        logger.debug(str(traceback.format_exc()))
        logger.debug('datasource loading failed :-(')
        logger.debug('Failed: %s' % e)
        raise RuntimeError('Loading KML failed')

    logger.debug('Datasource loaded ok')

    # find polygon layers (polygon or polygon25d)
    poly_layer = [layer for layer in data_source if (
            layer.geom_type.name == 'Polygon' or
            layer.geom_type.name == 'Polygon25D')]

    first_layer = None
    if poly_layer:
        logger.debug('Extracting poly')
        try:
            first_layer = poly_layer[0]
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.debug('')
            logger.debug('Crashed: %s' % e)
        logger.debug('Extracting poly done')
    else:
        logger.debug('Failed - no polygon data')
        os.remove(os.path.join(settings.SHP_UPLOAD_DIR, zip_file))
        raise RuntimeError(
            'The geometry %s is not available in this KML.' % geometry)

    logger.debug('Full datasource name: %s' % data_source.name)
    logger.debug('Number of available features: %s' % str(
        data_source[0].num_feat))
    logger.debug('Geometry type: %s' % first_layer.geom_type.name)
    logger.debug('Number of extracted features: %s' % str(features))

    # extract the N geometries, otherwise all of them
    if features != 'all':
        # if geos=True, geometry will be read as 2D, which is obligatory
        geometries_list = [
                              pt.wkt for pt in first_layer.get_geoms(geos=True)][0:features]
    else:
        geometries_list = [pt.wkt for pt in first_layer.get_geoms(geos=True)]

    # clean up
    os.remove(os.path.join(settings.SHP_UPLOAD_DIR, zip_file))
    # return the data
    return geometries_list
