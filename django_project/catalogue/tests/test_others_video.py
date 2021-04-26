"""
SANSA-EO Catalogue - others_video - Others views
    unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.2'
__date__ = '08/08/2013'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class OthersViews_video(TestCase):
    """
    Tests others.py video method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_video_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'video',
                kwargs=myKwargTest)

    def test_video_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(reverse('video', kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        # check used templates
        myExpTemplates = [
            'video.html', 'base.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
