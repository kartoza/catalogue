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

from ElementClassLookup import ElementClassLookup

class FallbackElementClassLookup(ElementClassLookup):
    """
    FallbackElementClassLookup(self, fallback=None)
    
        Superclass of Element class lookups with additional fallback.
    """
    def set_fallback(self, lookup): # real signature unknown; restored from __doc__
        """
        set_fallback(self, lookup)
        
                Sets the fallback scheme for this lookup method.
        """
        pass

    def __init__(self, fallback=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    fallback = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default


    __pyx_vtable__ = None # (!) real value is ''


