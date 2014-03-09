"""
SANSA-EO Catalogue - Initialization, generic and helper methods

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

# for kmz
import zipfile
from cStringIO import StringIO
import os.path
import re
from email.MIMEBase import MIMEBase

import logging
logger = logging.getLogger(__name__)

from django.template import RequestContext
# for rendering template to email
from django.template.loader import render_to_string
# for sending email
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart


from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from orders.models import (
    Order,
    OrderStatusHistory,
    OrderNotificationRecipients
)

from search.models import SearchRecord
from webodt.shortcuts import render_to

# Read default notification recipients from settings
CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS = getattr(
    settings,
    'CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS', False)

###########################################################
#
# EmailMessage subclass that makes it easy to send multipart/related
# messages. For example, including text and HTML versions with inline images.
#
# courtesy of: http://www.cupcakewithsprinkles.com/html-emails-with-inline
#                     -images-in-django/
#
###########################################################


class EmailMultiRelated(EmailMultiAlternatives):
    """
    A version of EmailMessage that makes it easy to send multipart/related
    messages. For example, including text and HTML versions with inline images.
    """
    related_subtype = 'related'

    def __init__(
            self, subject='', body='', from_email=None, to=None, bcc=None,
            connection=None, attachments=None, headers=None,
            alternatives=None):
        # self.related_ids = []
        self.related_attachments = []
        super(EmailMultiRelated, self).__init__(
            subject, body, from_email, to, bcc, connection, attachments,
            headers, alternatives)

    def attach_related(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted and the mimetype is guessed, if not provided.

        If the first parameter is a MIMEBase subclass it is inserted directly
        into the resulting message attachments.
        """

        if isinstance(filename, MIMEBase):
            assert content == mimetype is None
            self.related_attachments.append(filename)
        else:
            assert content is not None
            self.related_attachments.append((filename, content, mimetype))

    def attach_related_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, 'rb').read()
        self.attach_related(filename, content, mimetype)

    def _create_message(self, msg):
        return self._create_attachments(
            self._create_related_attachments(self._create_alternatives(msg)))

    def _create_alternatives(self, msg):
        for i, (content, mimetype) in enumerate(self.alternatives):
            if mimetype == 'text/html':
                for filename, _, _ in self.related_attachments:
                    content = re.sub(r'(?<!cid:)%s' % re.escape(filename),
                                     'cid:%s' % filename, content)
                    self.alternatives[i] = (content, mimetype)

            return super(EmailMultiRelated, self)._create_alternatives(msg)

    def _create_related_attachments(self, msg):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        if self.related_attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.related_subtype,
                                    encoding=encoding)
            if self.body:
                msg.attach(body_msg)
                for related in self.related_attachments:
                    msg.attach(self._create_related_attachment(*related))
        return msg

    def _create_related_attachment(self, filename, content, mimetype=None):
        """
        Convert the filename, content, mimetype triple into a MIME attachment
        object. Adjust headers to use Content-ID where applicable.
        Taken from http://code.djangoproject.com/ticket/4771
        """
        attachment = super(EmailMultiRelated, self)._create_attachment(
            filename, content, mimetype)
        if filename:
            mimetype = attachment['Content-Type']
            del(attachment['Content-Type'])
            del(attachment['Content-Disposition'])
            attachment.add_header('Content-Disposition', 'inline',
                                  filename=filename)
            attachment.add_header('Content-Type', mimetype, name=filename)
            attachment.add_header('Content-ID', '<%s>' % filename)
        return attachment


###########################################################
#
# Object duplication generic code
# from: http://github.com/johnboxall/django_usertools/blob/
#            28c1f243a4882da1e63b60d54a86947db4847cf6/helpers.py#L23
#
# This code could be used to duplicate the Search object
#
###########################################################


from django.db.models.deletion import Collector
from django.db.models.fields.related import ForeignKey


def update_related_field(obj, value, field):
    """
    Set `field` to `value` for all objects related to `obj`.
    Based on heavily off the delete object code:
    http://code.djangoproject.com/browser/django/trunk/django/db/models
                    /query.py#L824
    """
    # Collect all related objects.
    collected_objs = Collector()
    obj._collect_sub_objects(collected_objs)
    classes = collected_objs.keys()
    # Bulk update the objects for performance
    for cls in classes:
        items = collected_objs[cls].items()
        pk_list = [pk for pk, instance in items]
        cls._default_manager.filter(id__in=pk_list).update(**{field: value})
        del instance
    return obj


def duplicate(obj, value=None, field=None, duplicate_order=None):
    """
    Duplicate all related objects of obj setting
    field to value. If one of the duplicate
    objects has an FK to another duplicate object
    update that as well. Return the duplicate copy
    of obj.

    duplicate_order is a list of models which specify how
    the duplicate objects are saved. For complex objects
    this can matter. Check to save if objects are being
    saved correctly and if not just pass in related objects
    in the order that they should be saved.

    """
    collected_objs = Collector()
    obj._collect_sub_objects(collected_objs)
    related_models = collected_objs.keys()
    root_obj = None

    # Sometimes it's good enough just to save in reverse deletion order.
    if duplicate_order is None:
        duplicate_order = reversed(related_models)

    for model in duplicate_order:
        # Find all FKs on model that point to a related_model.
        fks = []
        for f in model._meta.fields:
            if isinstance(f, ForeignKey) and f.rel.to in related_models:
                fks.append(f)
        # Replace each `sub_obj` with a duplicate.
        if model not in collected_objs:
            continue
        sub_obj = collected_objs[model]
        for pk_val, obj in sub_obj.iteritems():
            for fk in fks:
                fk_value = getattr(obj, '%s_id' % fk.name)
                # If this FK has been duplicated then point to the duplicate.
                if fk_value in collected_objs[fk.rel.to]:
                    dupe_obj = collected_objs[fk.rel.to][fk_value]
                    setattr(obj, fk.name, dupe_obj)
            # Duplicate the object and save it.
            obj.id = None
            if field is not None and value is not None:
                setattr(obj, field, value)
            obj.save()
            if root_obj is None:
                root_obj = obj
            # unused
            del pk_val
    return root_obj

###########################################################
#
# Email notification of orders to SANSA sales staff
#
###########################################################


def notifySalesStaff(theUser, theOrderId, theContext=None):
    """
    A helper method to notify sales staff who are subscribed to a sensor
    Example usage from the console / doctest:


       >>> from catalogue.views import *
       >>> myUser = User.objects.get(id=1)
       >>> myUser
       >>> notifySalesStaff(myUser, 16)
    Args:
        theUser obj - Required. Django user object
        theOrderId int - Required. ID of the Order which has changed
        theContext obj - Optional. Useful when we need to pass RequestContext
            to the render_to_string (see Note)

    Note:
        RequestContext is important when executing unittests using test.client
        because of the way test.client generates response context object.
        Response context is a list of context objects, one for each used
        template, and if during rendering of a template context object is None,
        values of response context object are going to be empty. For example
        myResp.context['myObjects'] = [], but in reality it should have values
    """

    if not settings.EMAIL_NOTIFICATIONS_ENABLED:
        logger.info('Email sending disabled, set EMAIL_NOTIFICATIONS_ENABLED '
                    'in settings')
        return
    myOrder = get_object_or_404(Order, id=theOrderId)
    myRecords = SearchRecord.objects.filter(user=theUser,
                                            order=myOrder).select_related()
    myHistory = OrderStatusHistory.objects.filter(order=myOrder)
    theOrderPDF = render_to(template_name='order-summary.odt',
                            dictionary={
                                'myOrder': myOrder,
                                'myRecords': myRecords,
                                'myHistory': myHistory
                            },
                            format='pdf')
    myEmailSubject = ('SANSA Order ' + str(myOrder.id) + ' status update (' +
                      myOrder.order_status.name + ')')

    # Get a list of staff user's email addresses
    # we will use mass_mail to prevent users seeing who other recipients are
    myMessagesList = []

    myRecipients = set()
    myRecipients.update([theUser])
    logger.info('User recipient added: %s' % str(myRecipients))
    # get the list of recipients
    for myProduct in [s.product for s in myRecords]:
        myRecipients.update(
            OrderNotificationRecipients.getUsersForProduct(myProduct))

    # Add default recipients
    if not myRecipients and CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS:
        logger.info('Sending notice to default recipients : %s' %
                    CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)
        myRecipients.update(list(CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS))

    for myRecipient in myRecipients:
        #txt email template
        myEmailMessage_txt = render_to_string(
            'mail/order.txt', {
                'myOrder': myOrder,
                'myRecords': myRecords,
                'myHistory': myHistory,
                'myRecipient': myRecipient,
                'domain': settings.DOMAIN
            }, theContext)
        #html email template
        myEmailMessage_html = render_to_string(
            'mail/order.html', {
                'myOrder': myOrder,
                'myRecords': myRecords,
                'myHistory': myHistory,
                'myRecipient': myRecipient,
                'domain': settings.DOMAIN
            }, theContext)
        myAddress = myRecipient.email
        myMsg = EmailMultiRelated(
            myEmailSubject,
            myEmailMessage_txt,
            'dontreply@' + settings.DOMAIN, [myAddress])
        logger.info('Sending notice to : %s' % myAddress)

        #attach alternative payload - html
        myMsg.attach_alternative(myEmailMessage_html, 'text/html')
        # add required images, as inline attachments,
        # accesed by 'name' in templates
        myMsg.attach_related_file(
            os.path.join(
                settings.STATIC_ROOT, 'images', 'sac_header_email.jpg'))
        # get the filename of a PDF, ideally we should reuse theOrderPDF object
        myMsg.attach_related_file(theOrderPDF.name)
        #add message
        myMessagesList.append(myMsg)

    logger.info('Sending messages: \n%s' % myMessagesList)
    # initiate email connection, and send messages in bulk
    myEmailConnection = mail.get_connection()
    myEmailConnection.send_messages(myMessagesList)
    return


"""Layer definitions for use in conjunction with open layers"""
WEB_LAYERS = {
            # Streets and boundaries for SA base map with an
            # underlay of spot 2010 2m mosaic
            #
            # Uses the degraded 2.5m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single
            # layer for best quality.
          'ZaSpot2mMosaic2010TC':
              """var zaSpot2mMosaic2010TC = new OpenLayers.Layer.WMS(
              '2m Mosaic 2010 TC', 'http://""" +
              settings.WMS_SERVER + """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic2m2010',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay
            # of spot 2009 2m mosaic
            #
            # Uses the degraded 2.5m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer
            # for best quality.
          'ZaSpot2mMosaic2009TC':
              """var zaSpot2mMosaic2009TC = new OpenLayers.Layer.WMS(
              '2m Mosaic 2009 TC', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic2m2009',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay
            # of spot 2008 mosaic. Uses the degraded 2m product in a tile cache
            # and under that blue marble. Its rendered as a single layer for
            # best quality.
          'ZaSpot2mMosaic2008TC':
              """var zaSpot2mMosaic2008TC = new OpenLayers.Layer.WMS(
              '2m Mosaic 2008 TC', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic2m2008',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay of spot
            # 2007 mosaic. Uses the degraded 2m product in a tile cache
            # and under that blue marble. Its rendered as a single layer
            # for best quality.
          'ZaSpot2mMosaic2007TC':
            """var zaSpot2mMosaic2007TC = new OpenLayers.Layer.WMS(
            '2m Mosaic 2007 TC', 'http://""" + settings.WMS_SERVER +
            """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic2m2007',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay of spot
            # 2010 mosaic and under that blue marble. Its rendered as a single
            # layer for best quality.
          'ZaSpot2mMosaic2010':
              """var zaSpot2mMosaic2010 = new OpenLayers.Layer.WMS(
              '2m Mosaic 2010', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/mapserv?map=ZA_SPOT2010',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             layers: 'Roads',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay of
            # spot 2009 mosaic and under that blue marble. Its rendered as a
            # single layer for best quality.
            'ZaSpot2mMosaic2009':
                """var zaSpot2mMosaic2009 = new OpenLayers.Layer.WMS(
                '2m Mosaic 2009', 'http://""" + settings.WMS_SERVER +
                """/cgi-bin/mapserv?map=ZA_SPOT2009',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             layers: 'Roads',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
           # Streets and boundaries for SA base map with an underlay of spot
           # 2008 mosaic and under that blue marble. Its rendered as a single
           # layer for best quality.
           'ZaSpot2mMosaic2008':
               """var zaSpot2mMosaic2008 = new OpenLayers.Layer.WMS(
               '2m Mosaic 2008', 'http://""" +
               settings.WMS_SERVER + """/cgi-bin/mapserv?map=ZA_SPOT2008',
           {
              width: '800',
              layers: 'Roads',
              srs: 'EPSG:900913',
              maxResolution: '156543.0339',
              VERSION: '1.1.1',
              EXCEPTIONS: 'application/vnd.ogc.se_inimage',
              height: '525',
              format: 'image/jpeg',
              transparent: 'false',
              antialiasing: 'true'
            },
            {isBaseLayer: true});
           """,
           # Streets and boundaries for SA base map with an underlay of spot
           # 2007 mosaic and under that blue marble. Its rendered as a single
           # layer for best quality.
           'ZaSpot2mMosaic2007':
               """var zaSpot2mMosaic2007 = new OpenLayers.Layer.WMS(
              '2m Mosaic 2007', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/mapserv?map=ZA_SPOT2007',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             layers: 'Roads',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay of
            # spot 2010 mosaic. Uses the degraded 10m product in a tile cache
            # and under that blue marble. Its rendered as a single layer for
            # best quality.
          'ZaSpot10mMosaic2010':
              """var zaSpot10mMosaic2010 = new OpenLayers.Layer.WMS(
              '10m Mosaic 2010 TC', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic10m2010',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay of spot
            # 2009 mosaic. Uses the degraded 10m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for
            # best quality.
          'ZaSpot10mMosaic2009':
              """var zaSpot10mMosaic2009 = new OpenLayers.Layer.WMS(
              '10m Mosaic 2009 TC', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic10m2009',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay of
            # spot 2008 mosaic
            #
            # Uses the degraded 10 product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for
            # best quality.
          'ZaSpot10mMosaic2008':
              """var zaSpot10mMosaic2008 = new OpenLayers.Layer.WMS(
              '10m Mosaic 2008 TC', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic10m2008',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Streets and boundaries for SA base map with an underlay of spot
            # 2007 mosaic
            #
            # Uses the degraded 10 product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for
            # best quality.
          'ZaSpot10mMosaic2007':
              """var zaSpot10mMosaic2007 = new OpenLayers.Layer.WMS(
              '10m Mosaic 2007 TC', 'http://""" + settings.WMS_SERVER +
              """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic10m2007',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
           # Spot5 ZA 2008 10m Mosaic directly from mapserver
            'ZaSpot5Mosaic2008':
                """var zaSpot5Mosaic2008 = new OpenLayers.Layer.WMS(
                'SPOT5 10m Mosaic 2008, ZA',
                'http://""" + settings.WMS_SERVER +
                """/cgi-bin/mapserv?map=ZA_SPOT',
            {
              VERSION: '1.1.1',
              EXCEPTIONS: 'application/vnd.ogc.se_inimage',
              layers: 'Spot5_RSA_2008_10m',
              maxResolution: '156543.0339',
            });
            zaSpot5Mosaic2008.setVisibility(false);
            """,
           #a Vector only version of the above
          'ZaRoadsBoundaries':
               """var zaRoadsBoundaries = new OpenLayers.Layer.WMS(
               'SA Vector', 'http://""" + settings.WMS_SERVER +
               """/cgi-bin/tilecache.cgi?',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             //layers: 'Roads',
             layers: 'za_vector',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           """,
            # Map of all search footprints that have been made.
            # Transparent: true will make a wms layer into an overlay
            'Searches': """var searches = new OpenLayers.Layer.WMS(
                'Searches', 'http://""" + settings.WMS_SERVER +
                """/cgi-bin/mapserv?map=SEARCHES',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             layers: 'searches',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false});
           """,
        # Map of site visitors
        # Transparent: true will make a wms layer into an overlay
        'Visitors': """var visitors = new OpenLayers.Layer.WMS(
          'Visitors', 'http://""" + settings.WMS_SERVER +
          """/cgi-bin/mapserv?map=VISITORS',
          {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             width: '800',
             layers: 'visitors',
             styles: '',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false}
       );
        """,
        # Nasa Blue marble directly from mapserver
            'BlueMarble':
            """var BlueMarble = new OpenLayers.Layer.WMS('BlueMarble',
                'http://""" + settings.WMS_SERVER +
                """/cgi-bin/mapserv?map=WORLD',
            {
             VERSION: '1.1.1',
             EXCEPTIONS: 'application/vnd.ogc.se_inimage',
             layers: 'BlueMarble',
             maxResolution: '156543.0339'
            });
            BlueMarble.setVisibility(false);
            """,
        #
        # Google
        #
       'GooglePhysical': """var gphy = new OpenLayers.Layer.Google(
           'Google Physical',
           {type: G_PHYSICAL_MAP}
          );
       """,
        #
        # Google streets
        #
        'GoogleStreets': """var gmap = new OpenLayers.Layer.Google(
           'Google Streets' // the default
          );
        """,
        #
        # Google hybrid
        #
        'GoogleHybrid': """ var ghyb = new OpenLayers.Layer.Google(
           'Google Hybrid',
           {type: G_HYBRID_MAP}
          );
        """,
        #
        # Google Satellite
        #
        'GoogleSatellite': """var gsat = new OpenLayers.Layer.Google(
           'Google Satellite',
           {type: G_SATELLITE_MAP}
          );
        """,
        #
        # Heatmap - all
        #
        'Heatmap-total': """var heatmap_total = new OpenLayers.Layer.Image(
                'Heatmap total',
                '/media/heatmaps/heatmap-total.png',
                new OpenLayers.Bounds(-20037508.343,
                                      -16222639.241,
                                      20019734.329,
                                      16213801.068),
                new OpenLayers.Size(1252,1013),
                {isBaseLayer: true,
                maxResolution: 156543.0339
                }
           );
        """,
        #
        # Heatmap - last3month
        #
        'Heatmap-last3month':
            """var heatmap_last3month = new OpenLayers.Layer.Image(
                'Heatmap last 3 months',
                '/media/heatmaps/heatmap-last3month.png',
                new OpenLayers.Bounds(-20037508.343,
                                      -16222639.241,
                                      20019734.329,
                                      16213801.068),
                new OpenLayers.Size(1252,1013),
                {isBaseLayer: true,
                maxResolution: 156543.0339
                }
           );
        """,
        #
        # Heatmap - last month
        #
        'Heatmap-lastmonth':
            """var heatmap_lastmonth = new OpenLayers.Layer.Image(
                'Heatmap last month',
                '/media/heatmaps/heatmap-lastmonth.png',
                new OpenLayers.Bounds(-20037508.343,
                                      -16222639.241,
                                      20019734.329,
                                      16213801.068),
                new OpenLayers.Size(1252,1013),
                {isBaseLayer: true,
                maxResolution: 156543.0339
                }
           );
        """,
        #
        # Heatmap - last week
        #
        'Heatmap-lastweek':
            """var heatmap_lastweek = new OpenLayers.Layer.Image(
                'Heatmap last week',
                '/media/heatmaps/heatmap-lastweek.png',
                new OpenLayers.Bounds(-20037508.343,
                                      -16222639.241,
                                      20019734.329,
                                      16213801.068),
                new OpenLayers.Size(1252,1013),
                {isBaseLayer: true,
                maxResolution: 156543.0339
                }
           );
        """,
        # Note for this layer to be used you need to regex replace
        # USERNAME with theRequest.user.username
        'CartLayer':
            """var cartLayer = new OpenLayers.Layer.WMS('Cart', 'http://""" +
            settings.WMS_SERVER + """/cgi-bin/mapserv?map=""" +
            settings.CART_LAYER + """&user=USERNAME',
          {
             version: '1.1.1',
             width: '800',
             layers: 'Cart',
             srs: 'EPSG:4326',
             height: '525',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false});
           """,
        }

mLayerJs = {
    'VirtualEarth': (
        '<script src="http://dev.virtualearth.net/mapcontrol/mapcontrol.'
        'ashx?v=6.1"></script>'),
    'Google': (
        '<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;'
        'key="{{GOOGLE_MAPS_API_KEY}}"></script>')
}


# Note this code is from Tims personal codebase and copyright is retained
@login_required
def genericAdd(
        theRequest,
        theFormClass,
        theTitle,
        theRedirectPath,
        theOptions):
    myObject = getObject(theFormClass)
    logger.info('Generic add called')
    if theRequest.method == 'POST':
        # create a form instance using reflection
        # see http://stackoverflow.com/questions/452969/does-python-have-an
        #         -equivalent-to-java-class-forname/452981
        myForm = myObject(theRequest.POST, theRequest.FILES)
        myOptions = {
            'myForm': myForm,
            'myTitle': theTitle
        }
        # shortcut to join two dicts
        myOptions.update(theOptions),
        if myForm.is_valid():
            myObject = myForm.save(commit=False)
            myObject.user = theRequest.user
            myObject.save()
            logger.info('Add : data is valid')
            return HttpResponseRedirect(theRedirectPath + str(myObject.id))
        else:
            logger.info('Add : form is NOT valid')
            return render_to_response(
                'add.html', myOptions,
                context_instance=RequestContext(theRequest))
    else:
        myForm = myObject()
        myOptions = {
            'myForm': myForm,
            'myTitle': theTitle
        }
        #shortcut to join two dicts
        myOptions.update(theOptions),
        logger.info('Add : new object requested')
        return render_to_response(
            'add.html', myOptions,
            context_instance=RequestContext(theRequest))


def genericDelete(theRequest, theObject):
    if theObject.user != theRequest.user:
        return ({'myMessage': 'You can only delete an entry that you own!'})
    else:
        theObject.delete()
        return {'myMessage': 'Entry was deleted successfully'}


def getObject(theClass):
    #Create an object instance using reflection
    #from http://stackoverflow.com/questions/452969/does-python-have-an
    #           -equivalent-to-java-class-forname/452981
    myParts = theClass.split('.')
    myModule = '.'.join(myParts[:-1])
    myObject = __import__(myModule)
    for myPath in myParts[1:]:
        myObject = getattr(myObject, myPath)
    return myObject


@login_required
def isStrategicPartner(theRequest):
    """Returns true if the current user is a CSIR strategic partner
    otherwise false"""
    myProfile = None
    try:
        myProfile = theRequest.user.get_profile()
    except:
        logger.debug('Profile does not exist')
    myPartnerFlag = False
    if myProfile and myProfile.strategic_partner:
        myPartnerFlag = True
    return myPartnerFlag


def standardLayers(theRequest):
    """Helper methods used to return standard layer defs for the openlayers
       control
       .. note:: intended to be published as a view in urls.py

      e.g. usage:
      myLayersList, myLayerDefinitions, myActiveLayer =
           standardLayers(theRequest)
      where:
        myLayersList will be a string representing a javascript array of layers
        myLayerDefinitions will be an array of strings each representing
            javascript / openlayers layer defs
        myActiveLayer will be the name of the active base map
      """

    myProfile = None
    myLayersList = None
    myLayerDefinitions = None
    myActiveBaseMap = None
    try:
        myProfile = theRequest.user.get_profile()
    except:
        logger.debug('Profile does not exist')
    if myProfile and myProfile.strategic_partner:
        myLayerDefinitions = [
            WEB_LAYERS['ZaSpot2mMosaic2010TC'],
            WEB_LAYERS['ZaSpot2mMosaic2009TC'],
            WEB_LAYERS['ZaSpot2mMosaic2008TC'],
            WEB_LAYERS['ZaSpot2mMosaic2007TC'],
            WEB_LAYERS['ZaSpot10mMosaic2010'],
            WEB_LAYERS['ZaSpot10mMosaic2009'],
            WEB_LAYERS['ZaSpot10mMosaic2008'],
            WEB_LAYERS['ZaSpot10mMosaic2007'],
            WEB_LAYERS['ZaRoadsBoundaries']]
        myLayersList = (
            '[zaSpot2mMosaic2010TC, zaSpot2mMosaic2009TC,'
            'zaSpot2mMosaic2008TC, zaSpot2mMosaic2007TC, zaSpot10mMosaic2010,'
            'zaSpot10mMosaic2009,zaSpot10mMosaic2008,zaSpot10mMosaic2007,'
            'zaRoadsBoundaries ]')
        myActiveBaseMap = 'zaSpot2mMosaic2010TC'
    else:
        myLayerDefinitions = [
            WEB_LAYERS['ZaSpot10mMosaic2010'],
            WEB_LAYERS['ZaSpot10mMosaic2009'],
            WEB_LAYERS['ZaSpot10mMosaic2008'],
            WEB_LAYERS['ZaSpot10mMosaic2007'],
            WEB_LAYERS['ZaRoadsBoundaries']]
        myLayersList = (
            '[zaSpot10mMosaic2010,zaSpot10mMosaic2009,'
            'zaSpot10mMosaic2008,zaSpot10mMosaic2007,'
            'zaRoadsBoundaries]')
        myActiveBaseMap = 'zaSpot10mMosaic2010'
    return myLayersList, myLayerDefinitions, myActiveBaseMap


def standardLayersWithCart(theRequest):
    """Helper methods used to return standard layer defs for the openlayers
       control
       .. note:: intended to be published as a view in urls.py
       Note. Appends the cart layer to the list of layers otherwise much the
       same as standardLayers method
       e.g. usage:
       myLayersList, myLayerDefinitions, myActiveLayer =
         standardLayers(theRequest)
       where:
        myLayersList will be a string representing a javascript array of layers
        myLayerDefinitions will be an array of strings each representing
          javascript / openlayers layer defs
        myActiveLayer will be the name of the active base map
      """
    (myLayersList,
     myLayerDefinitions, myActiveBaseMap) = standardLayers(theRequest)
    myLayersList = myLayersList.replace(']', ',cartLayer]')
    myLayerDefinitions.append(
        WEB_LAYERS['CartLayer'].replace('USERNAME', theRequest.user.username))
    return myLayersList, myLayerDefinitions, myActiveBaseMap


def writeThumbToZip(theImagePath, theProductId, theZip):
    """Write a thumb and its world file into a zip file.

    Args:
        theImagePath: str required - path to the image file to write. For the
            world file its extension will be replaced with .wld.
        theProductId: str required - product id used as the output file name
            in the zip file.
        theZip: ZipFile required - handle to a ZipFile instance in which the
            images will be written.

    Returns:
        bool: True on success, False on failure

    Raises:
        Exceptions and issues are logged but not raised.
    """

    myWLDFile = '%s.wld' % os.path.splitext(theImagePath)[0]
    try:
        if os.path.isfile(theImagePath):
            with open(theImagePath, 'rb') as myFile:
                theZip.writestr('%s.jpg' % theProductId,
                               myFile.read())
                logger.debug('Adding thumbnail image to archive.')
        else:
            raise Exception('Thumbnail image not found: %s' % theImagePath)
        if os.path.isfile(myWLDFile):
            with open(myWLDFile, 'rb') as myFile:
                theZip.writestr('%s.wld' % theProductId,
                               myFile.read())
                logger.debug('Adding worldfile to archive.')
        else:
            raise Exception('World file not found: %s' % myWLDFile)
    except:
        logger.exception('Error writing thumb to zip')
        return False
    return True


def writeSearchRecordThumbToZip(theSearchRecord, theZip):
    """A helper function to write a thumbnail into a zip file.
    @parameter myRecord - a searchrecord instance
    @parameter theZip - a zip file handle ready to write stuff to
    """
    # Try to add thumbnail + wld file, we assume that jpg and wld
    # file have same name

    myImageFile = theSearchRecord.product.georeferencedThumbnail()
    return writeThumbToZip(myImageFile,
                           theSearchRecord.product.product_id,
                           theZip)

#render_to_kml helpers
def render_to_kml(theTemplate, theContext, filename):
    response = HttpResponse(render_to_string(theTemplate, theContext))
    response['Content-Type'] = 'application/vnd.google-earth.kml+xml'
    response['Content-Disposition'] = 'attachment; filename=%s.kml' % filename
    return response


def render_to_kmz(theTemplate, theContext, filename):
    """Render a kmz file. If search records are supplied, their georeferenced
    thumbnails will be bundled into the kmz archive."""
    #try to get MAX_METADATA_RECORDS from settings, default to 500
    myMaxMetadataRecords = getattr(settings, 'MAX_METADATA_RECORDS', 500)
    myKml = render_to_string(theTemplate, theContext)
    myZipData = StringIO()
    myZip = zipfile.ZipFile(myZipData, 'w', zipfile.ZIP_DEFLATED)
    myZip.writestr('%s.kml' % filename, myKml)
    if 'mySearchRecords' in theContext:
        for myRecord in theContext['mySearchRecords'][:myMaxMetadataRecords]:
            writeSearchRecordThumbToZip(myRecord, myZip)
    myZip.close()
    response = HttpResponse()
    response.content = myZipData.getvalue()
    response['Content-Type'] = 'application/vnd.google-earth.kmz'
    response['Content-Disposition'] = 'attachment; filename=%s.kmz' % filename
    response['Content-Length'] = str(len(response.content))
    return response


def downloadISOMetadata(theSearchRecords, theName):
    """ returns ZIPed XML metadata files for each product """
    response = HttpResponse()
    myZipData = StringIO()
    myZip = zipfile.ZipFile(myZipData, 'w', zipfile.ZIP_DEFLATED)
    #try to get MAX_METADATA_RECORDS from settings, default to 500
    myMaxMetadataRecords = getattr(settings, 'MAX_METADATA_RECORDS', 500)
    for mySearchRecord in theSearchRecords[:myMaxMetadataRecords]:
        myMetadata = mySearchRecord.product.getXML()
        logger.info('Adding product XML to ISO Metadata archive.')
        myZip.writestr('%s.xml' % mySearchRecord.product.product_id,
                       myMetadata)
        writeSearchRecordThumbToZip(mySearchRecord, myZip)

    myZip.close()
    response.content = myZipData.getvalue()
    myZipData.close()
    #get ORGANISATION_ACRONYM from settings, default to 'SANSA'
    myOrganisationAcronym = getattr(settings, 'ORGANISATION_ACRONYM', 'SANSA')
    filename = '%s-%s-Metadata.zip' % (myOrganisationAcronym, theName)
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = str(len(response.content))
    return response


def downloadHtmlMetadata(theSearchRecords, theName):
    """ returns ZIPed html metadata files for each product """
    response = HttpResponse()
    myZipData = StringIO()
    myZip = zipfile.ZipFile(myZipData, 'w', zipfile.ZIP_DEFLATED)
    #try to get MAX_METADATA_RECORDS from settings, default to 500
    myMaxMetadataRecords = getattr(settings, 'MAX_METADATA_RECORDS', 500)
    # used to tell html renderer not to prepend server path
    myThumbIsLocalFlag = True
    for mySearchRecord in theSearchRecords[:myMaxMetadataRecords]:
        myMetadata = mySearchRecord.product.getConcreteInstance().toHtml(
            myThumbIsLocalFlag)
        logger.info('Adding product HTML to HTML Metadata archive.')
        myZip.writestr('%s.html' % mySearchRecord.product.product_id,
                       myMetadata)
        writeSearchRecordThumbToZip(mySearchRecord, myZip)

    myZip.close()
    response.content = myZipData.getvalue()
    myZipData.close()
    #get ORGANISATION_ACRONYM from settings, default to 'SANSA'
    myOrganisationAcronym = getattr(settings, 'ORGANISATION_ACRONYM', 'SANSA')
    filename = '%s-%s-Metadata.zip' % (myOrganisationAcronym, theName)
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = str(len(response.content))
    return response
