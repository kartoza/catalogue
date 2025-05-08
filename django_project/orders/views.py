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
# other modules
from shapes.views import ShpResponder

from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect)
from django.core.paginator import (
    Paginator,
    EmptyPage,
    InvalidPage
)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings
# for aggregate queries
from django.db.models import Count

from django.contrib.gis.gdal import (
    SpatialReference,
    CoordTransform
)

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

from orders.forms import (
    OrderStatusHistoryForm,
    OrderForm,
    OrderFormNonSearchRecords
)
# Helper classes
from catalogue.views.helpers import (
    notify_sales_staff,
    render_to_kml,
    render_to_kmz,
    downloadISOMetadata,
    downloadHtmlMetadata
)

# SHP and KML readers
from catalogue.utmzonecalc import utmZoneFromLatLon
from catalogue.profile_required_decorator import require_profile
from catalogue.render_decorator import RenderWithContext

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
@RenderWithContext('order-list-page.html', 'order-list.html')
def my_orders(request):
    """
    The view to return a requesting user's orders

    NOTE: This view should probably be replaced by list_orders below as the
        only difference between the two is the value of myUrl which can equally
        well be calculated from request.path

    :param request: HttpRequest obj
    """
    records = Order.objects.filter(
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
        paginator = Paginator(records, 1)
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
        'header': True,
        'myUrl': reverse('orders'),
        'myCurrentMonth': datetime.date.today(),
        'table': table,
        'myRecords': records
    })


@login_required
@RenderWithContext('order-list-page.html', 'order-list.html')
def list_orders(request):
    """
    The view to return a list of Orders. Records returned depends on whether
    the requesting User is_staff.

    :param request: HttpRequest dict
    :return: order-list-page and order-list :rtype: HttpResponse
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
        'myUrl': reverse('list-orders'),
        'myCurrentMonth': datetime.date.today(),
        'table': table,
        'myRecords': records
    })


@login_required
@RenderWithContext('order-monthly-report.html')
def order_monthly_report(request, year, month):
    """
    The view to render a monthly Order report. reports depends on whether the
    requesting User is_staff

    :param request: HttpRequest dict
    :param year: Optional year int
    :param month: Optional month int
    :return: orderMonthlyReport.html :rtype: HttpResponse
    """
    if not (year and month):
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
def download_order(request, pk):
    """Dispaches request and returns geometry of ordered products in
       desired file format"""
    my_order = get_object_or_404(Order, id=pk)

    if 'shp' in request.GET:
        responder = ShpResponder(my_order)
        responder.file_name = 'products_for_order_%s' % my_order.id
        return responder.write_order_products(
            my_order.searchrecord_set.all())
    elif 'kml' in request.GET:
        return render_to_kml('kml/searchRecords.kml', {
            'mySearchRecords': my_order.searchrecord_set.all(),
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True
        }, 'products_for_order_%s' % my_order.id)
    elif 'kmz' in request.GET:
        return render_to_kmz('kml/searchRecords.kml', {
            'mySearchRecords': my_order.searchrecord_set.all(),
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True,
            'myThumbsFlag': True
        }, 'products_for_order_%s' % my_order.id)
    else:
        logger.info(
            'Request cannot be proccesed, unsupported download file type')
        raise Http404


@staff_member_required
def download_clip_geometry(request, pk):
    """Dispaches request and returns clip geometry
       for order in desired file format"""
    my_order = get_object_or_404(Order, id=pk)

    if 'shp' in request.GET:
        responder = ShpResponder(my_order)
        responder.file_name = 'clip_geometry_order_%s' % my_order.id
        return responder.write_delivery_details(my_order)
    elif 'kml' in request.GET:
        return render_to_kml(
            'kml/clip_geometry.kml', {
                'order': my_order,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True
            }, 'clip_geometry_order_%s' % my_order.id)
    elif 'kmz' in request.GET:
        return render_to_kmz(
            'kml/clip_geometry.kml', {
                'order': my_order,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True,
                'myThumbsFlag': True
            }, 'clip_geometry_order_%s' % my_order.id)
    else:
        logger.info(
            'Request cannot be processed, unsupported download file type')
        raise Http404


@login_required
def download_order_metadata(request, pk):
    """Returns ISO 19115 metadata for ordered products
      unless the request is suffixed by ?html"""
    my_order = get_object_or_404(Order, id=pk)
    if 'html' in request.GET:
        return downloadHtmlMetadata(
            my_order.searchrecord_set.all(), 'Order-%s' % my_order.id)
    else:
        return downloadISOMetadata(
            my_order.searchrecord_set.all(), 'Order-%s' % my_order.id)


@login_required
def view_order(request, pk):
    my_order = get_object_or_404(Order, id=pk)
    if not ((my_order.user == request.user) or request.user.is_staff):
        raise Http404
    my_records = SearchRecord.objects.all().filter(order=my_order)
    if my_records.count() > 0:
        my_history = OrderStatusHistory.objects.all().filter(order=my_order)
        my_status_form = OrderStatusHistoryForm()
        if request.method == 'POST':
            my_order_form = OrderForm(request.POST, request.FILES, instance=my_order)
            context = {
                'myOrder': my_order,
                'myOrderForm': my_order_form,
                'myRecords': my_records,
                'myHistory': my_history,
                'myStatusForm': my_status_form
            }
            if my_order_form.is_valid():
                order = my_order_form.save()
                for record in my_records:
                    proj = Projection.objects.get(epsg_code=request.POST.get(str(record.product.id) + '_projection'))
                    record.projection = proj
                    proc = ProcessingLevel.objects.get(pk=request.POST.get(str(record.product.id) + '_processing'))
                    record.processing_level = proc
                    record.save()

                return HttpResponseRedirect(
                    reverse('order', kwargs={'pk': order.id}))
            else:
                return render(
                    request,
                    'order_page.html',
                    context
                )
        else:
            if request.user.is_staff:
                my_order_form = OrderForm(instance=my_order)
                context = {
                    'myOrder': my_order,
                    'myOrderForm': my_order_form,
                    'myRecords': my_records,
                    'myHistory': my_history,
                    'myStatusForm': my_status_form
                }
                return render(
                    request,
                    'order_page.html',
                    context
                )
            else:
                context = {
                    'myOrder': my_order,
                    'myRecords': my_records,
                    'myHistory': my_history
                }
                return render(
                    request,
                    'order_page_user.html',
                    context,
                )
    else:
        my_records = NonSearchRecord.objects.all().filter(order=my_order)
        my_history = OrderStatusHistory.objects.all().filter(order=my_order)
        my_status_form = OrderStatusHistoryForm()
        list_currency = Currency.objects.all().values_list('code', 'name')
        my_currency = json.dumps([list(currency) for currency in list_currency])
        if request.method == 'POST':
            my_order_form = OrderFormNonSearchRecords(request.POST, request.FILES, instance=my_order)
            context = {
                'myOrder': my_order,
                'myOrderForm': my_order_form,
                'myRecords': my_records,
                'myHistory': my_history,
                'myStatusForm': my_status_form,
                'myCurrency': my_currency
            }
            if my_order_form.is_valid():
                order = my_order_form.save()
                NonSearchRecord.objects.all().filter(order=my_order).delete()
                products = request.POST.getlist('productlist')

                for product in products:
                    non_search_record = NonSearchRecord()
                    non_search_record.user = request.user
                    non_search_record.order = order
                    non_search_record.product_description = request.POST.get(str(product) + '_product')
                    non_search_record.cost_per_scene = Decimal(request.POST.get(str(product) + '_price'))
                    non_search_record.rand_cost_per_scene = Decimal(request.POST.get(str(product) + '_rand_price'))
                    prod_currency = request.POST.get(str(product) + '_currency')
                    non_search_record.currency = Currency.objects.get(code=prod_currency)
                    non_search_record.save()
                return HttpResponseRedirect(
                    reverse('order', kwargs={'pk': order.id}))
            else:
                return render(
                    request,
                    'order_adhoc_form.html',
                    context
                )
        else:
            if request.user.is_staff:
                my_order_form = OrderFormNonSearchRecords(instance=my_order)
                context = {
                    'myOrder': my_order,
                    'myOrderForm': my_order_form,
                    'myRecords': my_records,
                    'myHistory': my_history,
                    'myStatusForm': my_status_form,
                    'myCurrency': my_currency
                }
                return render(
                    request,
                    'orderAdHocPage.html',
                    context
                )
            else:
                my_sum = 0
                for record in my_records:
                    my_sum = my_sum + record.rand_cost_per_scene
                context = {
                    'myOrder': my_order,
                    'myRecords': my_records,
                    'myHistory': my_history,
                    'mySum': my_sum
                }
                return render(
                    request,
                    'orderAdHocPageUser.html',
                    context
                )


def coverage_for_order(order, search_records):
    """A small helper function to compute the coverage area. Logic is:
       - if AOI specified, the union of the products is clipped by the AOI
       - if no AOI is specified the area of the union of the products is
         returned.
       returns a dict with keys containing area properties for the order:
        ProductArea - total area of the union of all ordered products
        CentroidZone - UTM zone at cenroid of union of all ordered products
        IntersectedArea - area of union of all products intersected with AOI
       """
    coverage = {}
    union = None
    centroid = None
    zones = []
    try:
        for record in search_records:
            geometry = record.product.spatial_coverage
            if not union:
                union = geometry
            else:
                # This can be done faster using cascaded union
                # but needs geos 3.1
                union = union.union(geometry)
        if union:
            centroid = union.centroid
            zones = utmZoneFromLatLon(centroid.x, centroid.y)
        if len(zones) > 0:
            # use the first match
            zone = zones[0]
            logger.debug('Utm zones: %s' % zones)
            logger.debug('Before geom xform to %s: %s' % (zone[0], union))
            transform = CoordTransform(SpatialReference(4326),
                                       SpatialReference(zone[0]))
            union.transform(transform)
            logger.debug('After geom xform: %s' % union)
            coverage['ProductArea'] = int(union.area)
            coverage['CentroidZone'] = (
                    '%s (EPSG:%s)' % (zone[1], zone[0]))
        else:
            coverage['ProductArea'] = 'Error calculating area of products'
            coverage['CentroidZone'] = (
                'Error calculating centroid of products')
    except Exception as e:
        logger.info('Error calculating coverage for order %s' % e.message)
        pass
    return coverage


@login_required
def update_order_history(request):
    if not request.user.is_staff:
        return HttpResponse('''Access denied''')
    my_order_id = request.POST['order']
    my_order = get_object_or_404(Order, id=my_order_id)
    my_new_status_d = request.POST['new_order_status']
    my_notes = request.POST['notes']
    my_new_status = get_object_or_404(OrderStatus, id=my_new_status_d)

    my_order_status_history = OrderStatusHistory()
    my_order_status_history.order = my_order
    my_order_status_history.old_order_status = my_order.order_status
    my_order_status_history.new_order_status = my_new_status
    my_order_status_history.user = request.user
    my_order_status_history.notes = my_notes
    try:
        my_order_status_history.save()
    except:
        resp = simplejson.dumps({"saved": 'failed'})
        return HttpResponse(resp, content_type="application/json")
    my_order.order_status = my_new_status
    my_order.save()
    notify_sales_staff(my_order.user, my_order_id)
    resp = simplejson.dumps({"saved": 'ok'})
    return HttpResponse(resp, content_type="application/json")


@login_required
# @require_profile('add_order')
def add_order(request):
    print("USER",request.user)
    logger.debug('Order called')
    logger.info('Preparing order for user ' + str(request.user))

    if str(request.user) == 'AnonymousUser':
        logger.debug('User is anonymous')
        logger.info('Anonymous users cannot have items in their cart')
        message = ('If you want to order something, you need to'
                   'create an account and log in first.')
        return HttpResponse(message)
    else:
        logger.debug('User NOT anonymous')
        my_records = SearchRecord.objects.all().filter(
            user=request.user).filter(order__isnull=True)
        print("MY RECORDS", my_records)
        if my_records.count() < 1:
            logger.debug('Cart has no records')
            logger.info('User has no items in their cart')
            return HttpResponseRedirect(reverse('emptyCartHelp'))
        else:
            logger.debug('Cart has records')
            logger.info('Cart contains : %i items', my_records.count())
    extra_options = {
        'myRecords': my_records,
    }
    logger.info('Add Order called')
    if request.method == 'POST':
        logger.debug('Order posted')

        my_order_form = OrderForm(request.POST, request.FILES)

        print("FORM VALID?", my_order_form.is_valid())
        print("FORM ERRORS:", my_order_form.errors)

        context = {
            'myOrderForm': my_order_form,
        }
        # shortcut to join two dicts
        context.update(extra_options)
        if my_order_form.is_valid():
            logger.debug('Order valid')

            order = my_order_form.save()
            logger.debug('Order saved')

            # update serachrecords

            for myRecord in my_records:
                myRecord.order = order
                proj = Projection.objects.get(epsg_code=request.POST.get(str(myRecord.product.id) + '_projection'))
                myRecord.projection = proj
                proc = ProcessingLevel.objects.get(pk=request.POST.get(str(myRecord.product.id) + '_processing'))
                myRecord.processing_level = proc
                myRecord.save()

            notify_sales_staff(request.user, order.id)
            return HttpResponseRedirect(
                reverse('order', kwargs={'pk': order.id}))
        else:
            logger.info('Add Order: form is NOT valid')
            return render(
                request,
                'order_form.html',
                context
            )
    else:  # new order
        print("USER ID", request.user.id)
        my_order_form = OrderForm(
            initial={
                'market_sector': None,
                'user': request.user.id,
                'file_format': 1,
                'delivery_method': 2
            }
        )
        context = {
            'myOrderForm': my_order_form,
        }
        # shortcut to join two dicts
        context.update(extra_options),
        logger.info('Add Order: new object requested')
        return render(
            request,
            'order_form.html',
            context
        )


@login_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('orders_summary.html')
def orders_summary(request):
    del request
    # count orders by status
    my_order_status = OrderStatus.objects.annotate(num_orders=Count('order__id'))
    # count orders by product type (mission sensor)
    # TODO - refactoring
    my_order_instrument_type = None
    my_order_satellite = None
    return dict(
        my_orderStatus=my_order_status,
        my_orderInstrumentType=my_order_instrument_type,
        my_orderSatellite=my_order_satellite)


@login_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('order_summary.html')
def order_summary_mail(request):
    my_order = get_object_or_404(Order, id=643)
    my_records = SearchRecord.objects.filter(order=my_order).select_related()
    my_history = OrderStatusHistory.objects.filter(order=my_order)
    return ({
        'myOrder': my_order,
        'myRecords': my_records,
        'myHistory': my_history,
        'domain': settings.DOMAIN
    })


@staff_member_required
def add_adhoc_order(request):
    logger.debug('Adhoc order called')
    logger.info('by user ' + str(request.user))
    if request.method == 'POST':
        my_order_form = OrderFormNonSearchRecords(request.POST, request.FILES)
        context = {
            'myOrderForm': my_order_form,
        }

        if my_order_form.is_valid():
            order = my_order_form.save()
            products = request.POST.getlist('productlist')

            for product in products:
                non_search_record = NonSearchRecord();
                non_search_record.user = request.user
                non_search_record.order = order
                non_search_record.product_description = request.POST.get(str(product) + '_product')
                prod_cost = Decimal(request.POST.get(str(product) + '_price'))
                prod_currency = request.POST.get(str(product) + '_currency')
                non_search_record.cost_per_scene = prod_cost
                non_search_record.rand_cost_per_scene = convert_value(prod_cost, prod_currency, 'ZAR')
                non_search_record.currency = Currency.objects.get(code=prod_currency)
                non_search_record.save()
            notify_sales_staff(request.user, order.id)
            return HttpResponseRedirect(
                reverse('order', kwargs={'pk': order.id}))
        else:
            return render(
                request,
                'order_adhoc_form.html',
                context
            )
    else:
        my_order_form = OrderFormNonSearchRecords()
        list_currency = Currency.objects.all().values_list('code', 'name')
        my_currency = json.dumps([list(currency) for currency in list_currency])
        context = {
            'myOrderForm': my_order_form,
            'myCurrency': my_currency
        }
        # shortcut to join two dicts
        logger.info('Add Order: new object requested')
        return render(
            request,
            'order_adhoc_form.html',
            context
        )


def convert_price(request):
    currency = request.POST.get('currency')
    price = Decimal(request.POST.get('price'))
    rand_price = "%0.2f" % (convert_value(price, currency, 'ZAR'),)
    resp = simplejson.dumps({"rand_price": rand_price})
    return HttpResponse(resp, content_type="application/json")


@login_required
def view_order_status_email(request, pk):
    order = get_object_or_404(Order, id=pk)
    if not ((order.user == request.user) or request.user.is_staff):
        raise Http404
    my_records = SearchRecord.objects.all().filter(order=order)
    if my_records.count() == 0:
        my_records = NonSearchRecord.objects.all().filter(order=order)

    my_history = OrderStatusHistory.objects.all().filter(order=order)
    context = {
        'myOrder': order,
        'myRecords': my_records,
        'myHistory': my_history
    }
