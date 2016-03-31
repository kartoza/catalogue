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

from FallbackElementClassLookup import FallbackElementClassLookup

class ElementNamespaceClassLookup(FallbackElementClassLookup):
    """
    ElementNamespaceClassLookup(self, fallback=None)
    
        Element class lookup scheme that searches the Element class in the
        Namespace registry.
    """
    def get_namespace(self, ns_uri): # real signature unknown; restored from __doc__
        """
        get_namespace(self, ns_uri)
        
                Retrieve the namespace object associated with the given URI.
        
                Creates a new one if it does not yet exist.
        """
        pass

    def __init__(self, fallback=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


