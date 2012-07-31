"""
SANSA-EO Catalogue - search_cloudcover - test correctness of
    cloud cover search results

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


class SearchCloudCover_Test(SearchTestCase):
    """
    Tests Search Cloud Cover
    """

    def test_CloudCoverSearch(self):
        """
        Test cloud cover range:
        - with 10% or less - search 19
        - with 30% or less - search 20
        - with 60% or less - search 21
        - with 100% or less - search 22
        """
        myTestSearches = [19, 20, 21, 22]
        #we need to bound results
        myExpectedResults = [40, 50, 70, 100]

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
            assert mySearcher.mQuerySet.count() >= myExpectedResults[idx], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s expected:' % searchPK)
