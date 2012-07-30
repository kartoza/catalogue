"""
SANSA-EO Catalogue - search_inclinationangle - test correctness of
    search results for inclinationangle

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


class SearchIncliantionAngle_Test(SearchTestCase):
    """
    Tests Search Inclination Angle
    """

    def test_InclinationAngleRange(self):
        """
        Test inclination angle range:
            - 0-90 (positive) (search 10)
            - -90-0 (negative) (search 11)
            - -10-10 (normal) (search 12)
        """
        myTestSearches = [10, 11, 12]
        #we need to bound results
        myExpectedResults = [(50, 60), (35, 50), (25, 40)]

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
            assert mySearcher.mQuerySet.count() >= myExpectedResults[idx][0] and \
            mySearcher.mQuerySet.count() <= myExpectedResults[idx][1], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s expected in range:' % searchPK)
