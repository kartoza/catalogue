"""
SANSA-EO Catalogue - GeoIPUtils helper class

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
__date__ = '17/08/2012'
__copyright__ = 'South African National Space Agency'


from django.contrib.gis.geoip import GeoIP
from django.conf import settings
import re  # regex support
import urllib.request, urllib.error, urllib.parse

# python logging support to django logging middleware
import logging
logger = logging.getLogger(__name__)

import traceback


class GeoIpUtils:
    """A class for resolving lat/long from and IP address"""
    def __init__(self):
        """Constructor"""
        return

    def __del__(self):
        """Destructor"""
        return

    def getMyIp(self, request):
        """
        Fetch an IP when request.META returns localhost
        """
        remote_ip = request.META['REMOTE_ADDR']
        if remote_ip == '127.0.0.1':
            checkip = urllib.request.urlopen('http://checkip.dyndns.org/').read()
            matcher = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            try:
                remote_ip = matcher.search(checkip).group()
            except:
                remote_ip = ''
        logger.info('Remote ip is: ' + remote_ip)
        return remote_ip

    def getMyLatLong(self, request):
        if settings.USE_GEOIP:
            g = GeoIP()
            remote_ip = self.getMyIp(request)
            try:
                remote_location = g.city(remote_ip)
                if remote_location:
                    logger.info(remote_location)
                    return remote_location
                else:  # ip cannot be found
                    logger.info('IP could not be looked up :-(')
                    return None
            except Exception:
                logger.info(traceback.format_exc())
                return None
        return None
