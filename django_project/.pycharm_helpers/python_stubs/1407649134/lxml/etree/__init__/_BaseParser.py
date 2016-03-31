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

class _BaseParser(object):
    # no doc
    def copy(self): # real signature unknown; restored from __doc__
        """
        copy(self)
        
                Create a new parser with the same configuration.
        """
        pass

    def makeelement(self, _tag, attrib=None, nsmap=None, **_extra): # real signature unknown; restored from __doc__
        """
        makeelement(self, _tag, attrib=None, nsmap=None, **_extra)
        
                Creates a new element associated with this parser.
        """
        pass

    def setElementClassLookup(self, *args, **kwargs): # real signature unknown
        """ :deprecated: use ``parser.set_element_class_lookup(lookup)`` instead. """
        pass

    def set_element_class_lookup(self, lookup=None): # real signature unknown; restored from __doc__
        """
        set_element_class_lookup(self, lookup = None)
        
                Set a lookup scheme for element classes generated from this parser.
        
                Reset it by passing None or nothing.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    error_log = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The error log of the last parser run.
        """

    resolvers = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The custom resolver registry of this parser."""

    target = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    version = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The version of the underlying XML parser."""


    __pyx_vtable__ = None # (!) real value is ''


