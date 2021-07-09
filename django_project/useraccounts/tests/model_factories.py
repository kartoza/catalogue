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
import datetime
from django.utils import timezone
from useraccounts.models import SansaUserProfile
from django.conf import settings
from django.contrib.contenttypes import models as ct_models
from django.contrib.auth.models import Group, Permission, User
from django import VERSION as DJANGO_VERSION


# class ContentTypeF(factory.django.DjangoModelFactory):
#     # FACTORY_FOR = ct_models.ContentType
#     class Meta:
#         model = ct_models.ContentType
#
#     name = factory.Sequence(lambda n: "content type %s" % n)
#
#
# class PermissionF(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Permission
#
#     name = factory.Sequence(lambda n: "permission%s" % n)
#     content_type = factory.SubFactory(ContentTypeF)
#     codename = factory.Sequence(lambda n: "factory_%s" % n)
#
#
# class GroupF(factory.django.DjangoModelFactory):
#
#     class Meta:
#         model = Group
#     # @classmethod
#     # def _setup_next_sequence(cls):
#     #     try:
#     #         return cls._associated_class.objects.values_list(
#     #             'id', flat=True).order_by('-id')[0] + 1
#     #     except IndexError:
#     #         return 0
#
#     name = factory.Sequence(lambda n: "group%s" % n)
#
#
# class UserF(factory.django.DjangoModelFactory):
#
#     class Meta:
#         model = User
#     # @classmethod
#     # def _setup_next_sequence(cls):
#     #     try:
#     #         return cls._associated_class.objects.values_list(
#     #             'id', flat=True).order_by('-id')[0] + 1
#     #     except IndexError:
#     #         return 0
#
#     username = factory.Sequence(lambda n: "username%s" % n)
#     first_name = factory.Sequence(lambda n: "first_name%s" % n)
#     last_name = factory.Sequence(lambda n: "last_name%s" % n)
#     email = factory.Sequence(lambda n: "email%s@example.com" % n)
#     password = ''
#     is_staff = False
#     is_active = True
#     is_superuser = False
#     if DJANGO_VERSION[:2] >= (1, 4) and settings.USE_TZ:
#         last_login = timezone.datetime(2000, 1, 1).replace(tzinfo=timezone.utc)
#         date_joined = timezone.datetime(1999, 1, 1).replace(
#             tzinfo=timezone.utc)
#     else:
#         last_login = datetime.datetime(2000, 1, 1)
#         date_joined = datetime.datetime(1999, 1, 1)
#
#     @classmethod
#     def _prepare(cls, create, **kwargs):
#         password = kwargs.pop('password', None)
#         user = super(UserF, cls)._prepare(create, **kwargs)
#         if password:
#             user.set_password(password)
#             if create:
#                 user.save()
#         return user


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
