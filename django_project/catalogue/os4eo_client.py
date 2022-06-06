"""
SANSA-EO Catalogue - OS4EO Client implementation

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


from django.conf import settings

from elementsoap.ElementSOAP import (
    SoapService, SoapElement, SoapRequest)


OS4EO_SERVICE_ENDPOINT = getattr(
    settings, 'OS4EO_SERVICE_ENDPOINT', 'http://196.35.94.243/os4eo')


class OS4EOClient(SoapService):
    """
    OS4EO Client implementation
    This lib is not Django dependent except for OS4EO_SERVICE_ENDPOINT settings

    Note: SoapFault exception is raised in case of errors
    Note: uses a custom elementsoap library with enhanced debug capabilities
    """
    url = OS4EO_SERVICE_ENDPOINT

    def __init__(self, debug=False):
        self.debug = debug
        SoapService.__init__(self)

    def GetCapabilities(self):
        """
        This is the first implemented method, it was written just to test if
        the approach could be successful
        """
        action = 'GetCapabilities'
        request = SoapRequest(
            '{http://earth.esa.int/hma/ordering}GetCapabilities')
        request.set('service', 'OS')
        response = self.call(action, request, debug=self.debug)
        return response.findall('*/{http://www.opengis.net/ows}Operation')

    def Submit(self, dims_id_list, order_reference):
        """
        Place an order, returns orderId and order status
        """
        action = 'Submit'
        request = SoapRequest('{http://earth.esa.int/hma/ordering}Submit')
        request.set('service', 'OS')
        request.set('version', "0.9.4")

        orderSpecification = SoapElement(
            request, '{http://earth.esa.int/hma/ordering}orderSpecification')
        statusNotification = SoapElement(
            request, '{http://earth.esa.int/hma/ordering}statusNotification',
            None, 'None')

        orderReference = SoapElement(
            orderSpecification,
            '{http://earth.esa.int/hma/ordering}orderReference',
            None, order_reference)
        orderType = SoapElement(
            orderSpecification,
            '{http://earth.esa.int/hma/ordering}orderType',
            None, 'PRODUCT_ORDER')

        i = 1
        for dims_id in dims_id_list:
            orderItem = SoapElement(
                orderSpecification,
                '{http://earth.esa.int/hma/ordering}orderItem')
            productId = SoapElement(
                orderItem,
                '{http://earth.esa.int/hma/ordering}productId')
            productOrderOptionsId = SoapElement(
                orderItem,
                '{http://earth.esa.int/hma/ordering}productOrderOptionsId',
                None, 'None')
            SoapElement(
                orderItem,
                '{http://earth.esa.int/hma/ordering}deliveryMethod',
                None, 'ftp')
            SoapElement(
                orderItem,
                '{http://earth.esa.int/hma/ordering}packageMedium',
                None, 'file')
            SoapElement(
                orderItem,
                '{http://earth.esa.int/hma/ordering}numberOfCopies',
                None, '1')
            SoapElement(
                orderItem,
                '{http://earth.esa.int/hma/ordering}itemId',
                None, str(i).rjust(4, '0'))
            identifier = SoapElement(
                productId,
                '{http://earth.esa.int/hma/ordering}identifier',
                None, dims_id)
            identifier.set('codeSpace', 'urn:EOP:SAC:EOWEB')
            i = i + 1

        response = self.call(action, request, debug=self.debug)

        return (
            response.find('.//{http://earth.esa.int/hma/ordering}orderId')
            .text,
            response.find('.//{http://earth.esa.int/hma/ordering}status')
            .text)

    def GetStatus(self, orderId, full=False):
        """
        Return the order status (and the orderStatusInfo status if full is set
        and order is completed).

        Presentation can be 'brief' or 'full'
        """
        action = 'Submit'
        request = SoapRequest('{http://earth.esa.int/hma/ordering}GetStatus')
        request.set('service', 'OS')
        request.set('version', '0.9.4')

        SoapElement(
            request,
            '{http://earth.esa.int/hma/ordering}orderId', None, orderId)
        if full:
            presentation = 'full'
        else:
            presentation = 'brief'
        SoapElement(
            request,
            '{http://earth.esa.int/hma/ordering}presentation',
            None, presentation)
        response = self.call(action, request, debug=self.debug)
        if full:
            status = response.find(
                './/{http://earth.esa.int/hma/ordering}orderStatusInfo/{http:'
                '//earth.esa.int/hma/ordering}status').text
            if status == 'Completed':
                return status, response.find(
                    './/{http://earth.esa.int/hma/ordering}additionalStatus'
                    'Info').text
            else:
                return status
        else:
            return response.find(
                './/{http://earth.esa.int/hma/ordering}orderStatusInfo/{http:'
                '//earth.esa.int/hma/ordering}status').text

    def DescribeResultAccess(self, orderId):
        """
        Return the order Result Status
        """
        action = 'Submit'
        request = SoapRequest(
            '{http://earth.esa.int/hma/ordering}DescribeResultAccess')
        request.set('service', 'OS')
        request.set('version', '0.9.4')

        SoapElement(
            request, '{http://earth.esa.int/hma/ordering}orderId',
            None, orderId)
        SoapElement(
            request, '{http://earth.esa.int/hma/ordering}subFunction',
            None, 'allReady')
        response = self.call(action, request, debug=self.debug)
        status = response.find(
            './/{http://earth.esa.int/hma/ordering}status').text
        if status == 'failure':
            return status
        return status, response.find(
            './/{http://earth.esa.int/hma/ordering}URL').text
