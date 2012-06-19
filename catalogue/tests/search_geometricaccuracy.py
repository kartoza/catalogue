"""
SANSA-EO Catalogue - search_geometricaccuracy - test correctness of
    search results for geometric accuracy -(spatial resolution)

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '18/06/2012'
__copyright__ = 'South African National Space Agency'

from catalogue.tests.test_utils import simpleMessage, SearchTestCase
from catalogue.views.searcher import Searcher
from catalogue.models import Search


class SearchGeometricAccuracy_Test(SearchTestCase):
    """
    Tests Search Geometric Accuracy
    """

    def test_GeometricAccuracy(self):
        """
        Test geometric accuracy:
        -   0 - '<= 1m' (search 13),
        -   1 - '1m - 2m' (search 14),
        -   2 - '2m - 6m' (search 15),
        -   3 - '6m - 20m' (search 16),
        -   4 - '20m - 35m' (search 17),
        -   5 - '35m - 60m' (search 18),
        """
        myTestSearches = [13, 14, 15, 16, 17, 18]
        #we need to bound results
        myExpectedResults = [1, 1, 1, 1, 1, 1]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            #create a fake request object
            request = self.factory.get(
                '/searchresult/%s' % mySearch.guid)
            #assign user to request (usually done by middleware)
            request.user = self.user

            #create Searcher object
            mySearcher = Searcher(request, mySearch.guid)
            mySearcher.search()
            assert mySearcher.mQuerySet.count() == myExpectedResults[idx], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s expected:' % searchPK)
