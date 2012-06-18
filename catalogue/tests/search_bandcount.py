"""
SANSA-EO Catalogue - search_bandcount - test correctness of
    search results for band counts

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


class SearchBandCount_Test(SearchTestCase):
    """
    Tests Search Band Count
    """

    def test_Panchromatic_bandcount(self):
        """
        Test Panchromatic band count, range 0-2
        """
        myTestSearches = [5]
        myExpectedResults = [8]

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
                message='For search pk %s expected more then:' % searchPK)

    def test_Truecolor_bandcount(self):
        """
        Test Truecolor band count, range 3
        """
        myTestSearches = [6]
        myExpectedResults = [50]

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
                message='For search pk %s expected more then:' % searchPK)

    def test_Multispectral_bandcount(self):
        """
        Test Multispectral band count, range 4-8
        """
        myTestSearches = [7]
        myExpectedResults = [15]

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
                message='For search pk %s expected more then:' % searchPK)

    def test_Superspectral_bandcount(self):
        """
        Test Superspectral band count, range 9-40
        """
        myTestSearches = [8]
        myExpectedResults = [1]

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
                message='For search pk %s:' % searchPK)

    def test_Hyperspectral_bandcount(self):
        """
        Test Hyperspectral band count, range 41-1000
        """
        myTestSearches = [9]
        myExpectedResults = [1]

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
                message='For search pk %s:' % searchPK)
