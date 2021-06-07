"""
SANSA-EO Catalogue - Search API (TastyPie)

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
__date__ = '10/09/2013'
__copyright__ = 'South African National Space Agency'

from tastypie.api import Api

from search.api import SearchResultsResource, SearchRecordResource

from useraccounts.api import UserResource
from catalogue.api import OpticalProductResource

# register the api
v1_API = Api(api_name='v1')
v1_API.register(UserResource())
v1_API.register(SearchResultsResource())
# v1_API.register(SearchRecordResource())
v1_API.register(OpticalProductResource())
