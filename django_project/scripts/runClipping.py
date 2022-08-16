""" This script checks for new clipping requests in the Clip model and runs them.
It is run by a cronjob.
 """

#imports from Django
from django.conf import settings

# Models and forms for our app

# Tools to run gdal and ogrinfo and postgis commands
import shlex, subprocess

## use Python GDAL binding?

# 1. Filter Clip model for submitted requests.
toDoClips = Clip.objects.filter(status = "submitted")
# 2. For each of them:
for toDoClip in toDoClips:
    # Mark the request as "in process" so next run will ignore it.
    toDoClip.status = "in process"
    toDoClip.save()
    # Retrieve image (polygon is already in DB) - softcode path!
    #@FIXME that won't work - it's stored as the key not the value. Shit.
    myClipImage = toDoClip.image

    # Get bounding box
    myCoords= toDoClip.polygon.envelope
    # Swap the order as gdal_translate expects
    myExtent = "%s %s %s %s" % ( myCoords.min_x, myCoords.max_y, myCoords.max_x, myCoords.min_y )

    clippingDir = os.path.join(settings.CLIP_RESULT_PATH, toDoClip.guid)
    os.mkdir(clippingDir)

    # Convert polygons in gml to give them to gdal as a file. Rude creation of gml from valid gml one.
    gmlFile = open(os.path.join(clippingDir, 'boundary.gml'), 'w')
    gmlFile.write("""<?xml version="1.0" encoding="utf-8" ?>
          <ogr:FeatureCollection
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://ogr.maptools.org/ boundary.xsd"
            xmlns:ogr="http://ogr.maptools.org/"
            xmlns:gml="http://www.opengis.net/gml">
    <gml:featureMember>
      <ogr:boundary fid="F0">
        <ogr:geometryProperty>
                  """ +
    toDoClip.polygon.gml + """
    </ogr:geometryProperty>
      </ogr:boundary>
    </gml:featureMember>
  </ogr:FeatureCollection>"""
    )
    gmlFile.close()

    # Clip by bounding box
    myBBFileName = os.path.join(clippingDir, "clipbybb.tif")

    myGDALBBClipRaw = "/usr/local/bin/gdal_translate -projwin %s -of GTiff %s %s" % ( myExtent, myClipImage, myBBFileName )
    myGDALBBClip = shlex.split(myGDALBBClipRaw)
    myGDALBBClipProcess = subprocess.call(myGDALBBClip)

    # Clip by boundary
    myBoundaryFileName = os.path.join(clippingDir, "clipbyboundary.tif")
    myGDALBoundaryClipRaw = "gdalwarp -co COMPRESS=DEFLATE -co TILED=YES -of GTiff -r lanczos -cutline %s %s %s" \
              %(  gmlFile.name, myBBFileName , myBoundaryFileName )
    myGDALBoundaryClip = shlex.split(myGDALBoundaryClipRaw)
    myGDALBoundaryClipProcess = subprocess.call(myGDALBoundaryClip)

    # Mark the request as "completed"
    toDoClip.status = "completed"
    toDoClip.save()

    """
    # Send a mail to user with link to download
    myEmailSubject = 'SAC Clip ' + str(toDoClip.guid) + ' status update (' + toDoClip.status + ')'
    myEmailMessage = 'The status for clip request #' +  str(toDoClip.guid) + ' has changed. Please visit the order page:\n'
    #@TODO create view for clipping requests
    #myEmailMessage = myEmailMessage + 'http://' + settings.DOMAIN + '/vieworder/' + str(myOrder.id) + '/'
    send_mail(myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN,
              toDoClip.owner.email, fail_silently=False)
   """
