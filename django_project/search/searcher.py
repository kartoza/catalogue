"""
SANSA-EO Catalogue - Search helper classes

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
__date__ = '16/02/2013'
__copyright__ = 'South African National Space Agency'

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from datetime import timedelta

from django.db.models import Q

# Models and forms for our app

from dictionaries.models import OpticalProductProfile
from dictionaries.models import SatelliteInstrumentGroup

from catalogue.fields import IntegersCSVIntervalsField
from catalogue.models import OpticalProduct


class Searcher:
    """
    This is a class that manages searches in the catalogue.
    Class members - variables declared here act like static class members in
    C++ i.e. if you change them from an object, all objects will receive that
    change.
    """

    def __init__(self, theSearch):

        self.mSearch = theSearch
        self.mExtent = None

        self.filterCriteria()

    def filterCriteria(self):
        """
        Construct search filter
        """

        myOPP = OpticalProductProfile.objects

        # make sure we return only products which are searchable
        myOPP = myOPP.only_searchable()

        # filter instrument type
        if self.mSearch.collection.count() > 0:
            myOPP = myOPP.for_collection(
                self.mSearch.collection)
            logger.debug(
                'OPP filter - collection %s',
                self.mSearch.collection.values_list('pk'))

        if self.mSearch.satellite.count() > 0:
            myOPP = myOPP.for_satellite(self.mSearch.satellite)
            logger.debug(
                'OPP filter - satellite %s',
                self.mSearch.satellite.values_list('pk'))

        # filter instrument type
        if self.mSearch.instrument_type.count() > 0:
            myOPP = myOPP.for_instrumenttypes(
                self.mSearch.instrument_type)
            logger.debug(
                'OPP filter - instrumenttype %s',
                self.mSearch.instrument_type.values_list('pk'))

        if self.mSearch.spectral_group.count() > 0:
            myOPP = myOPP.for_spectralgroup(self.mSearch.spectral_group)
            logger.debug(
                'OPP filter - spectralgroup %s',
                self.mSearch.spectral_group.values_list('pk'))

        # filter by licence
        if self.mSearch.license_type.count() > 0:
            myOPP = myOPP.for_licence_type(self.mSearch.license_type)
            logger.debug(
                'Licence filter %s',
                self.mSearch.license_type.values_list('pk')
            )

        self.mQuerySet = OpticalProduct.objects.filter(
            product_profile__in=myOPP)
        logger.info('Selected product profiles: %s', myOPP.values_list('pk'))

        # eliminate specific dates as specified in dictionaries_satelliteinstrumentgroup
        myAllowedDate = Q()
        for sig in SatelliteInstrumentGroup.objects.filter(
            satellite_id__in=self.mSearch.satellite.values_list('pk')).filter(
                instrument_type__in=self.mSearch.instrument_type.values_list('pk')):

            if sig.start_date and sig.end_date:
                sigEndDate = sig.end_date - timedelta(hours=1)
                myAllowedDate = (
                    myAllowedDate | Q(product_date__range=(sig.start_date, sigEndDate)))
        self.mQuerySet = self.mQuerySet.exclude(myAllowedDate)

        # filter date ranges
        if self.mSearch.searchdaterange_set.count():
            myDateQuery = Q()
            for date_range in self.mSearch.searchdaterange_set.all():
                # add one hour to end date to search in the last day
                # search for 01-03-2012 -> 01-03-2012 yields no results
                # because range only compares dates
                myEndDate = date_range.end_date + timedelta(hours=1)
                myDateQuery = (
                    myDateQuery | Q(product_date__range=(
                        date_range.start_date, myEndDate))
                )
                logger.debug(
                    'Daterange filter %s - %s',
                    date_range.start_date, myEndDate
                )
            self.mQuerySet = self.mQuerySet.filter(myDateQuery)

        # filter by sensor_inclination angle
        if (self.mSearch.sensor_inclination_angle_start is not None and
                self.mSearch.sensor_inclination_angle_end is not None):

            mySensorInclinationAngleQuery = Q(
                sensor_inclination_angle__range=(
                    self.mSearch.sensor_inclination_angle_start,
                    self.mSearch.sensor_inclination_angle_end)
            )
            self.mQuerySet = self.mQuerySet.filter(
                mySensorInclinationAngleQuery
            )
            logger.debug(
                'Sensor inclination angle filter %s-%s',
                self.mSearch.sensor_inclination_angle_start,
                self.mSearch.sensor_inclination_angle_end
            )

        # filter spatial resolution
        if self.mSearch.spatial_resolution is not None:
            mySpatialRes = self.mSearch.SPATIAL_RESOLUTION_RANGE.get(
                self.mSearch.spatial_resolution
            )
            mySpatialResQuery = Q(spatial_resolution__range=mySpatialRes)
            self.mQuerySet = self.mQuerySet.filter(mySpatialResQuery)
            logger.debug('Spatial resolution filter %s', mySpatialRes)

        # filter cloud cover
        if self.mSearch.cloud_min is not None and self.mSearch.cloud_max is not None:
            myCloudQuery = (
                Q(cloud_cover__gte=self.mSearch.cloud_min) &
                Q(cloud_cover__lte=self.mSearch.cloud_max) |
                Q(cloud_cover__isnull=True))
            self.mQuerySet = self.mQuerySet.filter(myCloudQuery)
            logger.debug('Cloud mean filter: %s - %s', self.mSearch.cloud_min, self.mSearch.cloud_max)

        # filter band_count
        if self.mSearch.band_count is not None:
            #get bandcount range
            myBandCountRange = (
                self.mSearch.BAND_COUNT_RANGE[self.mSearch.band_count]
            )
            myBandCountQuery = Q(band_count__range=myBandCountRange)
            self.mQuerySet = self.mQuerySet.filter(myBandCountQuery)
            logger.debug('Band count filter: %s', myBandCountRange)

        # filter k_orbit_path
        if self.mSearch.k_orbit_path:
            myKOrbitPathQ = Q()
            myParsedData = IntegersCSVIntervalsField.to_tuple(
                self.mSearch.k_orbit_path)
            for kpath in myParsedData:
                if len(kpath) == 2:
                    myKOrbitPathQ = (
                        myKOrbitPathQ | Q(path__range=(kpath[0], kpath[1])))
                else:
                    myKOrbitPathQ = myKOrbitPathQ | Q(path=kpath[0])
            self.mQuerySet = self.mQuerySet.filter(myKOrbitPathQ)
            logger.debug('K Orbit Path filter: %s', myParsedData)

        # filter j_frame_row
        if self.mSearch.j_frame_row:
            myJFrameRowQ = Q()
            myParsedData = IntegersCSVIntervalsField.to_tuple(
                self.mSearch.j_frame_row)
            for jrow in myParsedData:
                if len(jrow) == 2:
                    myJFrameRowQ = (
                        myJFrameRowQ | Q(row__range=(jrow[0], jrow[1])))
                else:
                    myJFrameRowQ = myJFrameRowQ | Q(row=jrow[0])
            self.mQuerySet = self.mQuerySet.filter(myJFrameRowQ)
            logger.debug('J Frame Row filter: %s', myParsedData)

        # filter geometry
        if self.mSearch.geometry:
            myGeometryQuery = Q(
                spatial_coverage__intersects=self.mSearch.geometry)
            self.mQuerySet = self.mQuerySet.filter(myGeometryQuery)
            logger.debug(
                'Geometry filter envelope: %s',
                self.mSearch.geometry.envelope.extent
            )

        # we could use select_related here, however we also need to test this
        # self.mQuerySet = self.mQuerySet.select_related()

        # Updates self.mSearch with the new object count
        myRecordCount = self.mQuerySet.count()
        logger.debug('Total records found: %s', myRecordCount)
        self.mSearch.record_count = myRecordCount
        self.mSearch.save()
