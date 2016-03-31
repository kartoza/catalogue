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

from object import object

class CDATA(object):
    """
    CDATA(data)
    
        CDATA factory.  This factory creates an opaque data object that
        can be used to set Element text.  The usual way to use it is::
    
            >>> from lxml import etree
            >>> el = etree.Element('content')
            >>> el.text = etree.CDATA('a string')
    """
    def __init__(self, data): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass


