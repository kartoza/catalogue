"""
SANSA-EO Catalogue - mission_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.2'
__date__ = '09/08/2013'
__copyright__ = 'South African National Space Agency'

import os
import zipfile
from django.test import TestCase
from catalogue.views.helpers import writeThumbToZip


class ViewHelperTests(TestCase):

    def testWriteThumbToZip(self):
        """Test that we can write a thumb to a zip."""
        myZipPath = '/tmp/testWriteThumbToZip.zip'
        if os.path.exists(myZipPath):
            os.remove(myZipPath)
        myZip = zipfile.ZipFile(myZipPath, 'w', zipfile.ZIP_DEFLATED)
        myPath = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'sample_files',
                'sample_thumbnail.jpg'
            )
        )
        myMessage = 'Could not write thumb and wld into zip'
        myOutputName = 'test123'
        assert writeThumbToZip(myPath, myOutputName, myZip), myMessage
