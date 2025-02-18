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
    },
    'profiles': ['apiso', 'ebrim'],
    'manager': {
        'transactions': True
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
}

CSW = {
    'metadata': {
        'inspire': {
          'enabled': True,
          'languages_supported': ['eng'],
          'default_language': 'eng',
          'date': 'YYYY-MM-DD',
          'gemet_keywords': [],
          'conformity_service': 'notEvaluated',
          'contact_name': 'Organization Name',
          'contact_email': 'Email Address',
          'temp_extent': {
            'begin': 'YYYY-MM-DD',
            'end': 'YYYY-MM-DD'
          }
        },
        'identification': {
            'title': 'SANSA PyCSW Catalogue',
            'abstract': '',
            'keywords': ['sansa', 'pycsw', 'catalogue'],
            'keywords_type': 'theme',
            'fees': 'None',
            'accessconstraints': 'None',
        },
        'provider': {
          'name': 'South African National Space Agency (SANSA)',
          'url': 'http://catalogue.sansa.org.za/csw',
        },
        'contact': {
            'name': 'Unknown',
            'position': 'Unknown',
            'address': 'Unknown',
            'city': 'Unknown',
            'stateorprovince': 'Unknown',
            'postal': 'Unknown',
            'country': 'South Africa',
            'phone': 'Unknown',
            'fax': 'Unknown',
            'email': 'Unknown',
            'url': 'http://www.sansa.org.za/contact-us/sansa-earth-observation',
            'hours': 'Unknown',
            'instructions': 'Unknown',
            'role': 'pointOfContact',
        }
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
