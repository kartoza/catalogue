"""
SANSA-EO Catalogue - others_showPreview - Others views
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
__date__ = '09/08/2013'
__copyright__ = 'South African National Space Agency'


import unittest
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF


class OthersViews_showPreview_Tests(TestCase):
    """
    Tests others.py showPreview method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_showPreview_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showPreview',
                kwargs=myKwargTest)

    @unittest.skip("Skip this test")
    def test_showPreview_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'showPreview',
                kwargs={'theId': '1', 'theSize': 'a'}))
        self.assertEqual(myResp.status_code, 200)
        expString = (
            '<center>\n<img src="/thumbnail/1/a/">\n<div class="btn-group">\n '
            '   <button class="btn btn-info" onclick=\'showMetadata(1);\' alt='
            '"Click to view metadata for this image"\n        title="Click to '
            'view metadata for this image"><i class=" icon-list"></i>\n    </b'
            'utton>\n    <button class="btn btn-success disabled" alt="Click t'
            'o add to your cart"\n        title="You must be logged in to acce'
            'ss cart" ><i class="icon-shopping-cart"></i></button>\n    <butto'
            'n class="btn btn-success" data-toggle="modal" data-target="#myMod'
            'al" id="large_preview" href="/thumbnailpage/1/">\n    <i class="i'
            'con-zoom-in"></i></button></div>\n</center>'
        )
        self.assertEqual(
            myResp.content, expString)
        # check used templates
        myExpTemplates = ['productPreview.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    @unittest.skip("Skip this test")
    def test_showPreview_userlogin(self):
        """
        Test view if user is logged as user
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'showPreview',
                kwargs={'theId': '1', 'theSize': 'a'}))
        self.assertEqual(myResp.status_code, 200)
        expString = (
            '<center>\n<img src="/thumbnail/1/a/">\n<div class="btn-group">\n '
            '   <button class="btn btn-info" onclick=\'showMetadata(1);\' alt='
            '"Click to view metadata for this image"\n        title="Click to '
            'view metadata for this image"><i class=" icon-list"></i>\n    </b'
            'utton>\n    <button class="btn btn-success" onclick=\'addToCart(1'
            ');\' alt="Click to add to your cart"\n        title="Click to add'
            ' this image to your cart" ><i class="icon-shopping-cart"></i></bu'
            'tton>\n    <button class="btn btn-success" data-toggle="modal" da'
            'ta-target="#myModal" id="large_preview" href="/thumbnailpage/1/">'
            '\n    <i class="icon-zoom-in"></i></button></div>\n</center>'
        )
        self.assertEqual(
            myResp.content, expString)
        # check used templates
        myExpTemplates = ['productPreview.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
