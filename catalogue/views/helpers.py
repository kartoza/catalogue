###########################################################
#
# Initialization, generic and helper methods
#
###########################################################
import logging

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse

from catalogue.models import *
from django.template import RequestContext
# for rendering template to email
from django.template.loader import render_to_string

# for sending email
from django.core import mail

# for kmz
import zipfile
from cStringIO import StringIO

import os.path
import re
from email.MIMEBase import MIMEBase

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart

# Read default notification recipients from settings
CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS = getattr(settings, 'CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS', False )

###########################################################
#
# EmailMessage subclass that makes it easy to send multipart/related
# messages. For example, including text and HTML versions with inline images.
#
# courtesy of: http://www.cupcakewithsprinkles.com/html-emails-with-inline-images-in-django/
#
###########################################################

class EmailMultiRelated(EmailMultiAlternatives):
  """
  A version of EmailMessage that makes it easy to send multipart/related
  messages. For example, including text and HTML versions with inline images.
  """
  related_subtype = 'related'
 
  def __init__(self, subject='', body='', from_email=None, to=None, bcc=None, connection=None, attachments=None, headers=None, alternatives=None):
    # self.related_ids = []
    self.related_attachments = []
    return super(EmailMultiRelated, self).__init__(subject, body, from_email, to, bcc, connection, attachments, headers, alternatives)

  def attach_related(self, filename=None, content=None, mimetype=None):
    """
    Attaches a file with the given filename and content. The filename can
    be omitted and the mimetype is guessed, if not provided.

    If the first parameter is a MIMEBase subclass it is inserted directly
    into the resulting message attachments.
    """

    if isinstance(filename, MIMEBase):
      assert content == mimetype == None
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
    return self._create_attachments(self._create_related_attachments(self._create_alternatives(msg)))

  def _create_alternatives(self, msg):
    for i, (content, mimetype) in enumerate(self.alternatives):
      if mimetype == 'text/html':
        for filename, _, _ in self.related_attachments:
          content = re.sub(r'(?<!cid:)%s' % re.escape(filename), 'cid:%s' % filename, content)
          self.alternatives[i] = (content, mimetype)

      return super(EmailMultiRelated, self)._create_alternatives(msg)

  def _create_related_attachments(self, msg):
    encoding = self.encoding or settings.DEFAULT_CHARSET
    if self.related_attachments:
      body_msg = msg
      msg = SafeMIMEMultipart(_subtype=self.related_subtype, encoding=encoding)
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
      attachment = super(EmailMultiRelated, self)._create_attachment(filename, content, mimetype)
      if filename:
        mimetype = attachment['Content-Type']
        del(attachment['Content-Type'])
        del(attachment['Content-Disposition'])
        attachment.add_header('Content-Disposition', 'inline', filename=filename)
        attachment.add_header('Content-Type', mimetype, name=filename)
        attachment.add_header('Content-ID', '<%s>' % filename)
      return attachment


###########################################################
#
# Object duplication generic code
# from: http://github.com/johnboxall/django_usertools/blob/28c1f243a4882da1e63b60d54a86947db4847cf6/helpers.py#L23
#
# This code could be used to duplicate the Search object
#
###########################################################


from django.db.models.query import CollectedObjects
from django.db.models.fields.related import ForeignKey
from django.forms.models import model_to_dict


def update_related_field(obj, value, field):
    """
    Set `field` to `value` for all objects related to `obj`.
    Based on heavily off the delete object code:
    http://code.djangoproject.com/browser/django/trunk/django/db/models/query.py#L824

    """
    # Collect all related objects.
    collected_objs = CollectedObjects()
    obj._collect_sub_objects(collected_objs)
    classes = collected_objs.keys()
    # Bulk update the objects for performance
    for cls in classes:
        items = collected_objs[cls].items()
        pk_list = [pk for pk, instance in items]
        cls._default_manager.filter(id__in=pk_list).update(**{field:value})
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
    collected_objs = CollectedObjects()
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
                fk_value = getattr(obj, "%s_id" % fk.name)
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
    return root_obj

###########################################################
#
# Email notification of orders to sac sales staff
#
###########################################################
def notifySalesStaff(theUser, theOrderId):
  """ A helper method to notify sales staff who are subscribed to a sensor
     Example usage from the console / doctest:
     >>> from catalogue.models import *
     >>> from catalogue.views import *
     >>> myUser = User.objects.get(id=1)
     >>> myUser
     >>> notifySalesStaff( myUser, 16 )

  """

  if not settings.EMAIL_NOTIFICATIONS_ENABLED:
    logging.info("Email sending disabled, set EMAIL_NOTIFICATIONS_ENABLED in settings")
    return
  myOrder = get_object_or_404(Order,id=theOrderId)
  myRecords = SearchRecord.objects.filter(user=theUser, order=myOrder).select_related()
  myHistory = OrderStatusHistory.objects.filter(order=myOrder)

  myEmailSubject = 'SAC Order ' + str(myOrder.id) + ' status update (' + myOrder.order_status.name + ')'

  # Get a list of staff user's email addresses
  myMessagesList = [] # we will use mass_mail to prevent users seeing who other recipients are

  myRecipients = set()
  # get the list of recipients
  for myProduct in [s.product for s in myRecords]:
    myRecipients.update(OrderNotificationRecipients.getUsersForProduct(myProduct))

  # Add default recipients
  if not myRecipients and CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS:
    logging.info("Sending notice to default recipients : %s" % CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)
    myRecipients.update(list(CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS))

  for myRecipient in myRecipients:
    #txt email template
    myEmailMessage_txt = render_to_string( 'mail/order.txt', { 'myOrder': myOrder,
                                                    'myRecords' : myRecords,
                                                    'myHistory' : myHistory,
                                                    'myRecipient': myRecipient,
                                                    'domain':settings.DOMAIN
                                                  })
    #html email template
    myEmailMessage_html = render_to_string( 'mail/order.html', { 'myOrder': myOrder,
                                                      'myRecords' : myRecords,
                                                      'myHistory' : myHistory,
                                                      'myRecipient': myRecipient,
                                                      'domain':settings.DOMAIN
                                                  })
    myAddress = myRecipient.email
    myMsg = EmailMultiRelated(myEmailSubject, myEmailMessage_txt, 'dontreply@' + settings.DOMAIN, [myAddress])
    logging.info("Sending notice to : %s" % myAddress)

    #attach alternative payload - html
    myMsg.attach_alternative(myEmailMessage_html,'text/html')
    #add required images, as inline attachments, accesed by 'name' in templates
    myMsg.attach_related_file(os.path.join(settings.MEDIA_ROOT,'images','sac_header.jpg'))
    #add message
    myMessagesList.append(myMsg)

  logging.info("Sending messages: \n%s" % myMessagesList)
  # initiate email connection, and send messages in bulk
  myEmailConnection = mail.get_connection()
  myEmailConnection.send_messages(myMessagesList)
  return

###########################################################
#
# Email notification of tasking requests to sac sales staff
#
###########################################################
def notifySalesStaffOfTaskRequest(theUser, theId):
  """ A helper method to notify tasking staff who are subscribed to a sensor
     Example usage from the console / doctest:
     >>> from catalogue.models import *
     >>> from catalogue.views import *
     >>> myUser = User.objects.get(id=1)
     >>> myUser
     >>> notifySalesStaffOfTaskRequest( myUser, 11 )"""
  if not settings.EMAIL_NOTIFICATIONS_ENABLED:
    logging.info("Email sending disabled, set EMAIL_NOTIFICATIONS_ENABLED in settings")
    return
  myTaskingRequest = get_object_or_404(TaskingRequest,id=theId)
  myHistory = OrderStatusHistory.objects.all().filter(order=myTaskingRequest)
  myEmailSubject = 'SAC Tasking Request ' + str(myTaskingRequest.id) + ' status update (' + myTaskingRequest.order_status.name + ')'
  myEmailMessage = 'The status for tasking order #' +  str(myTaskingRequest.id) + ' has changed. Please visit the tasking request page:\n'
  myEmailMessage = myEmailMessage + 'http://' + settings.DOMAIN + '/viewtaskingrequest/' + str(myTaskingRequest.id) + '/\n\n\n'
  myTemplate = "taskingEmail.txt"
  myEmailMessage += render_to_string( myTemplate, { 'myOrder': myTaskingRequest,
                                                    'myHistory' : myHistory
                                                  })
  myMessagesList = [] # we will use mass_mail to prevent users seeing who other recipients are
  myRecipients = OrderNotificationRecipients.objects.filter(sensors=t.mission_sensor)
  for myRecipient in myRecipients:
    myMessagesList.append((myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN,
          [myRecipient.user.email]))
    logging.info("Sending notices to : %s" % myRecipient.user.email)

  # Add default
  if not myRecipients and CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS:
    logging.info("Sending notice to default recipients : %s" % CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)
    myMessagesList.append((myEmailSubject, myEmailMessage, settings.DEFAULT_FROM_EMAIL, list(CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)))

  #also send an email to the originator of the order
  #We do this separately to avoid them seeing the staff cc list
  myMessagesList.append((myEmailSubject, myEmailMessage, settings.DEFAULT_FROM_EMAIL,
          [ theUser.email ]))
  mail.send_mass_mail(tuple(myMessagesList), fail_silently=False)
  return


"""Layer definitions for use in conjunction with open layers"""
WEB_LAYERS = {
            # Streets and boundaries for SA base map with an underlay of spot 2009 2m mosaic
            #
            # Uses the degraded 2.5m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
          'ZaSpot2mMosaic2009TC' : '''var zaSpot2mMosaic2009TC = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2009TC", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2008 mosaic
            #
            # Uses the degraded 2m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
          'ZaSpot2mMosaic2008TC' : '''var zaSpot2mMosaic2008TC = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2008TC", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2007 mosaic
            #
            # Uses the degraded 2m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
          'ZaSpot2mMosaic2007TC' : '''var zaSpot2mMosaic2007TC = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2007TC", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2009 mosaic
            # and under that blue marble. Its rendered as a single layer for best quality.
            'ZaSpot2mMosaic2009' : '''var zaSpot2mMosaic2009 = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2009", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT2009",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
           # Streets and boundaries for SA base map with an underlay of spot 2008 mosaic
           # and under that blue marble. Its rendered as a single layer for best quality.
           'ZaSpot2mMosaic2008' : '''var zaSpot2mMosaic2008 = new OpenLayers.Layer.WMS(
           "ZaSpot2mMosaic2008", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT2008",
           {
              width: '800',
              layers: 'Roads',
              srs: 'EPSG:900913',
              maxResolution: '156543.0339',
              VERSION: '1.1.1',
              EXCEPTIONS: "application/vnd.ogc.se_inimage",
              height: '525',
              format: 'image/jpeg',
              transparent: 'false',
              antialiasing: 'true'
            },
            {isBaseLayer: true});
           ''',
           # Streets and boundaries for SA base map with an underlay of spot 2007 mosaic
           # and under that blue marble. Its rendered as a single layer for best quality.
           'ZaSpot2mMosaic2007' : '''var zaSpot2mMosaic2007 = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2007", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT2007",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2009 mosaic
            #
            # Uses the degraded 10m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
            # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaSpot10mMosaic2009' : '''var zaSpot10mMosaic2009 = new OpenLayers.Layer.WMS(
          "ZaSpot10mMosaic2009", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2008 mosaic
            #
            # Uses the degraded 10 product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
            # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaSpot10mMosaic2008' : '''var zaSpot10mMosaic2008 = new OpenLayers.Layer.WMS(
          "ZaSpot10mMosaic2008", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2007 mosaic
            #
            # Uses the degraded 10 product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
            # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaSpot10mMosaic2007' : '''var zaSpot10mMosaic2007 = new OpenLayers.Layer.WMS(
          "ZaSpot10mMosaic2007", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
           #a Vector only version of the above
           # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaRoadsBoundaries' : '''var zaRoadsBoundaries = new OpenLayers.Layer.WMS(
          "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
           ''',
            # Map of all search footprints that have been made.
            # Transparent: true will make a wms layer into an overlay
            'Searches' : '''var searches = new OpenLayers.Layer.WMS(
          "Searches", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=SEARCHES",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             layers: 'searches',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false});
           ''',
        # Map of site visitors
        # Transparent: true will make a wms layer into an overlay
        'Visitors' : '''var visitors = new OpenLayers.Layer.WMS(
          "Visitors", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=VISITORS",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
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
        ''',
        # Spot5 ZA 2008 10m Mosaic directly from mapserver
            'ZaSpot5Mosaic2008' : '''var zaSpot5Mosaic2008 = new OpenLayers.Layer.WMS( "SPOT5 10m Mosaic 2008, ZA",
            "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT",
            {
              VERSION: '1.1.1',
              EXCEPTIONS: "application/vnd.ogc.se_inimage",
              layers: "Spot5_RSA_2008_10m",
              maxResolution: '156543.0339',
            });
            zaSpot5Mosaic2008.setVisibility(false);
            ''',
        # Nasa Blue marble directly from mapserver
            'BlueMarble' : '''var BlueMarble = new OpenLayers.Layer.WMS( "BlueMarble",
            "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=WORLD",
            {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             layers: "BlueMarble",
             maxResolution: '156543.0339'
            });
            BlueMarble.setVisibility(false);
            ''',
        #
        # Google
        #
       'GooglePhysical' : '''var gphy = new OpenLayers.Layer.Google(
           "Google Physical",
           {type: G_PHYSICAL_MAP}
           );
       ''',
        #
        # Google streets
        #
        'GoogleStreets' : '''var gmap = new OpenLayers.Layer.Google(
           "Google Streets" // the default
           );
        ''',
        #
        # Google hybrid
        #
        'GoogleHybrid' : ''' var ghyb = new OpenLayers.Layer.Google(
           "Google Hybrid",
           {type: G_HYBRID_MAP}
           );
        ''',
        #
        # Google Satellite
        #
        'GoogleSatellite' : '''var gsat = new OpenLayers.Layer.Google(
           "Google Satellite",
           {type: G_SATELLITE_MAP}
           );
        '''
        }

mLayerJs = {'VirtualEarth' : '''<script src='http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6.1'></script>
         ''',
         'Google' : '''
          <script src='http://maps.google.com/maps?file=api&amp;v=2&amp;key='{{GOOGLE_MAPS_API_KEY}}'></script>
          '''}



# Note this code is from Tims personal codebase and copyright is retained
@login_required
def genericAdd(theRequest,
    theFormClass,
    theTitle,
    theRedirectPath,
    theOptions
    ):
  myObject = getObject(theFormClass)
  logging.info('Generic add called')
  if theRequest.method == 'POST':
    # create a form instance using reflection
    # see http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname/452981
    myForm = myObject(theRequest.POST,theRequest.FILES)
    myOptions =  {
            'myForm': myForm,
            'myTitle': theTitle
          }
    myOptions.update(theOptions), #shortcut to join two dicts
    if myForm.is_valid():
      myObject = myForm.save(commit=False)
      myObject.user = theRequest.user
      myObject.save()
      logging.info('Add : data is valid')
      return HttpResponseRedirect(theRedirectPath + str(myObject.id))
    else:
      logging.info('Add : form is NOT valid')
      return render_to_response('add.html',
          myOptions,
          context_instance=RequestContext(theRequest))
  else:
    myForm = myObject()
    myOptions =  {
          'myForm': myForm,
          'myTitle': theTitle
        }
    myOptions.update(theOptions), #shortcut to join two dicts
    logging.info('Add : new object requested')
    return render_to_response('add.html',
        myOptions,
        context_instance=RequestContext(theRequest))

def genericDelete(theRequest,theObject):
  if theObject.user != theRequest.user:
    return ({"myMessage" : "You can only delete an entry that you own!"})
  else:
    theObject.delete()
    return ({'myMessage' : "Entry was deleted successfully"})

def getObject( theClass ):
  #Create an object instance using reflection
  #from http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname/452981
  myParts = theClass.split('.')
  myModule = ".".join(myParts[:-1])
  myObject = __import__( myModule )
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
    logging.debug('Profile does not exist')
  myPartnerFlag = False
  if myProfile and myProfile.strategic_partner:
    myPartnerFlag = True
  return myPartnerFlag


def standardLayers(theRequest):
  """Helper methods used to return standard layer defs for the openlayers control
     Note intended to be published as a view in urls.py
    e.g. usage:
    myLayersList, myLayerDefinitions, myActiveLayer = standardLayers( theRequest )"""

  myProfile = None
  myLayersList = None
  myLayerDefinitions = None
  myActiveBaseMap = None
  try:
    myProfile = theRequest.user.get_profile()
  except:
    logging.debug('Profile does not exist')
  if myProfile and myProfile.strategic_partner:
    myLayerDefinitions = [ WEB_LAYERS['ZaSpot2mMosaic2009TC'], WEB_LAYERS['ZaSpot2mMosaic2008TC'], WEB_LAYERS['ZaSpot2mMosaic2007TC'], WEB_LAYERS['ZaRoadsBoundaries'] ]
    myLayersList = "[ zaSpot2mMosaic2009TC,zaSpot2mMosaic2008TC,zaSpot2mMosaic2007TC,zaRoadsBoundaries ]"
    myActiveBaseMap =  "zaSpot2mMosaic2009TC"
  else:
    myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2009'],WEB_LAYERS['ZaSpot10mMosaic2008'],WEB_LAYERS['ZaSpot10mMosaic2007'],WEB_LAYERS['ZaRoadsBoundaries'] ]
    myLayersList = "[zaSpot10mMosaic2009,zaSpot10mMosaic2008,zaSpot10mMosaic2007,zaRoadsBoundaries]"
    myActiveBaseMap =  "zaSpot10mMosaic2009"
  return myLayersList, myLayerDefinitions, myActiveBaseMap


#render_to_kml helpers
def render_to_kml(theTemplate,theContext,filename):
  response = HttpResponse(render_to_string(theTemplate,theContext))
  response['Content-Type'] = 'application/vnd.google-earth.kml+xml'
  response['Content-Disposition'] = 'attachment; filename=%s.kml' % filename
  return response

def render_to_kmz(theTemplate,theContext,filename):
  response = HttpResponse(render_to_string(theTemplate,theContext))
  kmz = StringIO()
  f = zipfile.ZipFile(kmz, 'w', zipfile.ZIP_DEFLATED)
  f.writestr('%s.kml' % filename, response.content)
  f.close()
  response.content = kmz.getvalue()
  kmz.close()
  response['Content-Type']        = 'application/vnd.google-earth.kmz'
  response['Content-Disposition'] = 'attachment; filename=%s.kmz' % filename
  response['Content-Length']      = str(len(response.content))
  return response

def downloadISOmetadata(theProducts,theName):
  """ returns ZIPed XML metadata files for each product """
  response = HttpResponse()
  myZipData = StringIO()
  myZip = zipfile.ZipFile(myZipData,'w', zipfile.ZIP_DEFLATED)
  for myProduct in theProducts:
    myMetadata = myProduct.product.getISOMetadata()
    myZip.writestr('%s.xml' % myProduct.product.product_id, myMetadata)
  myZip.close()
  response.content=myZipData.getvalue()
  myZipData.close()
  filename = 'SANSA-%s-Metadata.zip' % theName
  response['Content-Type']        = 'application/zip'
  response['Content-Disposition'] = 'attachment; filename=%s' % filename
  response['Content-Length']      = str(len(response.content))
  return response
