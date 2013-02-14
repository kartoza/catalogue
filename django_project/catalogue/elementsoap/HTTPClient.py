#
# ElementSOAP
# $Id: HTTPClient.py 2924 2006-11-19 22:24:22Z fredrik $
#
# a simple XML-over-HTTP client
#
# for more information, see:
#
#     http://effbot.org/zone/http-xml.htm
#
# history:
# 2002-07-12 fl   created
# 2002-07-14 fl   added to the xmltoys library
# 2002-07-17 fl   changed constructor to take a full URI
# 2003-05-13 fl   added parser argument
# 2003-11-16 fl   added HTTPError exception
# 2006-11-19 fl   added HTTPS support (based on a patch by Florent Aide).
# 2006-11-19 fl   use parser as callable, not parser class
#
# Copyright (c) 1999-2006 by Fredrik Lundh.  All rights reserved.
#
# fredrik@pythonware.com
# http://www.pythonware.com
#
# --------------------------------------------------------------------
# The ElementSOAP library is
#
# Copyright (c) 1999-2006 by Fredrik Lundh
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------

##
# This module implements a simple XML-over-HTTP transport layer.
##

from httplib import HTTP, HTTPS
import StringIO
import urlparse


##
# HTTP exception.  This exception contains the error code, the error
# message, an HTTP header dictionary, and a file handle, in that
# order.  The file handle can be used to read the error response.
from django_project.catalogue.elementsoap import ElementTree as ET


class HTTPError(Exception):
    pass

##
# HTTP client class.
#
# @param url Target URL.

class HTTPClient:

    user_agent = "HTTPClient.py (from effbot.org)"

    def __init__(self, url):

        scheme, host, path, params, query, fragment = urlparse.urlparse(url)
        if scheme != "http" and scheme != "https":
            raise ValueError("unsupported scheme (%s)" % scheme)

        self.host = host
        self.scheme = scheme

        if not path:
            path = "/"
        if params:
            path = path + ";" + params
        if query:
            path = path + "?" + query

        self.path = path

    ##
    # Issues an HTTP request.
    #
    # @param body Request body (a string or an ElementTree object).
    # @keyparam path Optional path.  If omitted, the path is derived
    #    from the host URL.
    # @keyparam method Optional HTTP method.  The default is POST.
    # @keyparam content_type Optional Content-Type setting.  The
    #    default is <b>text/xml</b>.
    # @keyparam extra_headers List of additional HTTP header fields.
    #    The list should contain (field, value)-tuples.
    # @keyparam parser Optional parser function.  If omitted, the
    #    standard ElementTree <b>parse</b> function is used.
    # @return An ElementTree instance containing the HTTP response.
    # @defreturn ElementTree
    # @throws HTTPError If the server returned an HTTP error code.
    #    The error code and other details can be obtained from the
    #    exception object.

    def do_request(self, body,
                   path=None,
                   method="POST",
                   content_type="text/xml",
                   extra_headers=None,
                   parser=None,
                   debug=False):

        if path is None:
            # use default path from constructor
            path = self.path

        if isinstance(body, ET.ElementTree):
            # serialize element tree
            file = StringIO.StringIO()
            body.write(file)
            body = file.getvalue()

        # send request
        if self.scheme == "https":
            h = HTTPS(self.host)
        else:
            h = HTTP(self.host)

        h.putrequest(method, path)
        h.putheader("User-Agent", self.user_agent)
        h.putheader("Host", self.host)
        h.putheader("Content-Type", content_type)
        h.putheader("Content-Length", str(len(body)))
        if extra_headers:
            for key, value in extra_headers:
                h.putheader(key, value)
        h.endheaders()

        h.send(body)


        # fetch the reply
        errcode, errmsg, headers = h.getreply()

        handle = h.getfile()

        if debug:
            print '-' * 50
            print '>\n'.join(body.split('>'))
            print '-' * 50
            print errcode, errmsg, headers
            print '-' * 50
            response_xml = handle.readlines()[0]
            handle = StringIO.StringIO(response_xml)
            print '>\n'.join(response_xml.split('>'))
            print '-' * 50

        if errcode != 200:
            raise HTTPError(errcode, errmsg, headers, handle)


        if parser:
            return parser(handle)

        return ET.parse(handle)
