"""
SANSA-EO Catalogue - searcher_object - tests correctness of
    search results

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
__date__ = '14/06/2012'
__copyright__ = 'South African National Space Agency'

from catalogue.tests.test_utils import simpleMessage, SearchTestCase
from catalogue.models import Search


class SearcherObject_Test(SearchTestCase):
    """
    Tests Searcher object
    """

    def test_isAdvanced(self):
        """
        Tests if search is an advanced search
        """
        #test searches pk
        myTestSearches = [1, 4, 5, 6]
        myExpectedResults = [False, False, True, True]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            assert mySearch.isAdvanced == myExpectedResults[idx], \
            simpleMessage(mySearch.isAdvanced, myExpectedResults[idx],
                message='For search pk %s:' % searchPK)
