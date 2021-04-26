"""
SANSA-EO Catalogue - AOIGeometry form field

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

import logging
logger = logging.getLogger(__name__)

from django import forms
from django.contrib.gis.geos import Point, Polygon


class AOIGeometryField(forms.CharField):
    widget = forms.TextInput

    def __init__(self, *args, **kwargs):
        super(AOIGeometryField, self).__init__(*args, **kwargs)
        #if we dont supply help_text use this as default
        if not('help_text' in kwargs):
            self.help_text = (
                'Upper left and lower right coordinates e.g. (20,-32,22,-34). '
                'Or circle center and radius e.g. (20,-32,100).')

    def clean(self, theValue):
        """ AOI geometry validator """
        if not theValue:
            #do nothing, return empty string ''
            return ''
        else:
            try:
                myFields = theValue.split(',')

                #test if fields can be converted to nunbers
                try:
                    myFields = [float(field) for field in myFields]
                except:
                    logger.info(
                        'AOI geometry: invalid input values, can\'t be '
                        'converted tu numbers: %s' % (theValue))
                    raise

                #point and radius validation
                if len(myFields) == 3:
                    logger.info('AOI geometry: point and radius validation')
                    if myFields[0] <= -180 or myFields[0] >= 180:
                        logger.info(
                            'AOI geometry: point longitude not in -180..180 '
                            'range: %f' % (myFields[0]))
                        raise
                    if myFields[1] <= -90 or myFields[1] >= 90:
                        logger.info(
                            'AOI geometry: point latitude not in -90..90 '
                            'range: %f' % (myFields[1]))
                        raise
                    if myFields[2] <= 0:
                        logger.info(
                            'AOI geometry: radius equal or less then Zero: %f'
                            % (myFields[2]))
                        raise
                #bbox validation
                elif len(myFields) == 4:
                    logger.info('AOI geometry: bbox validation')
                    if myFields[0] <= -180 or myFields[0] >= 180:
                        logger.info(
                            'AOI geometry: west longitude not in -180..180 '
                            'range: %f' % (myFields[0]))
                        raise
                    if myFields[2] <= -180 or myFields[2] >= 180:
                        logger.info(
                            'AOI geometry: east longitude not in -180..180 '
                            'range: %f' % (myFields[2]))
                        raise
                    if myFields[1] <= -90 or myFields[1] >= 90:
                        logger.info(
                            'AOI geometry: north latitude not in -90..90 '
                            'range: %f' % (myFields[1]))
                        raise
                    if myFields[3] <= -90 or myFields[3] >= 90:
                        logger.info(
                            'AOI geometry: south latitude not in -90..90 '
                            'range: %f' % (myFields[3]))
                        raise
                    #check bbox
                    if myFields[0] > myFields[2]:
                        logger.info(
                            'AOI geometry: west edge can\'t be after east '
                            'edge: %f<%f' % (myFields[0], myFields[2]))
                        raise

                    if myFields[3] > myFields[1]:
                        logger.info(
                            'AOI geometry: south edge can\'t be after north '
                            'edge: %f<%f' % (myFields[1], myFields[3]))
                        raise

                    if myFields[0] == myFields[2]:
                        logger.info(
                            'AOI geometry: west edge and east edge are '
                            'identical: %f=%f' % (myFields[0], myFields[2]))
                        raise
                    if myFields[1] == myFields[3]:
                        logger.info(
                            'AOI geometry: north edge and south edge are '
                            'identical: %f=%f' % (myFields[1], myFields[3]))
                        raise
                #unexpected number of arguments
                else:
                    logger.info(
                        'AOI geometry: unexpected number of arguments: (%i),%s'
                        % (len(myFields), theValue))
                    raise
            except Exception as e:
                logger.info(str(e))
                raise forms.ValidationError(
                    'Area of interest geometry is not valid.')

        return self.to_python(myFields)

    def to_python(self, theValue):
        if len(theValue) == 3:
            #calculate radius in degrees 1 deg ~= 111 km
            myRadius = theValue[2] / 111.
            myGeometry = Point(theValue[0], theValue[1]).buffer(myRadius)
        else:
            myGeometry = Polygon.from_bbox(
                (theValue[0], theValue[1], theValue[2], theValue[3]))
        #set srid
        myGeometry.set_srid(4326)
        #geos must output geom as ewkt, because wkt doesm't contain SRID info
        return myGeometry.ewkt
