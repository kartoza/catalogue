"""
SANSA-EO Catalogue - Search related views

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
__date__ = '24/02/2013'
__copyright__ = 'South African National Space Agency'

# python logger support to django logger middleware
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from .models import SearchRecord


class SearchView(object):
    """
    Common search view helper methods
    """
    def __init__(self, theRequest, theSearcher):

        self.mSearchRecords = []
        self.mExtent = None
        self.mQuerySet = theSearcher.mQuerySet
        self.mRequest = theRequest
        self.mSearch = theSearcher.mSearch
        self.search()

    def search(self):
        """
        Perform actual search, and paginate results
        """
        logger.debug('Starting search')

        # Paginate the results
        # self.mPaginator = Paginator(self.mQuerySet, settings.PAGE_SIZE)

        # try:
        #     self.mPageNo = int(self.mRequest.GET.get('page', '1'))
        # except ValueError:
        #     self.mPageNo = 1
        # logger.debug(
        #     'search by scene using paginator page... %s', str(self.mPageNo))
        # # If page request (9999) is out of range, deliver last page of results.
        # try:
        #     logger.debug('search by scene - getting page')
        #     self.mSearchPage = self.mPaginator.page(self.mPageNo)
        #     logger.debug('search by scene - search results paginated')
        # except (EmptyPage, InvalidPage):
        #     logger.debug(
        #         'search by scene - paginator page requested is out of range')
        #     self.mSearchPage = self.mPaginator.page(self.mPaginator.num_pages)

        myUnion = None
        for myObject in self.mQuerySet:
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
            # logger.debug('%s added to myRecords', myObject.product_id)
        if myUnion:
            self.mExtent = str(myUnion.extent)

        # -----------------------------------------------------
        # Wrap up now ...
        # -----------------------------------------------------
        logger.debug('search : wrapping up search result presentation')
        logger.debug('extent of search results page... %s', str(self.mExtent))
        return ()

    def templateData(self):
        """
        Return template data
        """
        return ({
            'mySearchGuid': self.mSearch.guid,
            # 'myMessages': self.mMessages,
            # 'myLayerDefinitions': self.mLayerDefinitions,
            # 'myThumbnails': self.mThumbnails,
            # 'myLayersList': self.mLayersList,
            # 'mySensor': self.mSearch.sensorsAsString(),
            'myRecords': self.mSearchRecords,
            'myQuerySet': self.mQuerySet,
            'myPage': self.mSearchPage,
            'myExtent': self.mExtent,
            'myPageNo': self.mPageNo,

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
            'myPaginator': self.mPaginator
        })
