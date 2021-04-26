from django import forms
from userena.forms import EditProfileForm
from userena.utils import get_profile_model


class EditProfileFormExtra(EditProfileForm):
    first_name = forms.CharField(
        label='First name (required)',
        max_length=30, required=True)
    last_name = forms.CharField(
        label='Last name (required)',
        max_length=30, required=True)

    class Meta:
        model = get_profile_model()
        exclude = ('user', 'mugshot', 'strategic_partner', 'privacy')
