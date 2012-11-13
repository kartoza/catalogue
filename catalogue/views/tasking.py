"""
SANSA-EO Catalogue - Tasking related views

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

# for error logging
import traceback
import logging
import datetime

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

# Models and forms for our app
from catalogue.renderDecorator import renderWithContext
from catalogue.profileRequiredDecorator import requireProfile

from catalogue.models import (
    TaskingRequest,
    OrderStatusHistory,)
from catalogue.views.helpers import (
    standardLayers,
    notifySalesStaffOfTaskRequest,
    render_to_kml,
    render_to_kmz,)
from catalogue.forms import (
    OrderStatusHistoryForm,
    TaskingRequestForm,
    TaskingRequestDeliveryDetailForm)

# SHP and KML readers
from catalogue.featureReaders import (
    getGeometryFromUploadedFile,)

###########################################################
#
# Tasking related views
#
###########################################################


@login_required
def viewTaskingRequest(theRequest, theId):
    """
    Used to get a detailed view of a single tasking request.
    This view is strictly for staff only or the tasking request owner
    """
    # check if the post ended with /?xhr
    # we do this as well as is_ajax call because we
    # may have arrived at this page via a response redirect
    # which will not then have the is_ajax flag set
    myAjaxFlag = 'xhr' in theRequest.GET
    myTemplatePath = 'taskingRequestPage.html'
    if theRequest.is_ajax() or myAjaxFlag:
        # No page container needed, just a snippet
        myTemplatePath = 'taskingRequestPageAjax.html'
        logging.debug('Request is ajax enabled')
    myTaskingRequest = get_object_or_404(TaskingRequest, id=theId)
    if not (
        (myTaskingRequest.user == theRequest.user) or
            (theRequest.user.is_staff)):
        raise Http404
    myHistory = OrderStatusHistory.objects.all().filter(order=theId)
    myForm = None
    if theRequest.user.is_staff:
        myForm = OrderStatusHistoryForm()
    #render_to_response is done by the renderWithContext decorator
    return render_to_response(myTemplatePath, {
        'myTaskingRequest': myTaskingRequest,
        'myHistory': myHistory,
        'myForm': myForm},
        context_instance=RequestContext(theRequest))


@login_required
def myTaskingRequests(theRequest):
    """
    Used to get an overview listing of tasking requests.
    Non staff users can only see their own orders listed
    """
    myPath = 'taskingRequestPage.html'
    if theRequest.is_ajax():
        # No page container needed, just a snippet
        myPath = 'taskingRequestList.html'
    myRecords = TaskingRequest.objects.filter(
        user=theRequest.user).order_by('-order_date')
    # Paginate the results
    myPaginator = Paginator(myRecords, 10)
    # Make sure page request is an int. If not, deliver first page.
    try:
        myPage = int(theRequest.GET.get('page', '1'))
    except ValueError:
        myPage = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        myRecords = myPaginator.page(myPage)
    except (EmptyPage, InvalidPage):
        myRecords = myPaginator.page(myPaginator.num_pages)
    myUrl = 'mytaskingrequests'
    #render_to_response is done by the renderWithContext decorator
    return render_to_response(myPath, {
        'myRecords': myRecords,
        'myUrl': myUrl},
        context_instance=RequestContext(theRequest))


@login_required
@renderWithContext('taskingRequestListPage.html', 'taskingRequestList.html')
def listTaskingRequests(theRequest):
    myRecords = None
    if not theRequest.user.is_staff:
        """Non staff users can only see their own tasking requests listed"""
        myRecords = TaskingRequest.objects.filter(
            user=theRequest.user).order_by('-order_date')
    else:
        """This view is strictly for staff only"""
        # This view uses the NoSubclassManager
        # base_objects is defined in the model and
        # will exclude all tasking requests or other
        # derived classes
        myRecords = TaskingRequest.objects.all().order_by('-order_date')
    if 'pdf' in theRequest.GET:
        myPageSize = myRecords.count()
    else:
        myPageSize = 100
    # Paginate the results
    try:
        myPage = int(theRequest.GET.get('page', '1'))
    except ValueError:
        myPage = 1
    myPaginator = Paginator(myRecords, myPageSize)
    # If page request (9999) is out of range, deliver last page of results.
    try:
        myRecords = myPaginator.page(myPage)
    except (EmptyPage, InvalidPage):
        myRecords = myPaginator.page(myPaginator.num_pages)
    #render_to_response is done by the renderWithContext decorator
    return ({
        'myRecords': myRecords,
        'myUrl': reverse('listTaskingRequests'),
        'myCurrentMonth': datetime.date.today()
    })


@requireProfile('addtaskingrequest')
@login_required
def addTaskingRequest(theRequest):
    """Used to create a new tasking request"""
    logging.debug(('Post vars:' + str(theRequest.POST)))
    logging.debug(('Post files:' + str(theRequest.FILES)))
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        theRequest)
    logging.debug('Add tasking request called')
    myTitle = 'Create a new tasking request'
    logging.info('Preparing tasking request for user ' + str(theRequest.user))
    myRecords = None
    if str(theRequest.user) == 'AnonymousUser':
        logging.debug('User is anonymous')
        logging.info('Anonymous users can\'t have items in their cart')
        myMessage = (
            'If you want to make a tasking request, you need to create an '
            'account and log in first.')
        return HttpResponse(myMessage)

    if theRequest.method == 'POST':
        logging.debug('Tasking request posted')
        #myForm = TaskingRequestForm( theRequest.POST )
        myTaskingForm = TaskingRequestForm(theRequest.POST)
        myTaskingDeliveryDetailsForm = TaskingRequestDeliveryDetailForm(
            theRequest.POST, theRequest.FILES)
        myOptions = {
            'myTaskingForm': myTaskingForm,
            'myTaskingDeliveryDetailsForm': myTaskingDeliveryDetailsForm,
            'myTitle': myTitle,
            'mySubmitLabel': "Submit Tasking Request",
            'myTaskingRequestFlag': True,
            'myLayerDefinitions': myLayerDefinitions,
            'myLayersList': myLayersList,
        }
        if (myTaskingForm.is_valid() and
                myTaskingDeliveryDetailsForm.is_valid()):
            logging.debug('Tasking Request valid')
            myDeliveryDetailObject = myTaskingDeliveryDetailsForm.save(
                commit=False)
            myDeliveryDetailObject.user = theRequest.user

            myGeometry = None
            try:
                myGeometry = getGeometryFromUploadedFile(
                    theRequest, myTaskingDeliveryDetailsForm, 'geometry_file')
                if myGeometry:
                    myDeliveryDetailObject.geometry = myGeometry
                else:
                    logging.info(
                        'Failed to set tasking request from uploaded geometry '
                        'file')
                    logging.info('Or no shapefile uploaded')
            except:
                logging.info(
                    'An error occurred try to set tasking area from uploaded '
                    'geometry file')
                logging.info(traceback.format_exc())
            if not myDeliveryDetailObject.geometry:
                # myErrors = myTaskingDeliveryDetailsForm._errors.setdefault(
                # "geometry", ErrorList())

                myErrors = myTaskingDeliveryDetailsForm._errors.setdefault(
                    NON_FIELD_ERRORS, ErrorList())
                myErrors.append(u'No valid geometry provided')
                logging.info(
                    'Form is NOT valid - at least a file or digitised geom is '
                    'needed')
                return render_to_response(
                    'addPage.html',
                    myOptions,
                    context_instance=RequestContext(theRequest))

            #save deliverydetailsform
            myDeliveryDetailObject.save()
            #save tasking form
            myObject = myTaskingForm.save(commit=False)
            myObject.user = theRequest.user
            myObject.delivery_detail = myDeliveryDetailObject
            myObject.save()

            logging.debug("Tasking Request saved")
            logging.info('Tasking request : data is valid')
            # Now add the cart contents to the order
            notifySalesStaffOfTaskRequest(myObject.user, myObject.id)
            return HttpResponseRedirect(reverse(
                'viewTaskingRequest', kwargs={'theId': myObject.id}))
        else:
            logging.info('Add Tasking Request : form is NOT valid')
            return render_to_response(
                'addPage.html',
                myOptions,
                context_instance=RequestContext(theRequest))
    else:  # new order
        myTaskingForm = TaskingRequestForm()
        myTaskingDeliveryDetailsForm = TaskingRequestDeliveryDetailForm()
        myOptions = {
            'myTaskingForm': myTaskingForm,
            'myTaskingDeliveryDetailsForm': myTaskingDeliveryDetailsForm,
            'myTitle': myTitle,
            'mySubmitLabel': "Submit Tasking Request",
            'myTaskingRequestFlag': True,
            'myLayerDefinitions': myLayerDefinitions,
            'myLayersList': myLayersList,
        }
        logging.info('Add Tasking Request: new object requested')
        return render_to_response(
            'addPage.html',
            myOptions,
            context_instance=RequestContext(theRequest))


@login_required
def downloadTaskingRequest(theRequest, theId):
    """
    Dispaches request and returns geometry of ordered products in desired file
    format
    """
    myRecord = get_object_or_404(TaskingRequest, id=theId)
    if myRecord.user != theRequest.user and not theRequest.user.is_staff:
        myJscript = """<script>alert('Error: You do not own this request, so
            you cannot download its geometry.</script>"""
        return HttpResponse(myJscript, mimetype='application/javascript')

    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(myRecord)
        myResponder.file_name = u'geometry_for_taskingrequest_%s' % myRecord.id
        return  myResponder.write_request_records([myRecord])
    elif 'kml' in theRequest.GET:
        return render_to_kml('kml/taskingRequest.kml', {
            'tasking_request': myRecord,
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True},
            u'geometry_for_taskingrequest_%s' % myRecord.id)
    elif 'kmz' in theRequest.GET:
        return render_to_kmz('kml/taskingRequest.kml', {
            'tasking_request': myRecord,
            'external_site_url': settings.DOMAIN,
            'transparentStyle': True},
            u'geometry_for_taskingrequest_%s' % myRecord.id)
    else:
        logging.info(
            'Request cannot be proccesed, unsupported download file type')
        raise Http404
