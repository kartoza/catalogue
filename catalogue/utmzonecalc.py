"""
SANSA-EO Catalogue - Find UTMZones for a point

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

#calcualte center meridians of utmzones for the world
#we use list.index(center_meridian)+1 as UTM zone number
UTMZONES = [x * 6 + 3 for x in range(-30, 30)]


def utmZoneFromLatLon(theLon, theLat, theBuffer=0):
    """
    Returns textual representation of UTMZone for specified (lon, lat) pair
    """
    if theLon <= -180 or theLon >= 180:
        raise ValueError('Longitude value error: %d' % theLon)
    if theLat <= -90 or theLat >= 90:
        raise ValueError('Latitude value error: %d' % theLat)

    #look up zone using simple calculation, add 1 because lists are 0 based
    myZone = UTMZONES.index(int(theLon / 6) * 6 + 3) + 1

    if theBuffer:
        myZones = []
        for buf in range(-theBuffer, theBuffer + 1):
            tmp = myZone + buf
            #account for zones on the edges
            if tmp > 60:
                tmp = tmp - 60
            if tmp < 1:
                tmp = tmp + 60
            myZones.append(tmp)
    else:
        myZones = [myZone]

    myResult = []
    for zone in myZones:
        if theLat > 0:
            myHemisphere = 'N'
            myPrefix = '326'
        else:
            myHemisphere = 'S'
            myPrefix = '327'
        mySuffix = '%02d' % zone
        myResult.append((myPrefix + mySuffix, 'UTM' + mySuffix + myHemisphere))
    return myResult
