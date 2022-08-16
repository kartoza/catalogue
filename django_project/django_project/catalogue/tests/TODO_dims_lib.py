"""

Unit tests for DIMS



Tests reader

>>> import os
>>> from catalogue.dims_lib import dimsWriter, dimsReader
>>> d = dimsReader(os.path.join(os.path.split(__file__)[0], 'sample_files', 'ORD_420882_20110124_20110124_SPOT-_V01_1.tar.gz'))
>>> products = d.get_products()
>>> product_code = products.keys()[0]
>>> products[product_code]['thumbnail']
<tarfile.ExFileObject object at ...>
>>> products[product_code]['xml']
<tarfile.ExFileObject object at ...>
>>> products[product_code]['image']
<tarfile.ExFileObject object at ...>

>>> md = d.get_metadata(product_code)
>>> md.get('cloud_cover_percentage') == None
True
>>> md.get('file_identifier') == 'S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT--Vers.0.01'
True
>>> md.get('md_abstract').find('The SPOT high resolution optical') != -1
True
>>> md.get('md_product_date') == '2011-01-22T09:25:57.000'
True
>>> md.get('processing_level_code') == 'L1A'
True
>>> md.get('product_date') == '2011-01-24T14:29:43.278'
True
>>> md.get('vertical_cs') == 'ORBIT'
True
>>> md.get('md_data_identification') == 'SPOT5.HRG.L1A'
True
>>> md.get('image_quality_code') == 'aaaabaaaaaaaaa'
True
>>> d.get_xml(product_code)
<tarfile.ExFileObject object at ...>

>>> md.get('institution_name') == 'CSIR Satellite Applications Centre'
True
>>> md.get('institution_address') == 'PO Box 395'
True
>>> md.get('institution_city') == 'Pretoria'
True
>>> md.get('institution_region') == 'Gauteng'
True
>>> md.get('institution_postcode') == '0001'
True
>>> md.get('institution_country') == 'South Africa'
True



Tests writer

>>> d  = dimsWriter('resources/PackageTemplate', '0000000001')
>>> products = {}
>>> products['PRODUCT_00001'] = {}
>>> products['PRODUCT_00001']['thumbnail']= 'catalogue/tests/sample_files/sample_thumbnail.jpg'
>>> products['PRODUCT_00001']['image'] = 'catalogue/tests/sample_files/sample_image.tif'
>>> products['PRODUCT_00001']['metadata'] = {}
>>> products['PRODUCT_00001']['metadata']['product_date'] = '2011-01-24T14:29:43.278'
>>> products['PRODUCT_00001']['metadata']['md_data_identification'] = 'SPOT5.HRG.L1A'
>>> products['PRODUCT_00001']['metadata']['processing_level_code'] = 'DN_L1A'
>>> products['PRODUCT_00001']['metadata']['verticalcs_name'] = 'ORBIT'
>>> d.add_products(products)
>>> tar_path = d.write()
>>> os.path.split(tar_path)[1]
'0000000001.tar.gz'

Now tests that the test image and thumbnail are really in the tarball

>>> import tarfile
>>> t = tarfile.open(tar_path, 'r:gz')
>>> '0000000001/Products/SacPackage/ORBIT/DN_L1A_DIMAP/PRODUCT_00001.tif' in t.getnames()
True
>>> '0000000001/Metadata/ISOMetadata/DN_L1A/PRODUCT_00001.xml' in t.getnames()
True
>>> '0000000001/Metadata/Thumbnails/DN_L1A/PRODUCT_00001.jpg' in t.getnames()
True
>>> '0000000001/Metadata/ISOMetadata/ISOMetadata_template.xml' in  t.getnames()
False


Test XML metadata export

>>> from lxml import etree
>>> xml = etree.parse(os.path.join( tar_path[:-7], 'Metadata/ISOMetadata/DN_L1A/PRODUCT_00001.xml'))
>>> xml.find('//{http://www.isotc211.org/2005/gmd}dateStamp/{http://www.isotc211.org/2005/gco}Date').text
'2011-01-24T14:29:43.278'
>>> xml.find('//{http://www.isotc211.org/2005/gmd}MD_DataIdentification//{http://www.isotc211.org/2005/gmd}CI_Citation/{http://www.isotc211.org/2005/gmd}title/{http://www.isotc211.org/2005/gco}CharacterString').text
'SPOT5.HRG.L1A'


Test save to a given path

>>> import tempfile
>>> dir = tempfile.mkdtemp()
>>> tar_path = os.path.join(dir, 'test0001.tar.gz')
>>> tar_path2 = d.write(tar_path)
>>> tar_path == tar_path2
True
>>> os.path.split(tar_path2)[1]
'test0001.tar.gz'


Now tests that the test image and thumbnail are really in the tarball

>>> import tarfile
>>> t = tarfile.open(tar_path2, 'r:gz')
>>> '0000000001/Products/SacPackage/ORBIT/DN_L1A_DIMAP/PRODUCT_00001.tif' in t.getnames()
True
>>> '0000000001/Products/SacPackage/ORBIT/DN_L1A_DIMAP/PRODUCT_00001.tif' in t.getnames()
True
>>> '0000000001/Metadata/ISOMetadata/DN_L1A/PRODUCT_00001.xml' in t.getnames()
True
>>> '0000000001/Metadata/Thumbnails/DN_L1A/PRODUCT_00001.jpg' in t.getnames()
True
>>> '0000000001/Metadata/ISOMetadata/ISOMetadata_template.xml' in  t.getnames()
False


Tests getXML static method

>>> from lxml import etree
>>> from django.conf import settings
>>> products['PRODUCT_00001']['metadata']['product_date'] = '2001-space-odissey'
>>> xml = dimsWriter.getXML(products['PRODUCT_00001']['metadata'], os.path.join(settings.PROJECT_ROOT, 'resources/PackageTemplate/Metadata/ISOMetadata/ISOMetadata_template.xml'))
>>> len(xml) > 0
True
>>> tree = etree.fromstring(xml)
>>> tree.getroottree().find(dimsWriter.METADATA['product_date'].format(**dimsWriter.NS)).text == products['PRODUCT_00001']['metadata']['product_date']
True


"""
