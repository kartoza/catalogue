from django.conf.urls import url

from .views import (
    list_orders,
    order_monthly_report,
    download_order,
    download_clip_geometry,
    download_order_metadata,
    view_order,
    update_order_history,
    add_order,
    orders_summary,
    order_summary_mail,
    add_adhoc_order,
    convert_price,
    my_orders
)
# Here are our patterns
urlpatterns = [
    url(r'^add-order/', add_order, name='add-order'),
    url(r'^download-clip-geometry/(?P<pk>\d*)/$',
        download_clip_geometry, name='download-clip-geometry'),
    url(r'^downloadordermetadata/(?P<pk>\d*)/$',
        download_order_metadata, name='downloadOrderMetadata'),
    url(r'^download-order/(?P<pk>\d*)/$',
        download_order, name='downloadOrder'),
    url(r'^myorders/$', my_orders, name='myOrders'),
    url(r'^list-orders/$', list_orders, name='list-orders'),
    url(r'^ordermonthlyreport/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        order_monthly_report, name='orderMonthlyReport'),
    url(r'^order/(?P<pk>[0-9]+)/$', view_order, name='order'),
    url(r'^updateorderhistory/$',
        update_order_history, name='updateOrderHistory'),
    url(r'^orders-summary/$', orders_summary, name='orders-summary'),
    url(r'^order-summary/$', order_summary_mail, name='order-Summary'),
    url(r'^add-ad-hoc-order/', add_adhoc_order, name='add-ad-hoc-order'),
    url(r'^convertprice/', convert_price, name='convertPrice'),
]
