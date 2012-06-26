from django import http
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
try:
    import ho.pisa as pisa
except:
    import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = http.HttpResponse(result.getvalue(), mimetype='application/pdf')
        #set content to 'attachment', so browsers download it
        response['Content-Disposition'] = 'attachment; filename=report.pdf'
        return response

    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
