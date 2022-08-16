"""
SANSA-EO Catalogue - Catalogue forms

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
logger = logging.getLogger(__name__)

from django import forms
from django.contrib.auth.models import User

from catalogue.geometrywidget import GeometryWidget

from search.models import Clip


class ClipForm(forms.ModelForm):
    """
    Allows the CSIR Partner user to clip one of the Extra Layers by a given
    geometry.
    """

    image = forms.ChoiceField(choices=[
        (0, 'zaSpot2mMosaic2009'),
        (1, 'zaSpot2mMosaic2008'),
        (2, 'zaSpot2mMosaic2007')])
    geometry = forms.CharField(
        widget=GeometryWidget, required=False,
        help_text=(
            'You can digitise your clip area directly, or alternatively use '
            'the file upload option below to upload the clip shapefile. You '
            'can use the help tab in the map area for more information on how '
            'to use the map. Draw an area of interest on the map to refine the'
            ' set of search results to a specific area.'))
    geometry_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'file'}),
        required=False,
        help_text=(
            'Upload a zipped shapefile of less than 1MB. If the shapefile '
            'contains more than one polygon, only the first will be used. The '
            'computation time is related to polygon complexity. For multipart '
            'and non-polygon features the bounding box of the first feature '
            'will be used.'))

    class Meta:
        model = Clip
        exclude = ('result_url', 'owner', 'guid', 'status')


class MessageForm(forms.Form):
    """An unbound form that creates a Message submission form to a single user
    """

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].choices = [('', '----------')] + [
            (myUser.id, myUser) for myUser in User.objects.all().order_by(
                'username')
        ]

    user_id = forms.ChoiceField(choices=(), widget=forms.Select())

    message = forms.CharField(
        label='Message:',
        # <-- specify the textarea widget!
        widget=forms.Textarea,
        required=True,
        help_text='Enter a message here',
        error_messages={
            'required': 'A message is required!'}
    )


class AllUsersMessageForm(forms.Form):
    """An unbound form that creates a Message submission form """

    message = forms.CharField(
        label='Message:',
        widget=forms.Textarea,
        # <-- specify the textarea widget!
        required=True,
        help_text='Enter a message here',
        error_messages={
            'required': 'A message is required!'}
    )
