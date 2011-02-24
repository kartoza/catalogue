"""
Reads DIMS tar gnu zip compressed packages and extract metadata
and/or imagery and thumbnails
"""

import os
import re
import shutil
import tempfile
import tarfile
import logging
from datetime import datetime

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
      xmlns       = "{http://www.isotc211.org/2005/gmd}",
      xmlns_gco   = "{http://www.isotc211.org/2005/gco}",
      xmlns_gts   = "{http://www.isotc211.org/2005/gts}",
      xmlns_gss   = "{http://www.isotc211.org/2005/gss}",
      xmlns_gsr   = "{http://www.isotc211.org/2005/gsr}",
      xmlns_xsi   = "{http://www.w3.org/2001/XMLSchema-instance}",
      xmlns_xlink = "{http://www.w3.org/1999/xlink}",
      xmlns_gml   = "{http://www.opengis.net/gml}",
    )

  #TODO: missing from ISO 'spatial_coverage':     PolygonField
  # Replaceable targets
  METADATA = dict(
      product_date            = '//{xmlns}dateStamp/{xmlns_gco}Date', # Product date
      file_identifier         = '//{xmlns}fileIdentifier/{xmlns_gco}CharacterString',
      vertical_cs             = '//{xmlns_gml}VerticalCS/{xmlns_gml}name', # Projection
      processing_level_code   = '//{xmlns}processingLevelCode//{xmlns}code/{xmlns_gco}CharacterString',
      cloud_cover_percentage  = '//{xmlns}cloudCoverPercentage/{xmlns_gco}Real',
      md_data_identification  = '//{xmlns}MD_DataIdentification//{xmlns}CI_Citation/{xmlns}title/{xmlns_gco}CharacterString',
      md_product_date         = '//{xmlns}MD_DataIdentification//{xmlns}CI_Date//{xmlns_gco}Date',
      md_abstract             = '//{xmlns}MD_DataIdentification/{xmlns}abstract/{xmlns_gco}CharacterString', # Sat & sensor description
      bbox_west               = '//{xmlns}EX_GeographicBoundingBox/{xmlns}westBoundLongitude/{xmlns_gco}Decimal',
      bbox_east               = '//{xmlns}EX_GeographicBoundingBox/{xmlns}eastBoundLongitude/{xmlns_gco}Decimal',
      bbox_north              = '//{xmlns}EX_GeographicBoundingBox/{xmlns}northBoundLatitude/{xmlns_gco}Decimal',
      bbox_south              = '//{xmlns}EX_GeographicBoundingBox/{xmlns}southBoundLatitude/{xmlns_gco}Decimal',
      image_quality_code      = '//{xmlns}imageQualityCode//{xmlns}code/{xmlns_gco}CharacterString',
    )


class dimsReader(dimsBase):
  """
  This class, extracts metadata and thumbnails from an existing tar.gz package
  """

  def __init__(self, path):
    """
    Set the tarball file path and reads the package
    """
    logging.info("%s initialized" % self.__class__)
    self._path      = path
    self._tar       = None
    self._tar_index = None
    self._products  = {}
    self._read()


  def _read(self):
    """
    Read the tar
    """
    self._tar       = tarfile.open(self._path)
    self._tar_index = self._tar.getnames()

    # Scan for DIMS products
    for product_path in filter(lambda x: re.search(self._tar_index[0] + '/' + 'Metadata/ISOMetadata/[^/]+/[^\.]+\.xml$', x), self._tar_index):
      m = re.search('ISOMetadata/([^/]+)/([^/]+)\.xml$', product_path)
      processing_level_code, product = m.groups()
      logging.info("reading %s" % product)
      self._products[product] = {
          'path':       product_path,
          'metadata':   self._read_metadata(product_path),
          'thumbnail':  self._read_file(product_path.replace('ISOMetadata', 'Thumbnails').replace('.xml', '.jpg')),
        }


  def _read_metadata(self, product_path):
    """
    Extract metadata from an XML metadata file object and
    returns informations as a dictionary, parsing and validation
    is left to the calling program. The only check is done here is
    for mandatory metadata presence.
    """
    file_info = self._tar.getmember(product_path)
    file_handle = self._tar.extractfile(file_info)
    tree = etree.parse(file_handle)
    metadata = {}
    for md_name, md_xpath in self.METADATA.items():
      logging.info('searching for %s in path %s' % (md_name, md_xpath))
      try:
        metadata[md_name] = tree.find(md_xpath.format(**self.NS)).text
      except AttributeError:
        logging.warning('not found %s in path %s' % (md_name, md_xpath))
    logging.info("metadata: %s" % metadata)
    return metadata


  def _read_file(self, file_path):
    """
    Read a file from tar
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

  def __str__(self):
    """
    Print
    """
    return 'DIMS Reader: %s ' % self._path




class dimsWriter(dimsBase):
  """
  This class takes a folders containing the package template and fill in the gaps.
  """

  def __init__(self, template_path, package_name):
    """
    Set the file path and reads the package
    """
    logging.info("%s initialized" % self.__class__)
    self._tmp           = tempfile.mkdtemp()
    self._path          = os.path.join(self._tmp, package_name)
    self._package_name  = package_name
    self._xml_template  = os.path.join(self._path, 'Metadata', 'ISOMetadata', 'ISOMetadata_template.xml')
    self._xml           = {}
    # makes a temporary copy of the template folder, all processing will be done on the copy
    shutil.copytree(template_path, self._path)
    logging.info("template copied to %s" % self._path)


  def _create_processing_level_folders(self, processing_level_code):
    """
    Creates the processing levels folders
    """
    for p in (os.path.join('Metadata', 'ISOMetadata'), os.path.join('Metadata', 'Thumbnails')):
      _p = os.path.join(self._path, p, processing_level_code)
      if not os.path.isdir(_p):
        logging.info("creating %s" % _p)
        os.mkdir(_p)

  def _get_metadata(self, product_data, key, silently_fail=False):
    """
    Returns a metadata value for a given product_code.
    If silently_fail is not set and metadata is not found then an exception is raised
    """
    try:
      product_data['metadata']
    except KeyError:
      MetadataNotFoundException('metadata are completely missing from product data')
    try:
      return product_data['metadata'][key]
    except KeyError:
      if silently_fail:
        return None
      raise MetadataNotFoundException('%s not found' % key)

  def _add_metadata(self, product_code, product_data):
    """
    Set metadata in the template
    """
    # Metadata
    _xml = os.path.join(self._path, 'Metadata', 'ISOMetadata',
                        self._get_metadata(product_data, 'processing_level_code'),
                        product_code + '.xml')
    tree = etree.parse(self._xml_template)
    metadata = {}
    for md_name, md_xpath in self.METADATA.items():
      logging.info('searching for %s in path %s' % (md_name, md_xpath))
      try:
        _val =  self._get_metadata(product_data, md_name, True)
        try:
          tree.find(md_xpath.format(**self.NS)).text = _val
          logging.info("adding %s = %s" % (md_name, _val))
        except AttributeError:
          logging.warning('not found %s in path %s' % (md_name, md_xpath))
      except MetadataNotFoundException:
        print 'searching for %s in path %s' % (md_name, md_xpath)
    self._xml[product_code] = _xml
    tree.write(_xml)
    logging.info("adding metadata to %s" % _xml)


  def _add_product(self, product_code, product_data):
    """
    Adds a single product
    """
    # Check if already added
    if product_code in self._xml:
      raise MetadataAlreadyAddedException
    self._create_processing_level_folders(self._get_metadata(product_data, 'processing_level_code'))
    # Adds the thumbnail, mandatory
    shutil.copy(product_data['thumbnail'], os.path.join(self._path, 'Metadata', 'Thumbnails', self._get_metadata(product_data, 'processing_level_code'), product_code + '.jpg'))
    # The product imagery itself is not mandatory
    try:
      if product_data['image']:
        # make sure the folders exists
        _p = os.path.join(self._path, 'Products', 'SacPackage', self._get_metadata(product_data, 'verticalcs_name'),  self._get_metadata(product_data, 'processing_level_code') + '_DIMAP')
        try:
          os.makedirs(_p)
        except OSError:
          logging.warning('cannot create %s' % _p)
        # Copy the image, rename the file to match product_code and keeps extension
        _image_path = os.path.join(_p, product_code + os.path.splitext(product_data['image'])[1])
        shutil.copy(product_data['image'], _image_path)
        logging.info("image saved in %s" % _image_path)
    except KeyError:
        logging.warning('no image data for %s' % product_code)

    self._add_metadata(product_code, product_data)


  def add_products(self, products_info):
    """
    Adds products to the archive directory.

    product_info must contain all the informations
    needed to create the product informations,
    files informations are passed as paths to the files

    See: tests for example usage.
    """
    for product_code, product_data in products_info.items():
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
    tar_path = tar_path or os.path.join(os.getcwd(), self._get_tarball_name())
    tar = tarfile.open(tar_path, "w:gz")
    tar.add(self._package_name, exclude=lambda x: -1 != x.find('ISOMetadata_template'))
    tar.close()
    logging.info("writing tarball %s" % tar_path)
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
