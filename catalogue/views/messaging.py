"""
SANSA-EO Catalogue -  Messaging

Contact : tim@linfiniti.com

.. note:: This program is the property of South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '17/08/2012'
__copyright__ = 'South African National Space Agency'

import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import (HttpResponseBadRequest,
                         HttpResponse)

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from offline_messages.models import OfflineMessage
from offline_messages.utils import create_offline_message, constants

from catalogue.forms import AllUsersMessageForm, MessageForm


@staff_member_required
def sendMessageToUser(theRequest):
    """Submit a message to a user via django-offline-messages.

    Args:
        theRequest - a POST request containing
            * user_id - the user id of the person to receive the message
            * message - the contents of the message to be sent to the user.
    Returns:
        HttpResponse: An html snippet indicating the message was successfully
            submitted
    """
    logging.debug('sendMessageToUser called.')
    # Should not need these two lines due to decorator
    if not theRequest.user.is_staff:
        return HttpResponseBadRequest('You are not permitted to do this.')
    if theRequest.method == 'POST':
        myForm = MessageForm(theRequest.POST)
        if myForm.is_valid():
            if not 'message' in theRequest.POST:
                return HttpResponseBadRequest(
                    'Message is missing from POST request')
            try:
                myMessage = theRequest.POST['message']
                myUserId = theRequest.POST['user_id']
                myUser = User.objects.get(id=myUserId)
                create_offline_message(myUser, myMessage, level=constants.INFO)
                logging.debug('Offline message created:\n%s' % myMessage)
                return HttpResponse('Message sent successfully to %s.' %
                                    myUser)
            except:
                myMessage = ('Message sending failed. '
                             'Please check the logs and try again.')
                logging.exception(myMessage)
                return HttpResponse(myMessage)
        else:
            # Otherwise the form is not valid so redisplay it
            # with validation messages
            # form.as_p() means 'render the form within html
            #paragraph elements'
            return render_to_response(
                'messageForm.html',
                {
                    'myForm': myForm
                },
                context_instance=RequestContext(theRequest)
            )
    else:
        # No post so make a new empty form
        myForm = MessageForm()
        # Show the form in the users browser
        return render_to_response(
            'messageForm.html',
            {
                'myForm': myForm
            },
            context_instance=RequestContext(theRequest)
        )


def sendMessageToAllUsers(theRequest):
    """
    Submit a message to all users via django-offline-messages. This view
    expects the message to be called with a POST request containing
    message - the contents of the message to be sent to the user.
    @return An html snippet indicating the message was successfully submitted
    """
    if not theRequest.user.is_staff:
        return HttpResponseBadRequest('You are not permitted to do this.')
    if theRequest.method == 'POST':
        #import pdb; pdb.set_trace()
        myForm = AllUsersMessageForm(theRequest.POST)
        if myForm.is_valid():
            if 'message' not in theRequest.POST:
                return HttpResponseBadRequest(
                    'Message is missing from POST request')
            try:
                myMessage = theRequest.POST['message']
                # Iterate through users
                for myUser in User.objects.all():
                    myNotifiedAlreadyFlag = OfflineMessage.objects.filter(
                        user=myUser, message=myMessage).exists()
                    if not myNotifiedAlreadyFlag:
                        create_offline_message(
                            myUser, myMessage, level=constants.INFO)
                return HttpResponse('Message sent successfully to all users.')
            except:
                myMessage = ('Message sending failed. '
                             'Please check the logs and try again.')
                logging.exception(myMessage)
                return HttpResponse(myMessage)
        else:
            # Otherwise the form is not valid so redisplay it with
            # validation messages form.as_p() means 'render the form
            # within html paragraph elements'
            return render_to_response(
                'messageForm.html',
                {
                    'myForm': myForm
                },
                context_instance=RequestContext(theRequest)
            )
    else:
        # No post so make a new empty form
        myForm = AllUsersMessageForm()
        # Show the form in the users browser
        return render_to_response(
            'messageForm.html',
            {
                'myForm': myForm
            },
            context_instance=RequestContext(theRequest)
        )


def userMessages(theRequest):
    '''
    Return any messages pending for the current logged in user.
    @see https://docs.djangoproject.com/en/dev/ref/contrib/messages/
    @note login_required should not be set otherwise anonymous
          users will see spurious popups.
    '''
    logging.debug('User messages requested')
    if theRequest.user.is_anonymous():
        return HttpResponse('')

    myMessages = OfflineMessage.objects.filter(user=theRequest.user)
    myResponse = render_to_response(
        'messages.html',
        {
            'messages': myMessages
        },
        context_instance=RequestContext(theRequest))
    for myMessage in myMessages:
        myMessage.delete()

    return myResponse
