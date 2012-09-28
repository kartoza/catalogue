"""
SANSA-EO Catalogue - test_utils - common test utils

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
__date__ = '13/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import Client
from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase

from catalogue.models import User


def simpleMessage(theResult, theExpectedResult, message='', enclose_in=''):
    """Format simple assert message

    Params:
        message - specify more expressive message
        enclose_in - character/text to enclose output with, helpful with strings,
            i.e. theString -> #theString#"""

    return '%(message)s\nGot: %(enclose_in)s%(result)s%(enclose_in)s \n\
Expected: %(enclose_in)s%(expectedResult)s%(enclose_in)s ' % {'message': message,
    'result': theResult, 'expectedResult': theExpectedResult, 'enclose_in': enclose_in}


#
# IMPORTANT: this is built-in class in Django 1.3
# https://docs.djangoproject.com/en/dev/topics/testing/#the-request-factory
# Take extra care on Django UPGRADE
#
class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.

    Usage:

    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})

    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client

    Once you have a request object you can pass it to any view function,
    just as if that view had been hooked up using a URLconf.

    """
    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)


class SearchTestCase(TestCase):
    """
    General Search Test Case
    """

    fixtures = [
        'test_user.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json'
        ]

    def setUp(self):
        """
        Set up before each test
        """
        self.factory = RequestFactory(enforce_csrf_checks=True)
        #authenticate
        self.factory.login(username='timlinux', password='password')
        #get user object
        self.user = User.objects.get(pk=1)
