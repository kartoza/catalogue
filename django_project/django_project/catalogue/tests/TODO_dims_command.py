"""

Tests ingestion

>>> from django.core.management import call_command
>>> from catalogue.models import *

###############################################

Prepare testing, copying the package in a test folder

###############################################

>>> import shutil
>>> import os
>>> package = 'catalogue/tests/sample_files/ORD_420882_20110124_20110124_SPOT-_V01_1_copy.tar.gz'
>>> shutil.copy('catalogue/tests/sample_files/ORD_420882_20110124_20110124_SPOT-_V01_1.tar.gz', package)


Load an initial fixture with

>>> call_command('loaddata', 'fixtures/catalogue.json')
Installing json fixture 'fixtures/catalogue' from absolute path.
Installed ...

###############################################

Test ingestion

###############################################

>>> call_command('dims_ingest', keep=True, folder='catalogue/tests/sample_files/', glob='*_copy.tar.gz', license='CC-BY-SA', owner='LINFINITI', creating_software='QGIS')
Product S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT- imported.



###############################################

Test that everything was imported correctly

###############################################

>>> p=OpticalProduct.objects.get(product_id='S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT-')
>>> p.acquisition_mode
<AcquisitionMode: B:CAM2:HRG:S5>
>>> p.path
94
>>> p.row
367
>>> p.processing_level
<ProcessingLevel: Level 1A>
>>> p.license
<License: CC-BY-SA>
>>> p.owner
<Institution: LINFINITI>
>>> p.creating_software
<CreatingSoftware: QGIS>
>>> p.local_storage_path == os.path.join(p.productDirectory(), p.product_id + '.tif.bz2')
True

>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.jpg'))
True
>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.wld'))
True
>>> os.path.isfile(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.tif.bz2'))
True

Test that the package was not deleted

>>> os.path.isfile(package)
True



###############################################

Test update reading owner from metadata

###############################################


Delete the image so that we can test store_image=False

>>> os.remove(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.tif.bz2'))
>>> os.path.isfile(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.tif.bz2'))
False

Delete product

>>> p=OpticalProduct.objects.get(product_id='S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT-')
>>> p.delete()

Import

>>> call_command('dims_ingest', keep=True, folder='catalogue/tests/sample_files/', glob='*_copy.tar.gz', license='CC-BY-SA', creating_software='QGIS')
Product S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT- imported.

>>> p=OpticalProduct.objects.get(product_id='S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT-')
>>> p.owner
<Institution: CSIR Satellite Applications Centre>


###############################################

Test update

###############################################


Delete the image so that we can test store_image=False

>>> os.remove(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.tif.bz2'))
>>> os.path.isfile(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.tif.bz2'))
False

>>> p.row = 1
>>> new_license = License.objects.exclude(pk=p.license.pk)[0]
>>> p.license = new_license
>>> p.save()
>>> call_command('dims_ingest', store_image=False, keep=True, folder='catalogue/tests/sample_files/', glob='*_copy.tar.gz', license='CC-BY-SA', institution='LINFINITI', creating_software='QGIS')
Product S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT- updated.

>>> p=OpticalProduct.objects.get(product_id='S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT-')
>>> p.acquisition_mode
<AcquisitionMode: B:CAM2:HRG:S5>
>>> p.path
94
>>> p.row
1
>>> p.processing_level
<ProcessingLevel: Level 1A>
>>> p.license == new_license
True
>>> os.path.isfile(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.tif.bz2'))
False


Update again, test that image is imported and package deleted

>>> call_command('dims_ingest', folder='catalogue/tests/sample_files/', glob='*_copy.tar.gz', license='CC-BY-SA', institution='LINFINITI', creating_software='QGIS')
Product S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT- updated.
>>> os.path.isfile(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.tif.bz2'))
True
>>> os.path.isfile(package)
False

###############################################

Cleanup

###############################################


>>> os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.jpg'))
>>> os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.wld'))



"""
