from django.contrib.gis import admin

from .models import Search


class SearchAdmin(admin.GeoModelAdmin):
    list_display = ('search_date', 'user', 'guid', 'search_date')
    list_filter = ('search_date', 'user', )

admin.site.register(Search, SearchAdmin)
