from django.contrib.gis import admin

from .models import SansaUserProfile


class SansaUserProfileAdmin(admin.GeoModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'strategic_partner',)
    list_filter = ('strategic_partner', )
    list_per_page = 100


# we need to deregister our user model if we want to customize it's admin
# as it's already registered by Userena
# http://docs.django-userena.org/en/latest/faq.html
admin.site.unregister(SansaUserProfile)

admin.site.register(SansaUserProfile, SansaUserProfileAdmin)
