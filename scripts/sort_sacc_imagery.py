#
# Sort raw imagery into a standard folder heirachy
#
#
#  To execute this script do:
#  source ../python/bin/activate   <--activate your virtual environment
#  python manage.py runscript --pythonpath=scripts -v 2 sort_sacc_imagery
#  deactivate
#
# from the dir above scripts dir
#
from catalogue.models import *
from settings import *
import traceback
import sys
import shutil
mSourcePath = "/mnt/cataloguestorage/imagery_processing/sacc/20080929_20091231/imp/"

def run( ):
  myErrorCount = 0
  myMissionAbbreviation = "S-C"
  myMission = Mission.objects.filter( abbreviation=myMissionAbbreviation )
  myProducts = GenericProduct.objects.filter( mission = myMission )
  for myProduct in myProducts:
    print myProduct.product_id
    myOutputPath = os.path.join( settings.IMAGERY_ROOT, myProduct.imagePath() )
    myOutputFile = os.path.join( myOutputPath, myProduct.product_id + ".tif.bz2" )
    myOriginalPixFile = os.path.join( mSourcePath, myProduct.original_product_id + ".pix" )
    mySourceFile = os.path.join( mSourcePath, myProduct.product_id + ".tif" )
    myBzipSourceFile = os.path.join( mSourcePath, myProduct.product_id + ".tif.bz2" )
    if os.path.isfile( myOriginalPixFile ):
      myString = "gdal_translate -of GTIFF %s %s" % ( myOriginalPixFile, mySourceFile )
      print myString
      os.system( myString )
      os.system( "bzip2 %s" % mySourceFile )
    if not os.path.isdir( myOutputPath ):
      #print "Creating dir: %s" % myOutputPath
      try:
        os.makedirs( myOutputPath )
      except OSError:
        print "Failed to make output directory...quitting"
        return "False"
    else:
      #print "Exists: %s" % myOutputPath
      pass
    print "Copy: %s to %s" % (mySourceFile, myOutputFile)
    try:
      shutil.move( myBzipSourceFile  , myOutputFile )
      myRelativePath = os.path.join( myProduct.imagePath(), myProduct.product_id + ".tif.bz2" )
      print "Local storage path: %s" % myRelativePath
      myProduct.local_storage_path = myRelativePath
      myProduct.save()
    except:
      traceback.print_exc(file=sys.stdout)
      myErrorCount += 1
  print "Files with errors: %s" % myErrorCount
