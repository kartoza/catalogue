from django.conf.urls import patterns, url

from .views import csw

urlpatterns = patterns(
    '',
    url(r'^csw$', csw, name='pycsw_service'),
)
