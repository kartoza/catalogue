import os.path
from configparser import SafeConfigParser

# from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pycsw import server


CONFIGURATION = {
    'server': {
        'home': '.',
        'mimetype': 'application/xml; charset=UTF-8',
        'encoding': 'UTF-8',
        'language': 'en-US',
        'maxrecords': '10',
        'pretty_print': 'true',
        'profiles': 'apiso'
    },
    'manager': {
        'transactions': 'false'
    },
    'repository': {
        'database': 'postgresql+psycopg2://%s:@/%s' % (
            settings.DATABASES['default']['USER'],
            settings.DATABASES['default']['NAME'],
        ),
        'mappings': os.path.join(os.path.dirname(__file__), 'mappings.py'),
        'table': 'pycsw_catalogue'
    },
}

CSW = {
    'metadata:main': {
        'identification_title': 'SANSA PyCSW Catalogue',
        'identification_abstract': '',
        'identification_keywords': 'sansa, pycsw, catalogue',
        'identification_keywords_type': 'theme',
        'identification_fees': 'None',
        'identification_accessconstraints': 'None',
        'provider_name': 'South African National Space Agency (SANSA)',
        'provider_url': 'http://41.74.158.4/csw',
        'contact_name': 'Unknown',
        'contact_position': 'Unknown',
        'contact_address': 'Unknown',
        'contact_city': 'Unknown',
        'contact_stateorprovince': 'Unknown',
        'contact_postalcode': 'Unknown',
        'contact_country': 'South Africa',
        'contact_phone': 'Unknown',
        'contact_fax': 'Unknown',
        'contact_email': 'Unknown',
        'contact_url': (
            'http://www.sansa.org.za/contact-us/sansa-earth-observation'
        ),
        'contact_hours': 'Unknown',
        'contact_instructions': 'Unknown',
        'contact_role': 'pointOfContact',
    }
}


@csrf_exempt
def csw(request):
    """CSW WSGI wrapper"""
    # serialize settings.CSW into SafeConfigParser
    # object for interaction with pycsw
    mdict = dict(CSW, **CONFIGURATION)

    # TODO: pass just dict when pycsw supports it
    config = SafeConfigParser()
    for section, options in mdict.items():
        config.add_section(section)
        for k, v in options.items():
            config.set(section, k, v)

    # update server.url
    server_url = '%s://%s%s' % \
        (request.META['wsgi.url_scheme'],
         request.META['HTTP_HOST'],
         request.META['PATH_INFO'])

    config.set('server', 'url', server_url)

    env = request.META.copy()
    env.update({
        'local.app_root': os.path.dirname(__file__),
        'REQUEST_URI': request.build_absolute_uri(),
    })
    csw = server.Csw(config, env)
    content = csw.dispatch_wsgi()
    return HttpResponse(content, content_type=csw.contenttype)
