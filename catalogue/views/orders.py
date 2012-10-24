"""
SANSA-EO Catalogue - Order related views

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
import datetime
import traceback

from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect)
from django.core.paginator import (
    Paginator,
    EmptyPage,
    InvalidPage)
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings
# for aggregate queries
from django.db.models import Count

from django.contrib.gis.gdal import (
    SpatialReference,
    CoordTransform)
# Models and forms for our app
from catalogue.models import (
    Order,
    OrderStatusHistory,
    SearchRecord,
    DeliveryDetail,
    OrderStatus,
    TaskingRequest,
    MissionSensor)

from catalogue.forms import (
    OrderStatusHistoryForm,
    ProductDeliveryDetailForm,
    DeliveryDetailForm,
    OrderForm)
# Helper classes
from catalogue.views.helpers import (
    notifySalesStaff,
    notifySalesStaffOfTaskRequest,
    standardLayers,
    render_to_kml,
    render_to_kmz,
    downloadISOMetadata,
    downloadHtmlMetadata,)
# SHP and KML readers
from catalogue.featureReaders import getGeometryFromUploadedFile
from catalogue.utmzonecalc import utmZoneFromLatLon
from catalogue.profileRequiredDecorator import requireProfile
from catalogue.renderDecorator import renderWithContext

#other modules
from shapes.views import ShpResponder

###########################################################
#
# Ordering related views
#
###########################################################


@login_required
@renderWithContext('orderListPage.html', 'orderList.html')
def myOrders(theRequest):
    '''Non staff users can only see their own orders listed'''
    myRecords = Order.base_objects.filter(
        user=theRequest.user).order_by('-order_date')
    # Paginate the results
    if 'pdf' in theRequest.GET:
        myPageSize = myRecords.count()
    else:
        myPageSize = 100
    myPaginator = Paginator(myRecords, myPageSize)
    # Make sure page request is an int. If not, deliver first page.
    try:
        myPage = int(theRequest.GET.get('page', '1'))
    except ValueError:
        myPage = 1
        logging.info('Order list page request defaulting to page 1'
                     ' because on an error in pagination')
    # If page request (9999) is out of range, deliver last page of results.
    try:
        myRecords = myPaginator.page(myPage)
    except (EmptyPage, InvalidPage):
        myRecords = myPaginator.page(myPaginator.num_pages)
    myUrl = 'myorders'
    #render_to_response is done by the renderWithContext decorator
    return ({
        'myRecords': myRecords,
        'myUrl': myUrl
    })


@login_required
@renderWithContext('orderListPage.html', 'orderList.html')
def listOrders(theRequest):
    myRecords = None
    if not theRequest.user.is_staff:
        '''Non staff users can only see their own orders listed'''
        myRecords = Order.base_objects.filter(
            user=theRequest.user).order_by('-order_date')
    else:
        '''This view is strictly for staff only'''
        # This view uses the NoSubclassManager
        # base_objects is defined in the model and
        # will exclude all tasking requests or other
        # derived classes
        myRecords = Order.base_objects.all().order_by('-order_date')
    if 'pdf' in theRequest.GET:
        myPageSize = myRecords.count()
    else:
        myPageSize = 100
    if myPageSize == 0:
        # Prevent divide by zero crash
        myPageSize = 1
    # Paginate the results
    try:
        myPage = int(theRequest.GET.get('page', '1'))
    except ValueError:
        myPage = 1
    myPaginator = Paginator(myRecords, myPageSize)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        myRecords = myPaginator.page(myPage)
    except (EmptyPage, InvalidPage):
        myRecords = myPaginator.page(myPaginator.num_pages)
    myUrl = 'listorders'
    #render_to_response is done by the renderWithContext decorator
    return ({
        'myRecords': myRecords,
        'myUrl': myUrl,
        'myCurrentMonth': datetime.date.today()
    })


@login_required
@renderWithContext('orderMonthlyReport.html')
def orderMonthlyReport(theRequest, theyear, themonth):
    #construct date object
    if not(theyear and themonth):
        myDate = datetime.date.today()
    else:
        try:
            myDate = datetime.date(int(theyear), int(themonth), 1)
        except:
            logging.error('Date arguments cannot be parsed')
            logging.info(traceback.format_exc())

    if not theRequest.user.is_staff:
        '''Non staff users can only see their own orders listed'''
        myRecords = (Order.base_objects.filter(
            user=theRequest.user)
            .filter(
                order_date__month=myDate.month)
            .filter(
                order_date__year=myDate.year)
            .order_by('order_date'))
    else:
        '''This view is strictly for staff only'''
        myRecords = (
            Order.base_objects.filter(
                order_date__month=myDate.month)
            .filter(
                order_date__year=myDate.year)
            .order_by('order_date'))

    return ({
        'myRecords': myRecords,
        'myCurrentDate': myDate,
        'myPrevDate': myDate - datetime.timedelta(days=1),
        'myNextDate': myDate + datetime.timedelta(days=31)
    })


@login_required
def downloadOrder(theRequest, theId):
    """Dispaches request and returns geometry of ordered products in
       desired file format"""
    myOrder = get_object_or_404(Order, id=theId)

    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(myOrder)
        myResponder.file_name = u'products_for_order_%s' % myOrder.id
        return  myResponder.write_order_products(
            myOrder.searchrecord_set.all())
    elif 'kml' in theRequest.GET:
        return render_to_kml('kml/searchRecords.kml', {
            'mySearchRecords': myOrder.searchrecord_set.all(),
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True
        }, u'products_for_order_%s' % myOrder.id)
    elif 'kmz' in theRequest.GET:
        return render_to_kmz('kml/searchRecords.kml', {
            'mySearchRecords': myOrder.searchrecord_set.all(),
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True,
            'myThumbsFlag': True
        }, u'products_for_order_%s' % myOrder.id)
    else:
        logging.info('Request cannot be proccesed,'
                     ' unsupported download file type')
        raise Http404


@staff_member_required
def downloadClipGeometry(theRequest, theId):
    """Dispaches request and returns clip geometry
       for order in desired file format"""
    myOrder = get_object_or_404(Order, id=theId)

    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(myOrder)
        myResponder.file_name = u'clip_geometry_order_%s' % myOrder.id
        return  myResponder.write_delivery_details(myOrder)
    elif 'kml' in theRequest.GET:
        return render_to_kml(
            'kml/clipGeometry.kml', {
                'order': myOrder,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True
            }, u'clip_geometry_order_%s' % myOrder.id)
    elif 'kmz' in theRequest.GET:
        return render_to_kmz(
            'kml/clipGeometry.kml', {
                'order': myOrder,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True,
                'myThumbsFlag': True
            }, u'clip_geometry_order_%s' % myOrder.id)
    else:
        logging.info('Request cannot be processed,'
                     ' unsupported download file type')
        raise Http404


@login_required
def downloadOrderMetadata(theRequest, theId):
    """Returns ISO 19115 metadata for ordered products
      unless the request is suffixed by ?html"""
    myOrder = get_object_or_404(Order, id=theId)
    if 'html' in theRequest.GET:
        return downloadHtmlMetadata(
            myOrder.searchrecord_set.all(), 'Order-%s' % myOrder.id)
    else:
        return downloadISOMetadata(
            myOrder.searchrecord_set.all(), 'Order-%s' % myOrder.id)


@login_required
def viewOrder(theRequest, theId):
    """This view is strictly for staff only or the order owner"""
    # check if the post ended with /?xhr
    # we do this as well as is_ajax call because we
    # may have arrived at this page via a response redirect
    # which will not then have the is_ajax flag set
    myAjaxFlag = 'xhr' in theRequest.GET
    myTemplatePath = 'orderPage.html'
    if theRequest.is_ajax() or myAjaxFlag:
        # No page container needed, just a snippet
        myTemplatePath = 'orderPageAjax.html'
        logging.debug('Request is ajax enabled')
    myOrder = get_object_or_404(Order, id=theId)
    myRecords = SearchRecord.objects.all().filter(order=myOrder)
    myCoverage = coverageForOrder(myOrder, myRecords)
    if not ((myOrder.user == theRequest.user) or (theRequest.user.is_staff)):
        raise Http404
    myHistory = OrderStatusHistory.objects.all().filter(order=myOrder)
    myForm = None
    if theRequest.user.is_staff:
        myForm = OrderStatusHistoryForm()
    #render_to_response is done by the renderWithContext decorator
    return render_to_response(myTemplatePath, {
        'myOrder': myOrder,
        'myRecords': myRecords,
        # Possible flags for the record template
        # myShowSensorFlag
        # myShowSceneIdFlag
        # myShowDateFlag
        # myCartFlag
        # myRemoveFlag
        # myThumbFlag
        # myShowDeliveryDetailsFlag
        # myShowDeliveryDetailsFormFlag
        # myDownloadOrderFlag
        'myShowSensorFlag': False,
        'myShowSceneIdFlag': True,
        'myShowDateFlag': False,
        # cant remove stuff after order was placed
        'myRemoveFlag': False,
        'myThumbFlag': False,
        'myShowMetdataFlag': False,
        # used when you need to add an item to the cart only
        'myCartFlag': False,
        'myPreviewFlag': False,
        'myShowDeliveryDetailsFlag': True,
        'myShowDeliveryDetailsFormFlag': False,
        'myDownloadOrderFlag': True,
        'myForm': myForm,
        'myHistory': myHistory,
        'myCartTitle': 'Product List',
        'myCoverage': myCoverage,
    }, context_instance=RequestContext(theRequest))


def coverageForOrder(theOrder, theSearchRecords):
    """A small helper function to compute the coverage area. Logic is:
       - if AOI specified, the union of the products is clipped by the AOI
       - if no AOI is specified the area of the union of the products is
         returned.
       returns a dict with keys containing area properties for the order:
        ProductArea - total area of the union of all ordered products
        CentroidZone - UTM zone at cenroid of union of all ordered products
        IntersectedArea - area of union of all products intersected with AOI
       """
    myCoverage = {}
    myUnion = None
    myCentroid = None
    myZones = []
    try:
        for myRecord in theSearchRecords:
            myGeometry = myRecord.product.spatial_coverage
            if not myUnion:
                myUnion = myGeometry
            else:
                # This can be done faster using cascaded union
                # but needs geos 3.1
                myUnion = myUnion.union(myGeometry)
        if myUnion:
            myCentroid = myUnion.centroid
            myZones = utmZoneFromLatLon(myCentroid.x, myCentroid.y)
        if len(myZones) > 0:
            # use the first match
            myZone = myZones[0]
            logging.debug('Utm zones: %s' % myZones)
            logging.debug('Before geom xform to %s: %s' % (myZone[0], myUnion))
            myTransform = CoordTransform(SpatialReference(4326),
                                         SpatialReference(myZone[0]))
            myUnion.transform(myTransform)
            logging.debug('After geom xform: %s' % myUnion)
            myCoverage['ProductArea'] = myUnion.area
            myCoverage['CentroidZone'] = (
                '%s (EPSG:%s)' % (myZone[1], myZone[0]))
        else:
            myCoverage['ProductArea'] = 'Error calculating area of products'
            myCoverage['CentroidZone'] = (
                'Error calculating centroid of products')
        if theOrder.delivery_detail.geometry:
            myClip = None
            if not myUnion:
                myClip = theOrder.delivery_detail.geometry
            else:
                myClip = myUnion.intersection(
                    theOrder.delivery_detail.geometry)
            myCoverage['IntersectedArea'] = myClip.area
            myCentroid = myClip.centroid
            # Calculate the zone independently as centroid may differ
            # from product union
            myZones = utmZoneFromLatLon(myCentroid.x, myCentroid.y)
            if len(myZones) > 0:
                myZone = myZones[0]
                if not myZone:
                    myCoverage['IntersectedArea'] = (
                        'Error calculating clip area')
                    myCoverage['ClipZone'] = 'Error calculating zone'
                    return myCoverage
                myTransform = CoordTransform(SpatialReference(4326),
                                             SpatialReference(myZone[0]))
                myClip.transform(myTransform)
                #logging.debug('Utm zones: %s' % myZone)
                myCoverage['IntersectedArea'] = myClip.area
                myCoverage['ClipZone'] = '%s (EPSG:%s)' % (
                    myZone[1], myZone[0])
        else:
            myCoverage['IntersectedArea'] = 'Not applicable'
            myCoverage['ClipZone'] = 'Not applicable'
    except Exception, e:
        logging.info('Error calculating coverage for order %s' % e.message)
        pass
    return myCoverage


@login_required
def updateOrderHistory(theRequest):
    if not theRequest.user.is_staff:
        return HttpResponse('''Access denied''')
    if not theRequest.method == 'POST':
        return HttpResponse('You can only access this view from a form POST')
    myTemplatePath = 'orderPage.html'
    if theRequest.is_ajax():
        # No page container needed, just a snippet
        myTemplatePath = 'orderStatusHistory.html'
        logging.debug('Request is ajax enabled')
    myOrderId = theRequest.POST['order']
    myOrder = get_object_or_404(Order, id=myOrderId)
    myNewStatusId = theRequest.POST['new_order_status']
    myNotes = theRequest.POST['notes']
    myNewStatus = get_object_or_404(OrderStatus, id=myNewStatusId)

    myOrderStatusHistory = OrderStatusHistory()
    myOrderStatusHistory.order = myOrder
    myOrderStatusHistory.old_order_status = myOrder.order_status
    myOrderStatusHistory.new_order_status = myNewStatus
    myOrderStatusHistory.user = theRequest.user
    myOrderStatusHistory.notes = myNotes
    try:
        myOrderStatusHistory.save()
    except:
        return HttpResponse('<html><head></head><body>Query error'
                            ' - please report to SAC staff</body></html>')
    myOrder.order_status = myNewStatus
    myOrder.save()
    myHistory = OrderStatusHistory.objects.all().filter(order=myOrder)
    # These next few lines and the long list of options below needed
    # for no ajax fallback
    myRecords = SearchRecord.objects.all().filter(order=myOrder)
    myForm = None

    myRequestContext = RequestContext(theRequest)
    if theRequest.user.is_staff:
        myForm = OrderStatusHistoryForm()
    if TaskingRequest.objects.filter(id=myOrderId):
        notifySalesStaffOfTaskRequest(
            myOrder.user, myOrderId, myRequestContext)
    else:
        notifySalesStaff(myOrder.user, myOrderId, myRequestContext)
    return render_to_response(myTemplatePath, {
        'myOrder': myOrder,
        'myRecords': myRecords,
        'myShowSensorFlag': True,
        'myShowSceneIdFlag': True,
        'myShowDateFlag': True,
        # cant remove stuff after order was placed
        'myRemoveFlag': False,
        'myThumbFlag': False,
        'myShowMetdataFlag': False,
        # used when you need to add an item to the cart only
        'myCartFlag': False,
        'myPreviewFlag': False,
        'myForm': myForm,
        'myHistory': myHistory,
        'myCartTitle': 'Product List',
    }, context_instance=myRequestContext)


@login_required
@renderWithContext('deliveryDetailForm.html')
def createDeliveryDetailForm(theRequest, theReferenceId):
    del theRequest
    myDeliveryDetailForm = ProductDeliveryDetailForm(
        initial={'ref_id': theReferenceId}, prefix='%i' % int(theReferenceId))
    return dict(myDeliveryDetailForm=myDeliveryDetailForm)


@login_required
@renderWithContext('deliveryDetail.html')
def showDeliveryDetail(theRequest, theReferenceId):
    del theRequest
    myDeliveryDetail = DeliveryDetail.objects.filter(
        pk__exact=theReferenceId).get()
    return dict(myDeliveryDetail=myDeliveryDetail)


@login_required
@requireProfile('addorder')
def addOrder(theRequest):
    logging.debug('Order called')
    myTitle = 'Create a new order'
    myRedirectPath = '/vieworder/'
    logging.info('Preparing order for user ' + str(theRequest.user))
    myRecords = None
    (myLayersList,
     myLayerDefinitions, myActiveBaseMap) = standardLayers(theRequest)
    myCartLayer = (
        'var myCartLayer = new OpenLayers.Layer.WMS("Cart", "http://'
        + settings.WMS_SERVER +
        '/cgi-bin/mapserv?map='
        + settings.CART_LAYER +
        '&user='
        + str(theRequest.user.username) + ''',
            {
               version: '1.1.1',
               layers: 'Cart',
               srs: 'EPSG:4326',
               format: 'image/png',
               transparent: 'true'
             },
             {isBaseLayer: false, singleTile:true});
             ''')

    # UGLY hack for adding Cart layer
    myLayersList = myLayersList[:-1] + ', myCartLayer ]'
    myLayerDefinitions.append(myCartLayer)

    if str(theRequest.user) == 'AnonymousUser':
        logging.debug('User is anonymous')
        logging.info('Anonymous users cannot have items in their cart')
        myMessage = ('If you want to order something, you need to'
                     ' create an account and log in first.')
        return HttpResponse(myMessage)
    else:
        logging.debug('User NOT anonymous')
        myRecords = SearchRecord.objects.all().filter(
            user=theRequest.user).filter(order__isnull=True)
        if myRecords.count() < 1:
            logging.debug('Cart has no records')
            logging.info('User has no items in their cart')
            return HttpResponseRedirect('/emptyCartHelp/')
        else:
            logging.debug('Cart has records')
            logging.info('Cart contains : ' +
                         str(myRecords.count()) + ' items')
    myExtraOptions = {
        # Possible flags for the record template
        # myShowSensorFlag
        # myShowIdFlag
        # myShowSceneIdFlag
        # myShowDateFlag
        # myShowCartFlag
        # myShowRemoveIconFlag
        # myShowPreviewFlag
        # myShowDeliveryDetailsFlag
        # myShowDeliveryDetailsFormFlag
        'myShowSensorFlag': False,
        'myShowSceneIdFlag': True,
        'myShowDateFlag': False,
        'myShowRemoveIconFlag': True,
        'myShowRowFlag': False,
        'myShowPathFlag': False,
        'myShowCloudCoverFlag': True,
        'myShowMetdataFlag': False,
        # used when you need to add an item to the cart only
        'myShowCartFlag': False,
        # used when you need to add an item to the cart only
        'myShowCartContentsFlag': True,
        'myShowPreviewFlag': False,
        'myShowDeliveryDetailsFlag': False,
        'myShowDeliveryDetailsFormFlag': True,
        'myCartTitle': 'Order Product List',
        'myRecords': myRecords,
        # propogated into the cart template
        'myBaseTemplate': 'emptytemplate.html',
        'mySubmitLabel': 'Submit Order',
        'myMessage': (' <div>Please specify any details for your order'
                      ' requirements below. If you need specific processing'
                      ' steps taken on individual images, please use the notes'
                      ' area below to provide detailed instructions. If you'
                      ' would like the product(s) to be clipped and masked'
                      ' to a specific geographic region, you can digitise'
                      ' that region using the map above, or the geometry'
                      ' input field below.</div>'),
        'myLayerDefinitions': myLayerDefinitions,
        'myLayersList': myLayersList,
        'myActiveBaseMap': myActiveBaseMap
    }
    logging.info('Add Order called')
    if theRequest.method == 'POST':
        logging.debug('Order posted')

        myOrderForm = OrderForm(theRequest.POST, theRequest.FILES)
        myDeliveryDetailForm = DeliveryDetailForm(
            myRecords, theRequest.POST, theRequest.FILES)

        # get ref_ids of product details forms, if any,
        # and generate forms for validation
        myProductForms = [
            ProductDeliveryDetailForm(
                theRequest.POST, prefix='%i' % int(myref)) for myref in
            myDeliveryDetailForm.data.get('ref_id').split(',')
            if len(myref) > 0]

        myOptions = {
            'myOrderForm': myOrderForm,
            'myDeliveryDetailForm': myDeliveryDetailForm,
            'myTitle': myTitle,
            'mySubmitLabel': 'Submit Order',
        }
        # shortcut to join two dicts
        myOptions.update(myExtraOptions)
        if (myOrderForm.is_valid() and myDeliveryDetailForm.is_valid()
                and all([form.is_valid() for form in myProductForms])):
            logging.debug('Order valid')

            myDeliveryDetailObject = myDeliveryDetailForm.save(commit=False)
            myDeliveryDetailObject.user = theRequest.user
            #check if user uploaded file and try to extract geometry
            try:
                myGeometry = getGeometryFromUploadedFile(
                    theRequest, myDeliveryDetailForm, 'geometry_file')
                if myGeometry:
                    myDeliveryDetailObject.geometry = myGeometry
                else:
                    logging.info('Failed to set search area'
                                 ' from uploaded geometry file')
            except:
                logging.info('An error occurred trying to set'
                             ' search area from uploaded geometry file')
            myDeliveryDetailObject.user = theRequest.user
            myDeliveryDetailObject.save()
            #save order
            myObject = myOrderForm.save(commit=False)
            myObject.user = theRequest.user
            myObject.delivery_detail = myDeliveryDetailObject
            myObject.save()
            logging.debug('Order saved')

            #save all of the subforms
            myDeliveryDetailsProducts = {}
            for mySubDeliveryForm in myProductForms:
                mySubData = mySubDeliveryForm.save(commit=False)
                mySubData.user = theRequest.user
                mySubData.save()
                # temporary store reference to deliverydetails
                # with search record ID as a key
                myDeliveryDetailsProducts[
                    int(mySubDeliveryForm.cleaned_data.get('ref_id'))
                ] = mySubData
            #update serachrecords
            for myRecord in myRecords:
                #check if this record has sepcific DeliveryDetails
                if myRecord.id in myDeliveryDetailsProducts:
                    myRecord.delivery_detail = myDeliveryDetailsProducts[
                        myRecord.id]
                myRecord.order = myObject
                myRecord.save()

            logging.info('Add Order : data is valid')

            logging.debug('Search records added')
            #return HttpResponse('Done')
            notifySalesStaff(theRequest.user, myObject.id)
            return HttpResponseRedirect(myRedirectPath + str(myObject.id))
        else:
            logging.info('Add Order: form is NOT valid')
            return render_to_response(
                'addPage.html', myOptions,
                context_instance=RequestContext(theRequest))
    else:  # new order
        myOrderForm = OrderForm()
        myDeliveryDetailForm = DeliveryDetailForm(myRecords)
        myOptions = {
            'myOrderForm': myOrderForm,
            'myDeliveryDetailForm': myDeliveryDetailForm,
            'myTitle': myTitle,
            'mySubmitLabel': 'Submit Order',
        }
        # shortcut to join two dicts
        myOptions.update(myExtraOptions),
        logging.info('Add Order: new object requested')
        return render_to_response(
            'addPage.html', myOptions,
            context_instance=RequestContext(theRequest))


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('cartContents.html')
def viewOrderItems(theRequest, theOrderId):
    """Just returns a table element - meant for use with ajax"""
    myOrder = get_object_or_404(Order, id=theOrderId)
    if not ((myOrder.user == theRequest.user) or (theRequest.user.is_staff)):
        raise Http404
    myRecords = SearchRecord.objects.all().filter(order=theOrderId)

    return ({
        'myRecords': myRecords,
        # Possible flags for the record template
        # myShowSensorFlag
        # myShowSceneIdFlag
        # myShowDateFlag
        # myShowCartFlag
        # myShowRemoveIconFlag
        # myShowPreviewFlag
        # myShowDeliveryDetailsFlag
        # myShowDeliveryDetailsFormFlag
        'myShowSensorFlag': False,
        'myShowSceneIdFlag': True,
        'myShowDateFlag': False,
        'myShowRemoveIconFlag': False,
        'myShowRowFlag': False,
        'myShowPathFlag': False,
        'myShowCloudCoverFlag': False,
        'myShowMetdataFlag': False,
        # used when you need to add an item to the cart only
        'myShowCartFlag': False,
        'myShowPreviewFlag': False,
        'myShowDeliveryDetailsFlag': True,
        'myShowDeliveryDetailsFormFlag': False,
        'myBaseTemplate': 'emptytemplate.html',
    })


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('ordersSummary.html')
def ordersSummary(theRequest):
    del theRequest
    #count orders by status
    myOrderStatus = OrderStatus.objects.annotate(num_orders=Count('order__id'))
    #count orders by product type (misson sensor)
    myOrderProductType = MissionSensor.objects.annotate(
        num_orders=Count('taskingrequest__order_ptr__id'))

    return dict(
        myOrderStatus=myOrderStatus,
        myOrderProductType=myOrderProductType)
