"""
SANSA-EO Catalogue - search_rowpath - test correctness of
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
__date__ = '21/06/2012'
__copyright__ = 'South African National Space Agency'

from catalogue.tests.test_utils import simpleMessage, SearchTestCase
from catalogue.views.searcher import Searcher
from catalogue.models import Search


class SearchRowPath_Test(SearchTestCase):
    """
    Tests Search Row/Path
    """

    def test_RowPathRange(self):
        """
        Test row/path searches:
        - row 319 - search 23
        - path 144 - search 24
        - row 412 and path 137 - search 25
        - row 380-390, 391 and path 144, 100-120 - search 26
        """
        myTestSearches = [23, 24, 25, 26]
        #we need to bound results
        myExpectedResults = [4, 4, 2, 4]

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
