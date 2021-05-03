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
import json
from decimal import Decimal
#other modules
from shapes.views import ShpResponder

from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect)
from django.core.paginator import (
    Paginator,
    EmptyPage,
    InvalidPage)
from django.urls import reverse
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

import json as simplejson
from exchange.models import Currency
from exchange.conversion import convert_value
# Models and forms for our app
from .models import (
    Order,
    OrderStatusHistory,
    OrderStatus,
    NonSearchRecord
)

from .forms import (
    OrderStatusHistoryForm,
    OrderForm,
    NonSearchRecordForm,
    OrderFormNonSearchRecords
)
# Helper classes
from catalogue.views.helpers import (
    notifySalesStaff,
    render_to_kml,
    render_to_kmz,
    downloadISOMetadata,
    downloadHtmlMetadata,)

# SHP and KML readers
from catalogue.utmzonecalc import utmZoneFromLatLon
from catalogue.profileRequiredDecorator import requireProfile
from catalogue.renderDecorator import renderWithContext

from search.models import SearchRecord
from dictionaries.models import Projection, ProcessingLevel
from django_tables2 import RequestConfig
from orders.tables import OrderListTable
# from dictionaries.models import InstrumentType, Satellite
###########################################################
#
# Ordering related views
#
###########################################################

logger = logging.getLogger(__name__)


@login_required
@renderWithContext('orderListPage.html', 'orderList.html')
def my_orders(request):
    """
    The view to return a requesting user's orders

    NOTE: This view should probably be replaced by list_orders below as the
        only difference between the two is the value of myUrl which can equally
        well be calculated from request.path

    :param request: HttpRequest obj
    """
    records = Order.base_objects.filter(
        user=request.user).order_by('-order_date')
    if 'pdf' in request.GET:
        # Django's pagination is only required for the PDF view as
        # django-tables2 handles pagination for the table
        table = None
        page_size = records.count()
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        paginator = Paginator(records, page_size)
        try:
            records = paginator.page(page)
        except (EmptyPage, InvalidPage):
            records = paginator.page(paginator.num_pages)
    else:
        table = OrderListTable(records)
        RequestConfig(request, paginate={
            'per_page': settings.PAGE_SIZE
        }).configure(table)
    return ({
        'myUrl': reverse('myOrders'),
        'myCurrentMonth': datetime.date.today(),
        'table': table,
        'myRecords': records
    })


@login_required
@renderWithContext('orderListPage.html', 'orderList.html')
def list_orders(request):
    """
    The view to return a list of Orders. Records returned depends on whether
    the requesting User is_staff.

    :param request: HttpRequest dict
    :return: orderListPage and orderList :rtype: HttpResponse
    """
    order_id = request.GET.get('order_id')
    if not request.user.is_staff:
        '''Non staff users can only see their own orders listed'''
        if order_id:
            records = Order.base_objects.filter(
                user=request.user, id=order_id).order_by('-order_date')
        else:
            records = Order.base_objects.filter(
                user=request.user).order_by('-order_date')
    else:
        '''This view is strictly for staff only'''
        # This view uses the NoSubclassManager
        # base_objects is defined in the model and
        # will exclude all tasking requests or other
        # derived classes
        if order_id:
            records = Order.base_objects.filter(id=order_id).order_by(
                '-order_date')
        else:
            records = Order.base_objects.all().order_by('-order_date')
    if 'pdf' in request.GET:
        # Django's pagination is only required for the PDF view as
        # django-tables2 handles pagination for the table
        table = None
        page_size = records.count()
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        paginator = Paginator(records, page_size)
        try:
            records = paginator.page(page)
        except (EmptyPage, InvalidPage):
            records = paginator.page(paginator.num_pages)
    else:
        table = OrderListTable(records)
        RequestConfig(request, paginate={
            'per_page': settings.PAGE_SIZE
        }).configure(table)
    return ({
        'myUrl': reverse('listOrders'),
        'myCurrentMonth': datetime.date.today(),
        'table': table,
        'myRecords': records
    })


@login_required
@renderWithContext('orderMonthlyReport.html')
def order_monthly_report(request, year, month):
    """
    The view to render a monthly Order report. reports depends on whether the
    requesting User is_staff

    :param request: HttpRequest dict
    :param year: Optional year int
    :param month: Optional month int
    :return: orderMonthlyReport.html :rtype: HttpResponse
    """
    if not(year and month):
        date = datetime.date.today()
    else:
        try:
            date = datetime.date(int(year), int(month), 1)
        except:
            date = None
            logger.error('Date arguments cannot be parsed')
            logger.info(traceback.format_exc())
    if not request.user.is_staff:
        '''Non staff users can only see their own orders listed'''
        records = (Order.base_objects.filter(
            user=request.user)
            .filter(
                order_date__month=date.month)
            .filter(
                order_date__year=date.year)
            .order_by('order_date'))
    else:
        '''This view is strictly for staff only'''
        records = (
            Order.base_objects.filter(
                order_date__month=date.month)
            .filter(
                order_date__year=date.year)
            .order_by('order_date'))
    if 'pdf' in request.GET:
        # Django's pagination is only required for the PDF view as
        # django-tables2 handles pagination for the table
        table = None
        page_size = records.count()
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        paginator = Paginator(records, page_size)
        try:
            records = paginator.page(page)
        except (EmptyPage, InvalidPage):
            records = paginator.page(paginator.num_pages)
    else:
        table = OrderListTable(records)
        RequestConfig(request, paginate={
            'per_page': settings.PAGE_SIZE
        }).configure(table)
    return ({
        'myRecords': records,
        'myCurrentDate': date,
        'myPrevDate': date - datetime.timedelta(days=1),
        'myNextDate': date + datetime.timedelta(days=31),
        'table': table
    })


@login_required
def downloadOrder(theRequest, theId):
    """Dispaches request and returns geometry of ordered products in
       desired file format"""
    myOrder = get_object_or_404(Order, id=theId)

    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(myOrder)
        myResponder.file_name = 'products_for_order_%s' % myOrder.id
        return myResponder.write_order_products(
            myOrder.searchrecord_set.all())
    elif 'kml' in theRequest.GET:
        return render_to_kml('kml/searchRecords.kml', {
            'mySearchRecords': myOrder.searchrecord_set.all(),
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True
        }, 'products_for_order_%s' % myOrder.id)
    elif 'kmz' in theRequest.GET:
        return render_to_kmz('kml/searchRecords.kml', {
            'mySearchRecords': myOrder.searchrecord_set.all(),
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True,
            'myThumbsFlag': True
        }, 'products_for_order_%s' % myOrder.id)
    else:
        logger.info(
            'Request cannot be proccesed, unsupported download file type')
        raise Http404


@staff_member_required
def downloadClipGeometry(theRequest, theId):
    """Dispaches request and returns clip geometry
       for order in desired file format"""
    myOrder = get_object_or_404(Order, id=theId)

    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(myOrder)
        myResponder.file_name = 'clip_geometry_order_%s' % myOrder.id
        return myResponder.write_delivery_details(myOrder)
    elif 'kml' in theRequest.GET:
        return render_to_kml(
            'kml/clipGeometry.kml', {
                'order': myOrder,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True
            }, 'clip_geometry_order_%s' % myOrder.id)
    elif 'kmz' in theRequest.GET:
        return render_to_kmz(
            'kml/clipGeometry.kml', {
                'order': myOrder,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True,
                'myThumbsFlag': True
            }, 'clip_geometry_order_%s' % myOrder.id)
    else:
        logger.info(
            'Request cannot be processed, unsupported download file type')
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

    myOrder = get_object_or_404(Order, id=theId)
    if not ((myOrder.user == theRequest.user) or (theRequest.user.is_staff)):
        raise Http404
    myRecords = SearchRecord.objects.all().filter(order=myOrder)
    if (myRecords.count() > 0):
        myHistory = OrderStatusHistory.objects.all().filter(order=myOrder)
        myStatusForm = OrderStatusHistoryForm()
        if (theRequest.method == 'POST'):
            myOrderForm = OrderForm(theRequest.POST, theRequest.FILES, instance=myOrder)
            myOptions = {
                    'myOrder': myOrder,
                    'myOrderForm': myOrderForm,
                    'myRecords': myRecords,
                    'myHistory': myHistory,
                    'myStatusForm': myStatusForm
                }
            if myOrderForm.is_valid():
                myObject = myOrderForm.save()
                for myRecord in myRecords:
                    proj = Projection.objects.get(epsg_code=theRequest.POST.get(str(myRecord.product.id) + '_projection'))
                    myRecord.projection = proj
                    proc = ProcessingLevel.objects.get(pk=theRequest.POST.get(str(myRecord.product.id) + '_processing'))
                    myRecord.processing_level = proc
                    myRecord.save()

                return HttpResponseRedirect(
                    reverse('viewOrder', kwargs={'theId': myObject.id}))
            else:
                return render_to_response(
                    'orderPage.html',
                    myOptions,
                    RequestContext(theRequest)
                )
        else:
            if (theRequest.user.is_staff):
                myOrderForm = OrderForm(instance=myOrder)
                myOptions = {
                    'myOrder': myOrder,
                    'myOrderForm': myOrderForm,
                    'myRecords': myRecords,
                    'myHistory': myHistory,
                    'myStatusForm': myStatusForm
                }
                return render_to_response(
                    'orderPage.html',
                    myOptions,
                    RequestContext(theRequest)
                )
            else:
                myOptions = {
                    'myOrder': myOrder,
                    'myRecords': myRecords,
                    'myHistory': myHistory
                }
                return render_to_response(
                    'orderPageUser.html',
                    myOptions,
                    RequestContext(theRequest)
                )
    else:
        myRecords = NonSearchRecord.objects.all().filter(order=myOrder)
        myStatusForm = OrderStatusHistoryForm()
        myHistory = OrderStatusHistory.objects.all().filter(order=myOrder)
        myStatusForm = OrderStatusHistoryForm()
        listCurrency = Currency.objects.all().values_list('code', 'name')
        myCurrency = json.dumps([list(currency) for currency in listCurrency])
        if (theRequest.method == 'POST'):
            myOrderForm = OrderFormNonSearchRecords(theRequest.POST, theRequest.FILES, instance=myOrder)
            myOptions = {
                    'myOrder': myOrder,
                    'myOrderForm': myOrderForm,
                    'myRecords': myRecords,
                    'myHistory': myHistory,
                    'myStatusForm': myStatusForm,
                    'myCurrency': myCurrency
                }
            if myOrderForm.is_valid():
                myObject = myOrderForm.save()
                NonSearchRecord.objects.all().filter(order=myOrder).delete()
                products = theRequest.POST.getlist('productlist')

                for product in products:
                    nonSearchRecord = NonSearchRecord();
                    nonSearchRecord.user = theRequest.user
                    nonSearchRecord.order = myObject
                    nonSearchRecord.product_description = theRequest.POST.get(str(product) + '_product')
                    nonSearchRecord.cost_per_scene = Decimal(theRequest.POST.get(str(product) + '_price'))
                    nonSearchRecord.rand_cost_per_scene = Decimal(theRequest.POST.get(str(product) + '_rand_price'))
                    prod_currency = theRequest.POST.get(str(product) + '_currency')
                    nonSearchRecord.currency = Currency.objects.get(code=prod_currency)
                    nonSearchRecord.save()
                return HttpResponseRedirect(
                    reverse('viewOrder', kwargs={'theId': myObject.id}))
            else:
                return render_to_response(
                    'orderAdHocForm.html',
                    myOptions,
                    RequestContext(theRequest)
                )
        else:
            if (theRequest.user.is_staff):
                myOrderForm = OrderFormNonSearchRecords(instance=myOrder)
                myOptions = {
                    'myOrder': myOrder,
                    'myOrderForm': myOrderForm,
                    'myRecords': myRecords,
                    'myHistory': myHistory,
                    'myStatusForm': myStatusForm,
                    'myCurrency': myCurrency
                }
                return render_to_response(
                    'orderAdHocPage.html',
                    myOptions,
                    RequestContext(theRequest)
                )
            else:
                mySum = 0
                for record in myRecords:
                    mySum = mySum + record.rand_cost_per_scene
                myOptions = {
                    'myOrder': myOrder,
                    'myRecords': myRecords,
                    'myHistory': myHistory,
                    'mySum': mySum
                }
                return render_to_response(
                    'orderAdHocPageUser.html',
                    myOptions,
                    RequestContext(theRequest)
                )


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
            logger.debug('Utm zones: %s' % myZones)
            logger.debug('Before geom xform to %s: %s' % (myZone[0], myUnion))
            myTransform = CoordTransform(SpatialReference(4326),
                                         SpatialReference(myZone[0]))
            myUnion.transform(myTransform)
            logger.debug('After geom xform: %s' % myUnion)
            myCoverage['ProductArea'] = int(myUnion.area)
            myCoverage['CentroidZone'] = (
                '%s (EPSG:%s)' % (myZone[1], myZone[0]))
        else:
            myCoverage['ProductArea'] = 'Error calculating area of products'
            myCoverage['CentroidZone'] = (
                'Error calculating centroid of products')
    except Exception as e:
        logger.info('Error calculating coverage for order %s' % e.message)
        pass
    return myCoverage


@login_required
def updateOrderHistory(theRequest):
    if not theRequest.user.is_staff:
        return HttpResponse('''Access denied''')
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
        resp = simplejson.dumps({"saved": 'failed'})
        return HttpResponse(resp, content_type="application/json")
    myOrder.order_status = myNewStatus
    myOrder.save()
    notifySalesStaff(myOrder.user, myOrderId)
    resp = simplejson.dumps({"saved": 'ok'})
    return HttpResponse(resp, content_type="application/json")



@login_required
@requireProfile('addorder')
def addOrder(theRequest):
    logger.debug('Order called')
    logger.info('Preparing order for user ' + str(theRequest.user))
    myRecords = None

    if str(theRequest.user) == 'AnonymousUser':
        logger.debug('User is anonymous')
        logger.info('Anonymous users cannot have items in their cart')
        myMessage = ('If you want to order something, you need to'
                     ' create an account and log in first.')
        return HttpResponse(myMessage)
    else:
        logger.debug('User NOT anonymous')
        myRecords = SearchRecord.objects.all().filter(
            user=theRequest.user).filter(order__isnull=True)
        if myRecords.count() < 1:
            logger.debug('Cart has no records')
            logger.info('User has no items in their cart')
            return HttpResponseRedirect(reverse('emptyCartHelp'))
        else:
            logger.debug('Cart has records')
            logger.info('Cart contains : %i items', myRecords.count())
    myExtraOptions = {
        'myRecords': myRecords,
    }
    logger.info('Add Order called')
    if theRequest.method == 'POST':
        logger.debug('Order posted')

        myOrderForm = OrderForm(theRequest.POST, theRequest.FILES)

        myOptions = {
            'myOrderForm': myOrderForm,
        }
        # shortcut to join two dicts
        myOptions.update(myExtraOptions)
        if myOrderForm.is_valid():
            logger.debug('Order valid')

            myObject = myOrderForm.save()
            logger.debug('Order saved')

            #update serachrecords

            for myRecord in myRecords:
                myRecord.order = myObject
                proj = Projection.objects.get(epsg_code=theRequest.POST.get(str(myRecord.product.id) + '_projection'))
                myRecord.projection = proj
                proc = ProcessingLevel.objects.get(pk=theRequest.POST.get(str(myRecord.product.id) + '_processing'))
                myRecord.processing_level = proc
                myRecord.save()

            notifySalesStaff(theRequest.user, myObject.id)
            return HttpResponseRedirect(
                reverse('viewOrder', kwargs={'theId': myObject.id}))
        else:
            logger.info('Add Order: form is NOT valid')
            return render_to_response(
                'orderForm.html',
                myOptions,
                RequestContext(theRequest)
            )
    else:  # new order
        myOrderForm = OrderForm(
            initial={
                'market_sector': None,
                'user': theRequest.user.id,
                'file_format': 1,
                'delivery_method': 2
            }
        )
        myOptions = {
            'myOrderForm': myOrderForm,
        }
        # shortcut to join two dicts
        myOptions.update(myExtraOptions),
        logger.info('Add Order: new object requested')
        return render_to_response(
            'orderForm.html',
            myOptions,
            RequestContext(theRequest)
        )


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('ordersSummary.html')
def ordersSummary(theRequest):
    del theRequest
    #count orders by status
    myOrderStatus = OrderStatus.objects.annotate(num_orders=Count('order__id'))
    # count orders by product type (mission sensor)
    # TODO - refactoring
    myOrderInstrumentType = None
    myOrderSatellite = None
    return dict(
        myOrderStatus=myOrderStatus,
        myOrderInstrumentType=myOrderInstrumentType,
        myOrderSatellite=myOrderSatellite)

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('order-summary.html')
def orderSummaryMail(theRequest):
    myOrder = get_object_or_404(Order, id=643)
    myRecords = SearchRecord.objects.filter(order=myOrder).select_related()
    myHistory = OrderStatusHistory.objects.filter(order=myOrder)
    return ({
        'myOrder': myOrder,
        'myRecords': myRecords,
        'myHistory': myHistory,
        'domain': settings.DOMAIN
    })

@staff_member_required
def addAdhocOrder(theRequest):
    logger.debug('Adhoc order called')
    logger.info('by user ' + str(theRequest.user))
    if theRequest.method == 'POST':
        myOrderForm = OrderFormNonSearchRecords(theRequest.POST, theRequest.FILES)
        myOptions = {
            'myOrderForm': myOrderForm,
        }

        if myOrderForm.is_valid():
            myObject = myOrderForm.save()
            products = theRequest.POST.getlist('productlist')

            for product in products:
                nonSearchRecord = NonSearchRecord();
                nonSearchRecord.user = theRequest.user
                nonSearchRecord.order = myObject
                nonSearchRecord.product_description = theRequest.POST.get(str(product) + '_product')
                prod_cost = Decimal(theRequest.POST.get(str(product) + '_price'))
                prod_currency = theRequest.POST.get(str(product) + '_currency')
                nonSearchRecord.cost_per_scene = prod_cost
                nonSearchRecord.rand_cost_per_scene = convert_value(prod_cost, prod_currency, 'ZAR')
                nonSearchRecord.currency = Currency.objects.get(code=prod_currency)
                nonSearchRecord.save()
            notifySalesStaff(theRequest.user, myObject.id)
            return HttpResponseRedirect(
                reverse('viewOrder', kwargs={'theId': myObject.id}))
        else:
            return render_to_response(
                'orderAdHocForm.html',
                myOptions,
                RequestContext(theRequest)
            )
    else:
        myOrderForm = OrderFormNonSearchRecords()
        listCurrency = Currency.objects.all().values_list('code', 'name')
        myCurrency = json.dumps([list(currency) for currency in listCurrency])
        myOptions = {
            'myOrderForm': myOrderForm,
            'myCurrency': myCurrency
        }
        # shortcut to join two dicts
        logger.info('Add Order: new object requested')
        return render_to_response(
            'orderAdHocForm.html',
            myOptions,
            RequestContext(theRequest)
        )


def convertPrice(theRequest):
    currency = theRequest.POST.get('currency')
    price = Decimal(theRequest.POST.get('price'))
    rand_price = "%0.2f" % (convert_value(price, currency, 'ZAR'),)
    resp = simplejson.dumps({"rand_price": rand_price})
    return HttpResponse(resp, content_type="application/json")


@login_required
def viewOrderStatusEmail(theRequest, theId):

    myOrder = get_object_or_404(Order, id=theId)
    if not ((myOrder.user == theRequest.user) or (theRequest.user.is_staff)):
        raise Http404
    myRecords = SearchRecord.objects.all().filter(order=myOrder)
    if (myRecords.count() == 0):
        myRecords = NonSearchRecord.objects.all().filter(order=myOrder)

    myHistory = OrderStatusHistory.objects.all().filter(order=myOrder)
    myOptions = {
        'myOrder': myOrder,
        'myRecords': myRecords,
        'myHistory': myHistory
    }
