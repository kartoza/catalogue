"""
SANSA-EO Catalogue - Shopping cart views

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

import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
# For shopping cart and ajax product id search
import json as simplejson
from django.conf import settings
#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

# Models and forms for our app
from catalogue.renderDecorator import renderWithContext
from catalogue.models import (
    GenericProduct)

# Helper classes (render_as_kml, ...)
from catalogue.views.helpers import (
    render_to_kml,
    render_to_kmz,
    downloadHtmlMetadata,
    downloadISOMetadata)

from search.models import SearchRecord
###########################################################
#
# Shopping cart stuff
#
###########################################################
logger = logging.getLogger(__name__)

@login_required
def downloadCart(theRequest):
    """Dispaches request and returns products in cart in desired file format"""
    myRecords = SearchRecord.objects.all().filter(
        user=theRequest.user).filter(order__isnull=True)

    myFilename = '%s-cart' % theRequest.user.username
    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(myRecords)
        myResponder.file_name = myFilename
        return  myResponder.write_order_products(myRecords)
    elif 'kml' in theRequest.GET:
        return render_to_kml(
            'kml/searchRecords.kml', {
                'mySearchRecords': myRecords,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True},
            myFilename)
    elif 'kmz' in theRequest.GET:
        return render_to_kmz(
            'kml/searchRecords.kml', {
                'mySearchRecords': myRecords,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True,
                'myThumbsFlag': True},
            myFilename)
    else:
        logger.info(
            'Request cannot be proccesed, unsupported download file type')
        raise Http404


@login_required
def downloadCartMetadata(theRequest):
    """
    Returns ISO 19115 metadata for products in cart, unless request is
    suffixed with html
    """
    myRecords = SearchRecord.objects.all().filter(
        user=theRequest.user).filter(order__isnull=True)
    if 'html' in theRequest.GET:
        return downloadHtmlMetadata(
            myRecords, 'Cart-%s' % theRequest.user.username)
    else:
        return downloadISOMetadata(
            myRecords, 'Cart-%s' % theRequest.user.username)


@login_required
def addToCart(theRequest, theId):
    """
    Optionally we can return the response as json for ajax clients. We still
    keep normal html response to support clients with no ajax support. see
    http://www.b-list.org/weblog/2006/jul/31/django-tips-simple-ajax
        -example-part-1/
    """
    logger.info('addToCart : id ' + theId)
    # we need to check for the xhr param because response redirect
    # does not pass along the ajax request header to the redirect url
    # The redirected url needs to check for is_ajax or xhr to
    # decide how to respond# check if the post ended with /?xhr
    myAjaxFlag = 'xhr' in theRequest.GET or theRequest.is_ajax()

    # construct a record by passing some params
    myGenericProduct = GenericProduct.objects.get(id=theId)
    myDuplicateRecords = (
        SearchRecord.objects.filter(product=myGenericProduct)
        .filter(user=theRequest.user).filter(order__isnull=True))
    myResponse = None
    if len(myDuplicateRecords) == 0:
        myRecord = SearchRecord().create(theRequest.user, myGenericProduct)
        myRecord.save()
        logger.info('Adding item %s Cart :' + myRecord.product.product_id)
        if not myAjaxFlag:
            myResponse = HttpResponse(
                'Successfully added %s to your myCart' % (
                    myRecord.product.product_id,),
                content_type='text/html')
        else:
            myDict = {'Item': theId, 'Status': 'Added'}
            myResponse = HttpResponse(
                simplejson.dumps(myDict), content_type='application/json')
    else:
        logger.info('Adding item %s Cart failed (its a duplicate):' % (
            myGenericProduct.product_id,))
        if not myAjaxFlag:
            myResponse = HttpResponse(
                'alert("Item already exists in your cart!");',
                content_type='application/javascript')
        else:
            myResponse = HttpResponse(
                'Item already exists in your cart!',
                content_type='application/json', status='480')
    return myResponse


@login_required
def removeFromCart(theRequest, theId):
    myRecord = SearchRecord.objects.get(id=theId)
    if myRecord.user == theRequest.user:
        myRecord.delete()
        response = HttpResponse(
            'Successfully removed item from your basket',
            content_type='text/plain')
    else:
        response = HttpResponse(
            'You don\'t own this record so you can not delete it!',
            content_type='text/plain')
    return response


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('cartContentsPage.html', 'cartContents.html')
def showCartContents(theRequest):
    """
    Returns a nice table showing cart contents. Second template in method sig.
    is used in ajax requests.
    """
    myAjaxFlag = False
    if 'xhr' in theRequest.GET or theRequest.is_ajax():
        myAjaxFlag = True
    myRecords = (
        SearchRecord.objects.all().filter(user=theRequest.user)
        .filter(order__isnull=True))
    logger.info('Cart contains : %s items' % str(myRecords.count()))
    return ({
        'myRecords': myRecords,
        # Possible flags for the record template
        # myShowSensorFlag
        # myShowSceneIdFlag
        # myShowDateFlag
        # myShowCartFlag
        # myShowRemoveIconFlag
        # myShowPreviewFlag
        'myShowSensorFlag': False,
        'myShowSceneIdFlag': True,
        'myShowDateFlag': True,
        'myShowRemoveIconFlag': True,
        'myShowRowFlag': False,
        'myShowPathFlag': False,
        'myShowCloudCoverFlag': True,
        'myShowMetdataFlag': True,
        # used when you need to add an item to the cart only
        'myShowCartFlag': False,
        'myShowPreviewFlag': True,
        'myCartTitle': 'Cart Contents',
        'myAjaxFlag': myAjaxFlag,
        'myMiniCartFlag': False,
    })


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('cartContents.html')
def showMiniCartContents(theRequest):
    """Just returns a table element - meant for use with ajax"""
    myBaseTemplate = 'cartContentsPage.html'
    myAjaxFlag = 'xhr' in theRequest.GET
    if theRequest.is_ajax() or myAjaxFlag:
        # so template can render full page if not an ajax load
        myBaseTemplate = 'emptytemplate.html'
    myRecords = SearchRecord.objects.all().filter(
        user=theRequest.user).filter(order__isnull=True)
    logger.info('Cart contains : %s items' % str(myRecords.count()))
    return ({
        'myRecords': myRecords,
        # Possible flags for the record template
        # myShowSensorFlag
        # myShowSceneIdFlag
        # myShowDateFlag
        # myShowCartFlag
        # myShowRemoveFlag
        # myShowPreviewFlag
        'myShowSensorFlag': False,
        'myShowIdFlag': False,
        'myShowSceneIdFlag': True,
        'myShowDateFlag': False,
        'myShowRemoveIconFlag': True,
        'myShowRowFlag': False,
        'myShowPathFlag': False,
        'myShowCloudCoverFlag': False,
        'myShowMetdataFlag': False,
        # used when you need to add an item to the cart only
        'myShowCartFlag': False,
        # so the appropriate jscrip is called when entry is deleted
        'myShowMiniCartFlag': True,
        'myShowPreviewFlag': True,
        'myBaseTemplate': myBaseTemplate,
        'myMiniCartFlag': True
    })
