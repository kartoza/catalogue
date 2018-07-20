from django.conf.urls import patterns, url, include

from useraccounts.forms import EditProfileFormExtra


urlpatterns = patterns(
    '',
    # we must override profile edit to add custom profile form
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
        'useraccounts.views.profile_edit',
        {'edit_profile_form': EditProfileFormExtra},
        name='userena_profile_edit',),
    url(r'^accounts/', include('userena.urls')),
)
