"""
SANSA-EO Catalogue - Reads DIMS tar gnu zip compressed packages and extract
                     metadata and/or imagery and thumbnails

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
import re
import shutil
import tempfile
import tarfile
import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.geos import Polygon

try:
    import io as StringIO
except ImportError:
    import io

# Use faster lxml if available, fallback on pure python implementation
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree


class MetadataAlreadyAddedException(Exception):
    """
    Raised when a metadata for a given product_code is already present
    """
    pass


class MetadataNotFoundException(Exception):
    """
    Raised when a mandatory metadata for a given product_code cannot be found
    """
    pass


class dimsBase(object):
    """
    Stores common XML functions
    """
    # Namespaces
    NS = dict(
        xmlns="{http://www.isotc211.org/2005/gmd}",
        xmlns_gco="{http://www.isotc211.org/2005/gco}",
        xmlns_gts="{http://www.isotc211.org/2005/gts}",
        xmlns_gss="{http://www.isotc211.org/2005/gss}",
        xmlns_gsr="{http://www.isotc211.org/2005/gsr}",
        xmlns_xsi="{http://www.w3.org/2001/XMLSchema-instance}",
        xmlns_xlink="{http://www.w3.org/1999/xlink}",
        xmlns_gml="{http://www.opengis.net/gml}",
    )

    #TODO: missing from ISO 'spatial_coverage':     PolygonField
    # Replaceable targets
    METADATA = dict(
        product_date='//{xmlns}dateStamp/{xmlns_gco}Date',  # Product date
        file_identifier='//{xmlns}fileIdentifier/{xmlns_gco}CharacterString',
        vertical_cs='//{xmlns_gml}VerticalCS/{xmlns_gml}name',  # Projection
        processing_level_code=(
            '//{xmlns}processingLevelCode//{xmlns}code/{xmlns_gco}Character'
            'String'),
        cloud_cover_percentage='//{xmlns}cloudCoverPercentage/{xmlns_gco}Real',
        md_data_identification=(
            '//{xmlns}MD_DataIdentification//{xmlns}CI_Citation/{xmlns}title/'
            '{xmlns_gco}CharacterString'),
        md_product_date=(
            '//{xmlns}MD_DataIdentification//{xmlns}CI_Date//{xmlns_gco}Date'),
        md_abstract=(
            '//{xmlns}MD_DataIdentification/{xmlns}abstract/{xmlns_gco}'
            'CharacterString'),  # Sat & sensor description
        bbox_west=(
            '//{xmlns}EX_GeographicBoundingBox/{xmlns}westBoundLongitude/'
            '{xmlns_gco}Decimal'),
        bbox_east=(
            '//{xmlns}EX_GeographicBoundingBox/{xmlns}eastBoundLongitude/'
            '{xmlns_gco}Decimal'),
        bbox_north=(
            '//{xmlns}EX_GeographicBoundingBox/{xmlns}northBoundLatitude/'
            '{xmlns_gco}Decimal'),
        bbox_south=(
            '//{xmlns}EX_GeographicBoundingBox/{xmlns}southBoundLatitude/'
            '{xmlns_gco}Decimal'),
        image_quality_code=(
            '//{xmlns}imageQualityCode//{xmlns}code/{xmlns_gco}Character'
            'String'),
        spatial_coverage='//{xmlns}EX_BoundingPolygon//{xmlns_gml}coordinates',
        institution_name=(
            '//{xmlns}CI_ResponsibleParty/{xmlns}organisationName/{xmlns_gco}'
            'CharacterString'),
        institution_address=(
            '//{xmlns}CI_Address/{xmlns}deliveryPoint/{xmlns_gco}Character'
            'String'),
        institution_city=(
            '//{xmlns}CI_Address/{xmlns}city/{xmlns_gco}CharacterString'),
        institution_region=(
            '//{xmlns}CI_Address/{xmlns}administrativeArea/{xmlns_gco}'
            'CharacterString'),
        institution_postcode=(
            '//{xmlns}CI_Address/{xmlns}postalCode/{xmlns_gco}Character'
            'String'),
        institution_country=(
            '//{xmlns}CI_Address/{xmlns}country/{xmlns_gco}CharacterString'),
    )


class dimsReader(dimsBase):
    """
    This class, extracts metadata and thumbnails from an existing tar.gz
    package
    """

    def __init__(self, path):
        """
        Set the tarball file path and reads the package
        """
        logger.info('%s initialized' % self.__class__)
        self._path = path
        self._tar = None
        self._tar_index = None
        self._products = {}
        self._read()

    def _read(self):
        """
        Read the tar
        """
        self._tar = tarfile.open(self._path)
        self._tar_index = self._tar.getnames()

        # Scan for DIMS products
        for product_path in [x for x in self._tar_index if re.search(
                    self._tar_index[0] + '/' +
                    'Metadata/ISOMetadata/[^/]+/[^\.]+\.xml$', x)]:
            m = re.search('ISOMetadata/([^/]+)/([^/]+)\.xml$', product_path)
            processing_level_code, product = m.groups()
            logger.info("reading %s" % product)
            # extracts metadata
            metadata = self._read_metadata(product_path)
            self._products[product] = {
                'path': product_path,
                'xml': self._read_file(product_path),
                'metadata': metadata,
                'thumbnail': self._read_file(
                    product_path.replace('ISOMetadata', 'Thumbnails')
                    .replace('.xml', '.jpg')),
                'image': self._read_file(
                    re.sub(
                        '(.*DN_)([^/]+)(.*)', r'\1\2_DIMAP\3',
                        product_path.replace(
                            os.path.join('Metadata', 'ISOMetadata'),
                            os.path.join('Products', 'SacPackage', 'ORBIT'))
                        .replace('.xml', '.tif'))),
            }
            # Optional spatial_coverage
            if metadata.get('spatial_coverage'):
                # Extract coordinates
                myCoordinatesList = re.findall(
                    '(-?[\.0-9]+)', metadata['spatial_coverage'])
                coordinates = list(zip(*[
                    [float(j) for j in myCoordinatesList]
                    [i::2] for i in range(2)]))
                # Build tuple for polygon
                coordinates = coordinates + coordinates[0:1]
                # Builds polygon
                spatial_coverage = Polygon(coordinates)
                spatial_coverage.set_srid(4326)
            else:
                spatial_coverage = None
            self._products[product]['spatial_coverage'] = spatial_coverage

    def _read_metadata(self, product_path):
        """
        Extract metadata from an XML metadata file object and returns
        informations as a dictionary, parsing and validation is left to the
        calling program.
        """
        tree = etree.parse(self._read_file(product_path))
        metadata = {}
        for md_name, md_xpath in list(self.METADATA.items()):
            logger.info('searching for %s in path %s' % (md_name, md_xpath))
            try:
                metadata[md_name] = tree.find(md_xpath.format(**self.NS)).text
            except AttributeError:
                logger.debug('not found %s in path %s' % (md_name, md_xpath))
        logger.info("metadata: %s" % metadata)
        return metadata

    def _read_file(self, file_path):
        """
        Read a file from tar, returns a file-like handle
        """
        file_info = self._tar.getmember(file_path)
        return self._tar.extractfile(file_info)

    def get_products(self):
        """
        Returns all read data
        """
        return self._products

    def get_metadata(self, product_code):
        """
        Returns metadata for the given product_code
        """
        return self._products.get(product_code).get('metadata')

    def get_xml(self, product_code):
        """
        Returns metadata for the given product_code
        """
        return self._products.get(product_code).get('xml')

    def __str__(self):
        """
        Print
        """
        return 'DIMS Reader: %s ' % self._path


class dimsWriter(dimsBase):
    """
    This class takes a folders containing the package template and fill in the
    gaps.
    """

    def __init__(self, template_path, package_name):
        """
        Set the file path and reads the package
        """
        logger.info("%s initialized" % self.__class__)
        self._tmp = tempfile.mkdtemp()
        self._path = os.path.join(self._tmp, package_name)
        self._package_name = package_name
        self._xml_template = os.path.join(
            self._path, 'Metadata', 'ISOMetadata', 'ISOMetadata_template.xml')
        self._xml = {}
        self.template_path = template_path
        # makes a temporary copy of the template folder, all processing will
        # be done on the copy
        shutil.copytree(template_path, self._path)
        logger.info("template copied to %s" % self._path)

    def _create_processing_level_folders(self, processing_level_code):
        """
        Creates the processing levels folders
        """
        logger.info("Processing level code %s" % processing_level_code)
        myProcFolders = (
            os.path.join('Metadata', 'ISOMetadata'),
            os.path.join('Metadata', 'Thumbnails'))
        for p in myProcFolders:
            _p = os.path.join(self._path, p, processing_level_code)
            if not os.path.isdir(_p):
                logger.info("creating %s" % _p)
                os.makedirs(_p)

    @staticmethod
    def _get_metadata(product_data, key, silently_fail=False):
        """
        Returns a metadata value for a given product_code.
        If silently_fail is not set and metadata is not found then an
        exception is raised
        """
        try:
            product_data['metadata']
        except KeyError:
            MetadataNotFoundException(
                'metadata are completely missing from product data')
        try:
            return product_data['metadata'][key]
        except KeyError:
            if silently_fail:
                return None
            raise MetadataNotFoundException('%s not found' % key)

    @staticmethod
    def getXML(metadata, template_xml):
        """
        Returns ISOMetadata.xml content as a string
        """
        tree = etree.parse(template_xml)
        for md_name, md_xpath in list(dimsBase.METADATA.items()):
            logger.info('searching for %s in path %s' % (md_name, md_xpath))
            try:
                try:
                    #convert any value to unicode
                    _val = str(metadata[md_name])
                    tree.find(md_xpath.format(**dimsBase.NS)).text = _val
                    logger.info("adding %s = %s" % (md_name, _val))
                except (KeyError, AttributeError):
                    logger.debug(
                        'not found %s in path %s' % (md_name, md_xpath))
            except MetadataNotFoundException:
                logger.debug(
                    'searching for %s in path %s' % (md_name, md_xpath))
        return etree.tostring(tree)

    def _add_metadata(self, product_code, product_data):
        """
        Set metadata in the template
        """
        # Metadata
        _xml = os.path.join(
            self._path, 'Metadata', 'ISOMetadata',
            self._get_metadata(product_data, 'processing_level_code'),
            product_code + '.xml')

        self._xml[product_code] = _xml
        fh = open(_xml, 'w+')
        myPath = os.path.join(
            self.template_path, 'Metadata', 'ISOMetadata',
            'ISOMetadata_template.xml')
        fh.write(dimsWriter.getXML(product_data.get('metadata'), myPath))
        fh.close()
        logger.info("adding metadata to %s" % _xml)

    def _add_product(self, product_code, product_data):
        """
        Adds a single product
        """
        # Check if already added
        if product_code in self._xml:
            raise MetadataAlreadyAddedException
        self._create_processing_level_folders(
            self._get_metadata(product_data, 'processing_level_code'))
        # Adds the thumbnail, mandatory
        shutil.copy(
            product_data['thumbnail'],
            os.path.join(
                self._path, 'Metadata', 'Thumbnails',
                self._get_metadata(product_data, 'processing_level_code'),
                product_code + '.jpg'))
        # The product imagery itself is not mandatory
        try:
            if product_data['image']:
                # make sure the folders exists
                _p = os.path.join(
                    self._path, 'Products', 'SacPackage',
                    self._get_metadata(product_data, 'verticalcs_name'),
                    self._get_metadata(product_data, 'processing_level_code')
                    + '_DIMAP')
                try:
                    os.makedirs(_p)
                except OSError:
                    logger.warning('cannot create %s' % _p)
                # Copy the image, rename the file to match product_code and
                # keeps extension
                _image_path = os.path.join(
                    _p, product_code + os.path.splitext(
                        product_data['image'])[1])
                shutil.copy(product_data['image'], _image_path)
                logger.info("image saved in %s" % _image_path)
        except KeyError:
            logger.warning('no image data for %s' % product_code)

        self._add_metadata(product_code, product_data)

    def add_products(self, products_info):
        """
        Adds products to the archive directory.

        product_info must contain all the informations
        needed to create the product informations,
        files informations are passed as paths to the files

        See: tests for example usage.
        """
        for product_code, product_data in list(products_info.items()):
            self._add_product(product_code, product_data)

    def _get_tarball_name(self):
        """
        Returns the tarball name
        """
        return self._package_name + '.tar.gz'

    def _write(self, tar_path):
        """
        Creates the package
        """
        os.chdir(os.path.split(self._path)[0])
        tar_path = tar_path or os.path.join(
            os.getcwd(), self._get_tarball_name())
        tar = tarfile.open(tar_path, "w:gz")
        tar.add(
            self._package_name,
            exclude=lambda x: -1 != x.find('ISOMetadata_template'))
        tar.close()
        logger.info("writing tarball %s" % tar_path)
        return tar_path

    def write(self, tar_path=None):
        """
        Public api
        """
        return self._write(tar_path)

    def __str__(self):
        """
        Print
        """
        return 'DIMS Writer: %s ' % self._path
