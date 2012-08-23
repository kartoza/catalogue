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

###########################################################
#
# Try to extract a geometry if a shp or kml was uploaded
#
###########################################################


def getGeometryFromUploadedFile(theRequest, theForm, theFileField):
    """
    Retrieve an uploaded geometry from a file. Note in order for this to work,
    you must have set your form to use multipart encoding type e.g.
    <form enctype="multipart/form-data" action="/search/" method="post"
        id="search_form">
    """
    logging.info('Form cleaned data: ' + str(theForm.cleaned_data))
    if theRequest.FILES[theFileField]:
        logging.debug('Using geometry from file.')

        #use last part of filename as extension
        myExtension = (
            theForm.cleaned_data[theFileField].name.split('.')[-1].lower())
        if not(myExtension == 'zip' or myExtension == 'kml' or
                myExtension == 'kmz'):
            logging.info(
                'Wrong format for uploaded geometry. Please select a valid '
                'file (ZIP, KML, KMZ.')
            #render_to_response is done by the renderWithContext decorator
            #@TODO return a clearer error spotmap just like Alert for the
            #missing dates
            return False

        #read geometry
        myFile = theForm.cleaned_data[theFileField]
        myOutFile = '/tmp/%s' % myFile.name
        destination = open(myOutFile, 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        if myExtension == 'zip':
            extractedGeometries = getFeaturesFromZipFile(
                myOutFile, 'Polygon', 1)
        else:
            extractedGeometries = getFeaturesFromKMLFile(
                myOutFile, 'Polygon', 1)

        if len(extractedGeometries) == 0:
            logging.info('No geometries found...')
            return None
        else:
            return processGeometriesType(extractedGeometries).wkt


def processGeometriesType(theGeometries):
    #get first geometry from setof geometries (they are in wkt)
    myGeometry = GEOSGeometry(theGeometries[0])
    # check it is a single part polygon. If it isnt we use its envelope...
    if myGeometry.geom_type != 'Polygon':
        logging.info(
            'Uploaded geometry is not a polygon (its a %s) - using its '
            'evenlope instead: ' % str(myGeometry.geom_type))
        myGeometry = myGeometry.envelope
    return myGeometry


def getFeaturesFromZipFile(zipfile, geometry, numFeatures="all"):
    """
    Takes a zip archive and extracts N features of the specified geometry type.
    """
    # inspect the zip file
    zippedShape = None
    try:
        logging.debug('Extracting...%s' % zipfile)
        zippedShape = ZipFile(zipfile)
        logging.debug('extract done...')
    except Exception, e:
        logging.debug(traceback.format_exc())
        logging.debug("ZipFile Failed: %s" % e)
    # check if the contents of the archive are the usual 3 files with no
    # subdirectories.
    logging.debug('checking zip contents are a shp, shx, dbf...')
    if any([f.endswith('/') for f in zippedShape.namelist()]):
        logging.debug('Extract failed due to subdirs present')
        raise RuntimeError(
            'The archive contains subdirectories. Please zip only the shp, '
            '.shx, .dbf[, .prj] files.')
    extensionsList = [
        fullname.split('.')[-1] for fullname in zippedShape.namelist()]
    presentExtensions = set(extensionsList).intersection(
        set(['shp', 'shx', 'dbf']))
    logging.debug('contents ok...')
    if len(presentExtensions) < 3:
        logging.debug('Extract failed due to less than 3 files present in zip')
        raise RuntimeError('At least one of .shp, .shx, .dbf is missing.')
    # extract - for Python 2.5. Python 2.6 has a nice ZipFile.extract()
    for each in zippedShape.namelist():
        destinationFile = os.path.join(settings.SHP_UPLOAD_DIR, each)
        data = zippedShape.read(each)
        f = open(destinationFile, 'w')
        f.write(data)
        f.close()
    zippedShape.close()
    logging.debug('Shapefiles written to  %s ' % settings.SHP_UPLOAD_DIR)
    shpName = [
        elem for elem in zippedShape.namelist() if elem[-3:] == 'shp'].pop()
    shpFileOnDiskPath = os.path.join(settings.SHP_UPLOAD_DIR, shpName)
    logging.debug('Uploaded shp is %s' % shpFileOnDiskPath)
    # load the shapefile in GeoDjango
    dataSource = None
    try:
        logging.debug('loading shapes as a datasource...')
        dataSource = DataSource(shpFileOnDiskPath)
    except Exception, e:
        logging.debug(str(traceback.format_exc()))
        logging.debug('datasource loading failed :-(')
        logging.debug('Failed: %s' % e)
        raise RuntimeError('Loading shp failed')
    logging.debug('Datasource loaded ok')

    # extract the first polygon if any
    firstLayer = None
    if dataSource[0].geom_type == geometry:
        logging.debug('Extracting poly')
        try:
            firstLayer = dataSource[0]
        except Exception, e:
            logging.debug(traceback.format_exc())
            logging.debug('')
            logging.debug('Crashed: %s' % e)
        logging.debug('Extracting poly done')
    else:
        logging.debug('Failed - no polygon data')
        # cleanup before exiting
        for each in zippedShape.namelist():
            logging.debug('Failed - removing shps')
            os.remove(os.path.join(settings.SHP_UPLOAD_DIR, each))
        raise RuntimeError(
            'The geometry %s is not available in this shapefile.' % geometry)

    # some info.
    logging.debug('Zip archive name: %s' % zippedShape.filename)
    logging.debug('Shapefile name: %s ' % shpName)
    logging.debug('Full datasource name: %s' % dataSource.name)
    logging.debug('Number of available features: %s' % str(
        dataSource[0].num_feat))
    logging.debug('Geometry type: %s' % firstLayer.geom_type.name)
    logging.debug('Number of extracted features: %s' % str(numFeatures))

    # extract the N geometries, otherwise all of them
    if numFeatures != 'all':
        geometriesList = [
            pt.wkt for pt in firstLayer.get_geoms()][0:numFeatures]
    else:
        geometriesList = [pt.wkt for pt in firstLayer.get_geoms()]

    # cleanup of dezipped files
    for each in zippedShape.namelist():
        logging.debug('Removing shps')
        os.remove(os.path.join(settings.SHP_UPLOAD_DIR, each))

    # return the data
    return geometriesList


def getFeaturesFromKMLFile(zipfile, geometry, numFeatures='all'):
    """
    Takes a KML or KMZ file and extracts N features of the specified geometry
    type.
    """
    # inspect the KML file
    myGeomFile = None
    if zipfile.split('.')[1] == 'kmz':
        try:
            logging.debug('Extracting...%s' % zipfile)
            tmp_zip = ZipFile(zipfile)
            #read first file in unzipped kmz, which is kml
            myGeomFile = tmp_zip.read(tmp_zip.namelist()[0])
            logging.debug('extract done...')
        except Exception, e:
            logging.debug(traceback.format_exc())
            logging.debug('ZipFile Failed: %s' % e)
    else:
        #if plain KML file, read data
        tmp_data = open(zipfile, 'r')
        myGeomFile = tmp_data.read()
        tmp_data.close()

    #temporary store unpacked files
    destinationFile = os.path.join(settings.SHP_UPLOAD_DIR, zipfile)
    f = open(destinationFile, 'w')
    f.write(myGeomFile)
    f.close()

    dataSource = None
    try:
        logging.debug('loading KML as a datasource...')
        dataSource = DataSource(destinationFile)
    except Exception, e:
        logging.debug(str(traceback.format_exc()))
        logging.debug('datasource loading failed :-(')
        logging.debug('Failed: %s' % e)
        raise RuntimeError('Loading KML failed')
    logging.debug('Datasource loaded ok')

    # find polygon layers (polygon or polygon25d)
    poly_layer = [layer for layer in dataSource if (
        layer.geom_type.name == 'Polygon' or
        layer.geom_type.name == 'Polygon25D')]

    firstLayer = None
    if poly_layer:
        logging.debug('Extracting poly')
        try:
            firstLayer = poly_layer[0]
        except Exception, e:
            logging.debug(traceback.format_exc())
            logging.debug('')
            logging.debug('Crashed: %s' % e)
        logging.debug('Extracting poly done')
    else:
        logging.debug('Failed - no polygon data')
        os.remove(os.path.join(settings.SHP_UPLOAD_DIR, zipfile))
        raise RuntimeError(
            'The geometry %s is not available in this KML.' % geometry)

    logging.debug('Full datasource name: %s' % dataSource.name)
    logging.debug('Number of available features: %s' % str(
        dataSource[0].num_feat))
    logging.debug('Geometry type: %s' % firstLayer.geom_type.name)
    logging.debug('Number of extracted features: %s' % str(numFeatures))

    # extract the N geometries, otherwise all of them
    if numFeatures != 'all':
        #if geos=True, geometry will be read as 2D, which is obligatory
        geometriesList = [
            pt.wkt for pt in firstLayer.get_geoms(geos=True)][0:numFeatures]
    else:
        geometriesList = [pt.wkt for pt in firstLayer.get_geoms(geos=True)]

    #clean up
    os.remove(os.path.join(settings.SHP_UPLOAD_DIR, zipfile))
    # return the data
    return geometriesList
