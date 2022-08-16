#
# Sort raw imagery into a standard folder heirachy
#
#
# to run do:
# source ../python/bin/activate
# python manage.py runscript sort_cbers_raw_imagery
# from the dir above scripts dir
import traceback
import sys

from django_project.catalogue.models import *
from settings import *

mSourcePath = "/mnt/cataloguestorage/imagery_processing/cbers/20081212_20100114/raw"

def run( ):
    myCwd = os.getcwd()
    os.chdir(mSourcePath)
    # We change to the source dir to avoid prefixing long paths into the tarball
    myErrorCount = 0
    myMissionAbbreviation = "C2B"
    myMission = Mission.objects.filter( abbreviation=myMissionAbbreviation )
    myProducts = GenericProduct.objects.filter( mission = myMission )
    for myProduct in myProducts:
        print myProduct.product_id
        myOutputPath = os.path.join( settings.IMAGERY_ROOT, myProduct.productDirectory().replace("1Ab","1Aa") )
        myOutputFile = os.path.join( myOutputPath, myProduct.product_id.replace("L1Ab","L1Aa") + ".bz2" )
        myImportRecord = None
        try:
            myImportRecord = Cbers.objects.get( sceneid = myProduct.original_product_id )
        except:
            print "No import record match (or too many matches) found for %s" % myProduct.original_product_id
            myErrorCount += 1
            continue


        mySourceDir = myImportRecord.source
        myTokens = mySourceDir.split('/')
        mySourceDir = os.path.join( myTokens[-2], myTokens[-1] )
        print "Source dir : %s" % mySourceDir
        if not os.path.isdir( myOutputPath ):
            print "Creating dir: %s" % myOutputPath
            try:
                os.makedirs( myOutputPath )
            except OSError:
                print "Failed to make output directory...quitting"
                return "False"
        else:
            print "Exists: %s" % myOutputPath
            pass
        # We make copies so we can rerun this script with a different naming scheme if needed
        if os.path.isfile( myOutputFile ): #dont try to recompress if it already exists
            print "File exists, skipping: %s" % myOutputFile
            continue
        if os.path.isdir( mySourceDir ): #dont try to recompress if it already exists
            try:
                # zip up the raw dir
                myCommand = "tar cfj %s %s" % ( myOutputFile, mySourceDir )
                print myCommand
                os.chdir(mSourcePath)
                print "Running from  %s " % os.getcwd()
                os.system( myCommand )
            except:
                traceback.print_exc( file=sys.stdout )
                myErrorCount += 1
        else:
            print "Source dir %s does not exist" % mySourceDir
            print "Running from %s " % os.getcwd()
            myErrorCount += 1

    os.chdir( myCwd )
    print "Files with errors: %s" % myErrorCount
