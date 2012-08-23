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
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import logging

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.conf import settings

# Models and forms for our app
from catalogue.models import (
    Search,
    SearchRecord,
    GenericSensorProduct,
    GeospatialProduct,
    RadarProduct,
    OpticalProduct,
    License)
from catalogue.forms import IntegersCSVIntervalsField
# for using django Q() query defs
from helpers import (
    standardLayersWithCart,)

DEFAULT_EXTENT = (
    '(-61.773122863038, -74.531249997024, 128.32031249488, 70.612614236677)')


class Searcher:
    """
    This is a class that manages searches in the catalogue.
    Class members - variables declared here act like static class members in
    C++ i.e. if you change them from an object, all objects will receive that
    change.
    """

    def clearTemplateData(self):
        """Clear the searcher data"""
        self.mMessages = []
        self.mThumbnails = []
        self.mRequest = None
        self.mSearch = None
        self.mSearchRecords = []
        self.mQuerySet = None
        self.mSearchPage = None
        self.mExtent = DEFAULT_EXTENT
        self.mPageNo = 1
        self.mSqlString = ''
        self.mLayerDefinitions = []
        self.mLayersList = ''
        self.mRecordCount = 0

    def templateData(self):
        """
        Return data from the searcher suitable for passing along to the
        map.html template
        """
        return ({
            'mySearchGuid': self.mSearch.guid,
            'myMessages': self.mMessages,
            'myLayerDefinitions': self.mLayerDefinitions,
            'myThumbnails': self.mThumbnails,
            'myLayersList': self.mLayersList,
            'mySensor': self.mSearch.sensorsAsString(),
            'myRecords': self.mSearchRecords,
            'myQuerySet': self.mQuerySet,
            'myPage': self.mSearchPage,
            'myExtent': self.mExtent,
            'myPageNo': self.mPageNo,
            'mySqlString': self.mSqlString,
            # Possible flags for the record template
            # myShowSensorFlag
            # myShowSceneIdFlag
            # myShowDateFlag
            # myShowCartFlag
            # myRemoveFlag
            # myShowHighlightFlag
            # myThumbFlag
            # myLegendFlag
            'myDetailFlag': True,
            'myShowSceneIdFlag': True,
            'myShowDateFlag': True,
            # used in cart contents listing context only
            'myShowRemoveIconFlag': False,
            'myShowHighlightFlag': True,
            'myShowRowFlag': False,
            'myShowPathFlag': False,
            'myShowCloudCoverFlag': True,
            'myShowMetadataFlag': True,
            'myShowCartFlag': True,
            'myShowPreviewFlag': True,
            'myLegendFlag': True,  # used to show the legend in the accordion
            'mySearchFlag': True,
            'myPaginator': self.mPaginator,
            'myProductIdSearch': (
                self.mSearch.search_type == Search.PRODUCT_SEARCH_OPTICAL),
        })

    def __del__(self):
        logging.info('Searcher destroyed')
        return

    def initQuery(self):
        """
        Setup the querySet configuring the filters
        """
        # -----------------------------------------------------
        # First fallback extent, will be overwritten by search geom extents if
        # there is a search geom
        self.mExtent = DEFAULT_EXTENT
        if self.mSearch.geometry:
            # Add the geometry of the search to the layers list for openlayers
            # to render
            self.mLayerDefinitions.append('''
var mySearchAreaLayer = new OpenLayers.Layer.Vector("Search Area");
var myGeojsonFormat = new OpenLayers.Format.GeoJSON();
var mySearchFeature = myGeojsonFormat.read(%s)[0];
mySearchFeature.geometry = transformGeometry( mySearchFeature.geometry );
mySearchAreaLayer.addFeatures(mySearchFeature);
mMap.addLayer(mySearchAreaLayer);''' % self.mSearch.geometry.geojson)
            # This will get overwritten by the extents of the page further
            # down here but its a good fallback in case there were no records
            self.mExtent = str(self.mSearch.geometry.envelope.extent)

        # ABP: Create the query set based on the type of class we're going to
        # search in
        assert (
            self.mSearch.search_type in
            dict(Search.PRODUCT_SEARCH_TYPES).keys())

        if (not self.mSearch.isAdvanced or
                self.mSearch.search_type == Search.PRODUCT_SEARCH_GENERIC):
            logging.info('Search type is PRODUCT_SEARCH_GENERIC')
            self.mSearch.search_type = Search.PRODUCT_SEARCH_GENERIC
            # ABP: changed simple search to GenericSensorProduct
            #      because sensors are now mandatory
            self.mQuerySet = GenericSensorProduct.objects.all()
        elif self.mSearch.search_type == Search.PRODUCT_SEARCH_OPTICAL:
            logging.info('Search type is PRODUCT_SEARCH_OPTICAL')
            self.mQuerySet = OpticalProduct.objects.all()
        elif self.mSearch.search_type == Search.PRODUCT_SEARCH_RADAR:
            logging.info('Search type is PRODUCT_SEARCH_RADAR')
            self.mQuerySet = RadarProduct.objects.all()
        elif self.mSearch.search_type == Search.PRODUCT_SEARCH_GEOSPATIAL:
            logging.info('Search type is PRODUCT_SEARCH_GEOSPATIAL')
            self.mQuerySet = GeospatialProduct.objects.all()
        elif self.mSearch.search_type == Search.PRODUCT_SEARCH_IMAGERY:
            logging.info('Search type is PRODUCT_SEARCH_IMAGERY')
            self.mQuerySet = GeospatialProduct.objects.all()

        # -----------------------------------------------------
        logging.info('filtering by search criteria ...')
        #
        # ABP: new logic is to get directly from the request which kind of
        # product to search on
        # ABP: common "simple search" parameters
        if self.mSearch.searchdaterange_set.count():
            self.mDateQuery = Q()
            for date_range in self.mSearch.searchdaterange_set.all():
                self.mDateQuery = (
                    self.mDateQuery | Q(
                        product_date__range=(
                            date_range.start_date, date_range.end_date)))
                # TODO: format dates in dd-mm-yyyy
                self.mMessages.append(
                    'date range <b>%s</b>' % date_range.local_format())
            self.mQuerySet = self.mQuerySet.filter(self.mDateQuery)

        if self.mSearch.geometry:
            self.mGeometryQuery = Q(
                spatial_coverage__intersects=self.mSearch.geometry)
            self.mQuerySet = self.mQuerySet.filter(self.mGeometryQuery)

        # ABP: sensors is mandatory ? Better if not enforced here: too bad in
        # product_id search!
        # assert self.mSearch.sensors.count() > 0,
        # "Search contains no sensors informations"
        if self.mSearch.sensors.count() > 0:
            try:
                #__in = match to one or more sensors
                self.mSensorQuery = Q(
                    acquisition_mode__sensor_type__mission_sensor__in=
                    self.mSearch.sensors.all())
                self.mQuerySet = self.mQuerySet.filter(self.mSensorQuery)
                self.mMessages.append(
                    'sensors <b>%s</b>' % self.mSearch.sensorsAsString())
                logging.info(
                    'Sensor in use is:' + str(
                        self.mSearch.sensors.values_list('name', flat=True)))
            except Exception, e:
                logging.error(
                    'QuerySet modification failed \n %s' % e.message())
                # This exception handler was added to prevent crashes here like
                # this:
                # FieldError: Cannot resolve keyword 'acquisition_mode' into
                # field. Choices are: GenericProduct_child,
                # GenericProduct_parent, children, creating_software,
                # data_type, description, equivalent_scale, genericproduct,
                # genericproduct_ptr, id, license, local_storage_path, metadata
                # name, original_product_id, owner, place, place_type,
                # primary_topic, processing_level, processing_notes,
                # product_date, product_id, product_revision, projection,
                # quality, remote_thumbnail_url, searchrecord,
                # spatial_coverage, temporal_extent_end, temporal_extent_start
                #
                # Somewhere generic product is being used for the search but
                # the form is allowing the selection of sensors.
                # This should be fixed.
                # Tim Nov 27 2011

        # ABP: paramters for "advanced search" only
        if self.mAdvancedFlag:
            logging.info('Search is advanced')
            # ABP: adds informations about search_type
            self.mMessages.append('search type <b>%s</b>' % dict(
                self.mSearch.PRODUCT_SEARCH_TYPES)[self.mSearch.search_type])
            # ABP: advanced search parameters, not sensor-specific
            if self.mSearch.license_type:
                self.mMessages.append(
                    'license type <b>%s</b>' % dict(
                        License.LICENSE_TYPE_CHOICES).get(
                            self.mSearch.license_type))
                # ABP: int dictionary
                self.mLicenseQuery = Q(
                    license__type=self.mSearch.license_type)
                self.mQuerySet = self.mQuerySet.filter(self.mLicenseQuery)

            # ABP: sensor only (advanced  query for Radar and Optical)
            # I don't really like this kind of checks... bad OOP ...
            # this should be sooner or later heavily refactored

            ##
            # radar and optical (genericsensor)
            #
            if self.mSearch.search_type in (
                    Search.PRODUCT_SEARCH_OPTICAL,
                    Search.PRODUCT_SEARCH_RADAR):
                logging.info('GenericSensorProduct advanced search activated')
                if self.mSearch.acquisition_mode:
                    self.mMessages.append(
                        'acquisition mode <b>%s</b>' % (
                            self.mSearch.acquisition_mode,))
                    self.mAcquisitionModeQuery = Q(
                        acquisition_mode=self.mSearch.acquisition_mode)
                    self.mQuerySet = self.mQuerySet.filter(
                        self.mAcquisitionModeQuery)
                if self.mSearch.mission:
                    self.mMessages.append(
                        'mission <b>%s</b>' % self.mSearch.mission)
                    self.mMissionQuery = Q(
                        acquisition_mode__sensor_type__mission_sensor__mission=
                        self.mSearch.mission)
                    self.mQuerySet = self.mQuerySet.filter(self.mMissionQuery)
                if self.mSearch.sensor_type:
                    self.mMessages.append(
                        'sensor type <b>%s</b>' % self.mSearch.sensor_type)
                    self.mSensorTypeQuery = Q(
                        acquisition_mode__sensor_type=self.mSearch.sensor_type)
                    self.mQuerySet = self.mQuerySet.filter(
                        self.mSensorTypeQuery)
                # Check for none since it can be 0
                if self.mSearch.spatial_resolution is not None:
                    # ABP: this needs special handling to map from classes to
                    # floats
                    self.mMessages.append(
                        'spatial resolution between <b>%sm and %sm</b>' % (
                            Search.SPATIAL_RESOLUTION_RANGE.get(
                                self.mSearch.spatial_resolution)),)
                    self.mSpatialResolutionQuery = Q(
                        spatial_resolution__range=
                        Search.SPATIAL_RESOLUTION_RANGE.get(
                            self.mSearch.spatial_resolution))
                    self.mQuerySet = self.mQuerySet.filter(
                        self.mSpatialResolutionQuery)
                # Check for none since it can be 0
                if self.mSearch.band_count is not None:
                    #get bandcount range
                    myBandcountRange = (
                        self.mSearch.BAND_COUNT_RANGE[self.mSearch.band_count])
                    self.mMessages.append(
                        'spectral resolution <b>%s->%s</b>' % myBandcountRange)
                    #create a range (BETWEEN) query
                    self.mSpectralResolutionQuery = Q(
                        band_count__range=myBandcountRange)
                    self.mQuerySet = self.mQuerySet.filter(
                        self.mSpectralResolutionQuery)
                logging.info(
                    'checking if we should use landsat path / row filtering..')
                if self.mSearch.k_orbit_path or self.mSearch.j_frame_row:
                    logging.info('path row filtering is enabled')
                    # used for scene searches only (landsat only)
                    if self.mSearch.k_orbit_path:
                        self.mKOrbitPathQuery = Q()
                        self.mMessages.append(
                            'Path: <b>%s</b>' % self.mSearch.k_orbit_path)
                        for _k in IntegersCSVIntervalsField.to_tuple(
                                self.mSearch.k_orbit_path):
                            if len(_k) == 2:
                                self.mKOrbitPathQuery = (
                                    self.mKOrbitPathQuery | Q(
                                        path__range=(_k[0], _k[1])))
                            else:
                                self.mKOrbitPathQuery = (
                                    self.mKOrbitPathQuery | Q(path=_k[0]))
                        self.mQuerySet = self.mQuerySet.filter(
                            self.mKOrbitPathQuery)
                    if self.mSearch.j_frame_row:
                        self.mJFrameRowQuery = Q()
                        self.mMessages.append(
                            'Row: <b>%s</b>' % self.mSearch.j_frame_row)
                        for _j in IntegersCSVIntervalsField.to_tuple(
                                self.mSearch.j_frame_row):
                            if len(_j) == 2:
                                self.mJFrameRowQuery = (
                                    self.mJFrameRowQuery | Q(
                                        row__range=(_j[0], _j[1])))
                            else:
                                self.mJFrameRowQuery = (
                                    self.mJFrameRowQuery | Q(row=_j[0]))
                        self.mQuerySet = self.mQuerySet.filter(
                            self.mJFrameRowQuery)
                else:
                    logging.info('path row filtering is DISABLED')

            ##
            # radar only
            #
            if self.mSearch.search_type == Search.PRODUCT_SEARCH_RADAR:
                logging.info('RadarProduct advanced search activated')
                if self.mSearch.polarising_mode:
                    self.mMessages.append(
                        'polarisation mode <b>%s</b>' % (
                            self.mSearch.polarising_mode,))
                    self.mPolarisingModeQuery = Q(
                        polarising_mode=self.mSearch.polarising_mode)
                    self.mQuerySet = self.mQuerySet.filter(
                        self.mPolarisingModeQuery)
            ##
            # optical only
            #
            if self.mSearch.search_type == Search.PRODUCT_SEARCH_OPTICAL:
                logging.info('OpticalProduct advanced search activated')
                if self.mSearch.use_cloud_cover and self.mSearch.cloud_mean:
                    self.mCloudQuery = (
                        Q(cloud_cover__lte=self.mSearch.cloud_mean)
                        | Q(cloud_cover__isnull=True))
                    self.mQuerySet = self.mQuerySet.filter(self.mCloudQuery)
                    self.mMessages.append(self.meanCloudString())

                if (self.mSearch.sensor_inclination_angle_start is not None and
                        self.mSearch.sensor_inclination_angle_end is not None):

                    assert (
                        (self.mSearch.sensor_inclination_angle_start <
                            self.mSearch.sensor_inclination_angle_end) or not
                        (self.mSearch.sensor_inclination_angle_start or
                            self.mSearch.sensor_inclination_angle_end),
                        'Search sensor_inclination_angle_start is not < '
                        'sensor_inclination_angle_end')

                    self.mSensorInclinationAngleQuery = Q(
                        sensor_inclination_angle__range=(
                            self.mSearch.sensor_inclination_angle_start,
                            self.mSearch.sensor_inclination_angle_end)
                    )
                    self.mQuerySet = self.mQuerySet.filter(
                        self.mSensorInclinationAngleQuery
                    )
                    self.mMessages.append(
                        'sensor inclination angle between <b> %s and %s</b>'
                        % (
                            self.mSearch.sensor_inclination_angle_start,
                            self.mSearch.sensor_inclination_angle_end))

            ##
            # geospatial only
            #
            if self.mSearch.search_type == Search.PRODUCT_SEARCH_GEOSPATIAL:
                logging.info('GeospatialProduct advanced search activated')

        else:
            logging.info('Search is simple (advanced flag is not set)')

        self.mSqlString = self.mQuerySet.query
        self.mRecordCount = self.mQuerySet.count()
        # Updates self.mSearch with the new count
        self.mSearch.record_count = self.mRecordCount
        self.mSearch.save()

    def __init__(self, theRequest, theGuid):

        self.mSearch = get_object_or_404(Search, guid=theGuid)

        # Queries
        self.mPageNo = 1

        # items that are passed back with templateData
        self.mMessages = []
        self.mThumbnails = []
        self.mSearchRecords = []
        self.mExtent = DEFAULT_EXTENT
        self.mRequest = theRequest
        self.mRecordCount = 0

        # ABP: is advanced ?
        self.mAdvancedFlag = self.mSearch.isAdvanced

        self.mSqlString = ""
        self.mLayersList, self.mLayerDefinitions, myActiveBaseMap = (
            standardLayersWithCart(theRequest))
        self.mSearchPage = None
        self.mPaginator = None
        self.initQuery()
        logging.info('Searcher initialised')

    def logResults(self):
        logging.info('New results: ')
        for myResult in self.mSearchRecords:
            logging.info('Result product: ' + str(myResult.product.product_id))
        return

    def search(self, thePaginateFlag=True):
        """Performs a search and shows a map of a single search for scenes"""
        logging.info('search by Scene paginating...')
        # Can also write the query like this:
        # mQuerySet = Localization.objects.filter(sensor=mSearch.sensor)
        # .filter(timeStamp__range=(mSearch.start_date,mSearch.end_date))
        # .filter(geometry__intersects=mSearch.geometry)
        #

        if thePaginateFlag:
            # only use this next line for serious debugging - its a performance
            # killer
            # logging.info(
            #    'search by scene pre-paginator count...' + str(
            #        self.mQuerySet.count()))
            # Paginate the results
            self.mPaginator = Paginator(self.mQuerySet, settings.PAGE_SIZE)
            # Make sure page request is an int. If not, deliver first page.
        else:
            self.mPaginator = Paginator(self.mQuerySet, self.mQuerySet.count())
        try:
            self.mPageNo = int(self.mRequest.GET.get('page', '1'))
        except ValueError:
            self.mPageNo = 1
        logging.info(
            'search by scene using paginator page...' + str(self.mPageNo))
        # If page request (9999) is out of range, deliver last page of results.
        try:
            logging.info('search by scene - getting page')
            self.mSearchPage = self.mPaginator.page(self.mPageNo)
            logging.info('search by scene - search results paginated')
        except (EmptyPage, InvalidPage):
            logging.info(
                'search by scene - paginator page requested is out of range')
            self.mSearchPage = self.mPaginator.page(self.mPaginator.num_pages)

        myUnion = None
        for myObject in self.mSearchPage.object_list:
            myRecord = SearchRecord()
            myRecord.product = myObject
            self.mSearchRecords.append(myRecord)
            if not myUnion:
                # We only union the envelopes as we are only interested in
                # the rectangular extents of all features, not their geometric
                # union
                myUnion = myObject.spatial_coverage.envelope
            else:
                # This can be done faster using cascaded union but needs
                # geos 3.1
                myUnion = myUnion.union(myObject.spatial_coverage.envelope)
            logging.info('%s added to myRecords' % myObject.product_id)
        if myUnion:
            self.mExtent = str(myUnion.extent)

        # -----------------------------------------------------
        # Wrap up now ...
        # -----------------------------------------------------
        logging.info('search : wrapping up search result presentation')
        logging.info('extent of search results page...' + str(self.mExtent))
        self.logResults()
        return ()

    def meanCloudString(self):
        myCloudAsPercent = None
        if self.mSearch.cloud_mean:
            myCloudAsPercent = int(self.mSearch.cloud_mean) * 10
        else:
            myCloudAsPercent = 0
        # %% is to escape the percent symbol so we get a % literal
        myString = 'with a maximum cloud cover of %s%%' % myCloudAsPercent
        return myString

    def describeQuery(self, unset_only=False):
        """
        Returns a struct with messages and SQL of mSearch query

        unset_only parameter, define if the list of values should be returned
        only when the corresponding search values is not set
        """
        # Get option for all related fields, exclude users

        assert (
            self.mSearch.search_type == Search.PRODUCT_SEARCH_OPTICAL or
            self.mSearch.search_type == Search.PRODUCT_SEARCH_RADAR,
            'Search type is GENERIC')

        values = {}
        mySearchFields = [
            f.name for f in self.mSearch._meta.fields
            if f.rel and f.name != 'user']

        for field_name in mySearchFields:
            if not unset_only or not getattr(self.mSearch, field_name, None):
                values[field_name] = self.getOption(field_name)
        # m2m
        if not unset_only or not getattr(self.mSearch, 'sensors').count():
            values['sensors'] = self.getOption('mission_sensor')
        if not unset_only or not getattr(self.mSearch, 'license').count():
            values['license'] = self.getOption('license')

        if settings.DEBUG:
            query = '%s' % self.mSqlString
        else:
            query = ''
        return {
            'messages': self.mMessages,
            'query': query,
            'count': self.mRecordCount,
            'values': values}

    def getOption(self, field_name):
        """
        Returns a list of possible values that selected search parameters can
        assume for a given field
        """
        return list(
            self.mQuerySet.distinct().values_list(
                self.mSearch.getDictionaryMap(field_name), flat=True)
            .order_by())
