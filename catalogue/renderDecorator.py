"""
SANSA-EO Catalogue - Decorator used to always pass RenderContext to the
                     template

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


from django.shortcuts import render_to_response
from django.template import RequestContext
from pdfReport import render_to_pdf


class renderWithContext(object):
    """
    This is a decorator that when used will always pass the RequestContext
    over to the template. This is needed in tandem with the authentication
    stuff so that the templates can know who the logged in users is
    and perform conditional rendering based on that.

    example useage in your view:

    from catalogue.renderDecorator import renderWithContext

    @renderWithContext('demo.html')
    def demo(request):
        return {}

    The template will then have the RequestContext passed to it along
    automatically,  along with any other parameters your view defines.
    """
    def __init__(self, template_name, ajax_template_name=None):
        self.template_name = template_name
        self.ajax_template_name = ajax_template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            if request.is_ajax():
                if self.ajax_template_name:
                    render_template = self.ajax_template_name
                else:
                    #if request is really ajax and uses single template,
                    #use template_name
                    render_template = self.template_name
            else:
                render_template = self.template_name

            items = func(request, *args, **kwargs)
            #check for PDF arg
            if 'pdf' in request.GET:
                tmp_template_name = '/'.join(['pdf', self.template_name])
                return render_to_pdf(tmp_template_name, items)

            return render_to_response(
                render_template, items,
                context_instance=RequestContext(request))

        return rendered_func
