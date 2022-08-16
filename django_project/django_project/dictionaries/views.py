"""
SANSA-EO Catalogue - Ancillary Dictionary models

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__date__ = '01/11/2012'
__copyright__ = 'South African National Space Agency'

from django.shortcuts import render_to_response

from.models import (
    Collection,
    Satellite
)


def collectionList(theRequest):
    """Produce a nice report for all satellites.

    Args:
       None

    Returns:
        HttpResponse: An html snippet with detailed info for a satellite.

    Raises:
        None
    """
    myCollection = Collection.objects.all()

    return render_to_response(
        'dictionaries/collectionList.html',
        {
            'collection': myCollection,
        },
    )


def satelliteDetails(theRequest, theSatelliteId):
    """Produce a nice report for a satellite.

    Args:
        theSatelliteId: int - pkey of the satellite to produce the report for.

    Returns:
        HttpResponse: An html snippet with detailed info for a satellite.

    Raises:
        None
    """
    mySatellite = Satellite.objects.get(id=theSatelliteId)

    return render_to_response(
        'dictionaries/satelliteDetails.html',
        {
            'satellite': mySatellite,
        },
    )
