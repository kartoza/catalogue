import os.path
from io import BytesIO
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
      'database': 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(
          user=settings.DATABASES['default']['USER'],
          password=settings.DATABASES['default'].get('PASSWORD', ''),
          host=settings.DATABASES['default'].get('HOST', 'localhost'),
          port=settings.DATABASES['default'].get('PORT', '5432'),
          name=settings.DATABASES['default']['NAME'],
      ),
      'mappings': os.path.join(os.path.dirname(__file__), 'mappings.py'),
      'table': 'pycsw_catalogue_view'
    },
     'logging': {
        'level': 'DEBUG',
    },
    'operations': {
         'GetRecordById': {
             'parameters': {
                 'outputSchema': {
                     'values': [
                         'http://www.opengis.net/cat/csw/2.0.2',
                         'http://www.isotc211.org/2005/gmd'
                     ]
                 }
             }
         }
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
        'provider_url': 'http://catalogue.sansa.org.za/csw',
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
        'contact_url': 'http://www.sansa.org.za/contact-us/sansa-earth-observation',
        'contact_hours': 'Unknown',
        'contact_instructions': 'Unknown',
        'contact_role': 'pointOfContact',
    }
}


@csrf_exempt
def csw(request):
    """CSW WSGI wrapper"""

    # Combine CSW and CONFIGURATION dictionaries
    mdict = dict(CSW, **CONFIGURATION)
    
    # Update the server URL dynamically
    server_url = '%s://%s%s' % (
        request.META['wsgi.url_scheme'],
        request.META['HTTP_HOST'],
        request.META['PATH_INFO'],
    )
    mdict['server']['url'] = server_url

    env = request.META.copy()
    env.update({
        'local.app_root': os.path.dirname(__file__),
        'REQUEST_URI': request.build_absolute_uri(),
        'wsgi.input': BytesIO(request.body),
    })

    csw_instance = server.Csw(mdict, env)
    http_status_code, response = csw_instance.dispatch_wsgi()
    return HttpResponse(
        response, 
        content_type=csw_instance.contenttype)
