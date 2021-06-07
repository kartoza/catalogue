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
    url(r'^addorder/', add_order, name='addOrder'),
    url(r'^downloadclipgeometry/(?P<pk>\d*)/$',
        download_clip_geometry, name='downloadClipGeometry'),
    url(r'^downloadordermetadata/(?P<pk>\d*)/$',
        download_order_metadata, name='downloadOrderMetadata'),
    url(r'^downloadorder/(?P<pk>\d*)/$',
        download_order, name='downloadOrder'),
    url(r'^myorders/$', my_orders, name='myOrders'),
    url(r'^listorders/$', list_orders, name='listOrders'),
    url(r'^ordermonthlyreport/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        order_monthly_report, name='orderMonthlyReport'),
    url(r'^vieworder/(?P<pk>[0-9]+)/$', view_order, name='viewOrder'),
    url(r'^updateorderhistory/$',
        update_order_history, name='updateOrderHistory'),
    url(r'^orderssummary/$', orders_summary, name='ordersSummary'),
    url(r'^order-summary/$', order_summary_mail, name='order-Summary'),
    url(r'^addadhocorder/', add_adhoc_order, name='addAdhocOrder'),
    url(r'^convertprice/', convert_price, name='convertPrice'),
]
