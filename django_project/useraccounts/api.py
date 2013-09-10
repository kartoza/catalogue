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
__date__ = '09/09/2013'
__copyright__ = 'South African National Space Agency'

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
# from tastypie.authentication import SessionAuthentication


from django.contrib.auth.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        # authentication = SessionAuthentication()
        authorization = Authorization()
        # always_return_data = True
        include_resource_uri = False
        allowed_methods = ['get']
        fields = ['id', 'username']
