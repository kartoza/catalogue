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

from _Validator import _Validator

class DTD(_Validator):
    """
    DTD(self, file=None, external_id=None)
        A DTD validator.
    
        Can load from filesystem directly given a filename or file-like object.
        Alternatively, pass the keyword parameter ``external_id`` to load from a
        catalog.
    """
    def __call__(self, etree): # real signature unknown; restored from __doc__
        """
        __call__(self, etree)
        
                Validate doc using the DTD.
        
                Returns true if the document is valid, false if not.
        """
        pass

    def __init__(self, file=None, external_id=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


