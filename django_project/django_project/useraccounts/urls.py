from userena import views
from django.conf.urls import url, include

from useraccounts.forms import EditProfileFormExtra

urlpatterns = [
    # we must override profile edit to add custom profile form
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
        views.profile_edit,
        {'edit_profile_form': EditProfileFormExtra},
        name='userena_profile_edit', ),
    url(r'^accounts/', include('userena.urls')),
]
