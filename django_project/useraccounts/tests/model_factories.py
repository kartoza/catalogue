"""
SANSA-EO Catalogue - Dictionary model factories

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '09/08/2013'
__copyright__ = 'South African National Space Agency'

import factory

from ..models import SansaUserProfile


class SansaUserProfileF(factory.django.DjangoModelFactory):
    """
    SansaUserProfile model factory
    """
    class Meta:
        model = SansaUserProfile

    user = factory.SubFactory('core.model_factories.UserF')
    strategic_partner = False
    url = ''
    about = ''
    address1 = factory.Sequence(lambda n: "Addr1 {}".format(n))
    address2 = factory.Sequence(lambda n: "Addr2 {}".format(n))
    address3 = ''
    address4 = ''
    post_code = factory.Sequence(lambda n: "Post code {}".format(n))
    organisation = factory.Sequence(lambda n: "Organisation {}".format(n))
    contact_no = factory.Sequence(lambda n: "Contact No {}".format(n))
