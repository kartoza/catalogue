#calcualte center meridians of utmzones for the world
#we use list.index(center_meridian)+1 as UTM zone number
utmzones = [x * 6 + 3 for x in range(-30, 30)]


def utmZoneFromLatLon(theLon, theLat, theBuffer=0):
    """
    Returns textual representation of UTMZone for specified (lon, lat) pair
    """
    if theLon <= -180 or theLon >= 180:
        raise ValueError("Longitude value error: %d" % theLon)
    if theLat <= -90 or theLat >= 90:
        raise ValueError("Latitude value error: %d" % theLat)

    #look up zone using simple calculation, add 1 because lists are 0 based
    myZone = utmzones.index(int(theLon / 6) * 6 + 3) + 1

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
            myPrefix = "326"
        else:
            myHemisphere = 'S'
            myPrefix = "327"
        mySuffix = "%02d" % zone
        myResult.append((myPrefix + mySuffix, "UTM" + mySuffix + myHemisphere))
    return myResult
