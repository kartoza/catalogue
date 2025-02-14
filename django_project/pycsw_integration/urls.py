from django.conf.urls import url

from .views import csw

urlpatterns = [
    url(r'^csw/$', csw, name='pycsw_service'),
]