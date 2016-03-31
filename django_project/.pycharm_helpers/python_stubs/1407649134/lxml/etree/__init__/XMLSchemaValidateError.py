# encoding: utf-8
# module lxml.etree
# from /usr/local/lib/python2.7/site-packages/lxml/etree.so
# by generator 1.138
"""
The ``lxml.etree`` module implements the extended ElementTree API
for XML.
"""

# imports
import __builtin__ as __builtins__ # <module '__builtin__' (built-in)>

from XMLSchemaError import XMLSchemaError

class XMLSchemaValidateError(XMLSchemaError):
    """ Error while validating an XML document with an XML Schema. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


