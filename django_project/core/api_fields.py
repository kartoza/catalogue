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

from django.utils import six
from django.core.exceptions import ObjectDoesNotExist

from tastypie import fields
from tastypie.exceptions import ApiFieldError
from tastypie.bundle import Bundle


class ProductRelField(fields.ToOneField):
    """
    Provides access to related data via foreign key.

    This subclass requires Django's ORM layer to work properly.
    """
    help_text = (
        'A single related resource. Can be either a URI or set of nested '
        'resource data.'
    )

    def dehydrate(self, bundle, for_list=True):
        foreign_obj = None

        if isinstance(self.attribute, six.string_types):
            attrs = self.attribute.split('__')
            foreign_obj = bundle.obj

            for attr in attrs:
                try:
                    # make sure we get the concrete product instance
                    foreign_obj = getattr(
                        foreign_obj, attr, None).getConcreteInstance()
                except ObjectDoesNotExist:
                    foreign_obj = None
        elif callable(self.attribute):
            foreign_obj = self.attribute(bundle)

        if not foreign_obj:
            if not self.null:
                raise ApiFieldError((
                    'The model "%r" has an empty attribute "%s" and doesn\'t '
                    'allow a null value." % (previous_obj, attr)')
                )

            return None

        self.fk_resource = self.get_related_resource(foreign_obj)
        fk_bundle = Bundle(obj=foreign_obj, request=bundle.request)
        return self.dehydrate_related(
            fk_bundle, self.fk_resource, for_list=for_list)
