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

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
import logging
logger = logging.getLogger(__name__)
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
        def inner_decorator(request, *args, **kwargs):
            profile = None
            try:
                profile = request.user.sansauserprofile
            except ObjectDoesNotExist:
                logger.info('User Profile exception - redirecting')
                logger.debug('User Profile exception - redirecting')
                logger.debug(traceback.format_exc())
            finally:
                # finally always executes, so we can safely redirect here
                if profile and check_profile(profile):
                    logger.info('User Profile is populated')
                    return theFunction(request, *args, **kwargs)
                else:
                    logger.info('User Profile is NOT populated - redirecting')
                    if request.is_ajax():
                        # we need to tell the client to do the redirection
                        # in this case...
                        script_relocate = """
                            <script>
                            window.location.replace(
                                "/accounts/{0}/edit/?next=/{1}/");
                            </script>""".format(profile.user, theView)
                        return HttpResponse(
                            script_relocate,
                            content_type='application/javascript'
                        )
                    else:
                        return HttpResponseRedirect(
                            "/accounts/{0}/edit/?next=/{1}/".format(profile.user, theView))

        return wraps(theFunction)(inner_decorator)
    return decorator


def check_profile(profile):
    """Does basic checking that required fields are not just populated with
      zero length strings."""
    if not (
            profile.user.first_name
            or profile.user.last_name
            or profile.address1
            or profile.address2
            or profile.post_code
            or profile.organisation
            or profile.contact_no
    ):
        return False
    else:
        return True
