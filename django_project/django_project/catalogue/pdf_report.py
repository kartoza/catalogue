"""
SANSA-EO Catalogue - render template to pdf using pisa

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

import cgi
from io import BytesIO
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(),
                                content_type='application/pdf')
        # set content to 'attachment', so browsers download it
        response['Content-Disposition'] = 'attachment; filename=report.pdf'
        return response

    return HttpResponse(
        'We had some errors<pre>%s</pre>' % cgi.escape(html))
