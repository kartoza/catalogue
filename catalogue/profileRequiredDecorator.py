"""
SANSA-EO Catalogue - Decorator used for checking if user filled all profile
                     attributes

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
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

from django.http import HttpResponse, HttpResponseRedirect
import logging
# for error logging
import traceback
from functools import wraps


def requireProfile(theView):
    """
    This is a decorator that when used will ensure that the user
    has filled in all their personal details before being allowed
    to continue.

    example useage in your view:

    from catalogue.profileRequiredDecorator import requireProfile

    @requireProfile('demo')
    def demo(request):
        return {}

    The userprofile system will then redirect the user back to this page
    once they have completed their details.

    Note this will not check the validity of the profile, only its
        existance. It relies on the user profile form to ensure sufficient
        details are collected
    """
    def decorator(theFunction):
        def inner_decorator(theRequest, *args, **kwargs):
            try:
                myProfile = theRequest.user.get_profile()
                if myProfile and checkProfile(myProfile):
                    logging.info('User Profile is populated')
                    return theFunction(theRequest, *args, **kwargs)
                else:
                    logging.info('User Profile is NOT populated - redirecting')
                    if theRequest.is_ajax():
                        #we need to tell the client to do the redirection
                        # in this case...
                        myJscriptRelocate = """
                            <script>
                            window.location.replace(
                                "/accounts/profile/edit/personal/?next=/%s/");
                            </script>""" % theView
                        return HttpResponse(
                            myJscriptRelocate,
                            mimetype='application/javascript')
                    else:
                        return HttpResponseRedirect(
                            "/accounts/profile/edit/personal/?next=/%s/" %
                            theView)
            except:
                logging.info('User Profile exception - redirecting')
                logging.debug('User Profile exception - redirecting')
                logging.debug(traceback.format_exc())
                return HttpResponseRedirect(
                    '/accounts/profile/edit/personal/?next=/%s/' % theView)
        return wraps(theFunction)(inner_decorator)
    return decorator


def checkProfile(theProfile):
    """Does basic checking that required fields are not just populated with
      zero length strings."""
    if not (theProfile.firstname
            or theProfile.surname
            or theProfile.address1
            or theProfile.address2
            or theProfile.post_code
            or theProfile.organisation
            or theProfile.contact_no):
        return False
    else:
        return True
