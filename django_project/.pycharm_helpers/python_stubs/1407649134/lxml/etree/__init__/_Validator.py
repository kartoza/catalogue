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

class _Validator(object):
    """ Base class for XML validators. """
    def assertValid(self, etree): # real signature unknown; restored from __doc__
        """
        assertValid(self, etree)
        
                Raises `DocumentInvalid` if the document does not comply with the schema.
        """
        pass

    def assert_(self, etree): # real signature unknown; restored from __doc__
        """
        assert_(self, etree)
        
                Raises `AssertionError` if the document does not comply with the schema.
        """
        pass

    def validate(self, etree): # real signature unknown; restored from __doc__
        """
        validate(self, etree)
        
                Validate the document using this schema.
        
                Returns true if document is valid, false if not.
        """
        pass

    def _append_log_message(self, *args, **kwargs): # real signature unknown
        pass

    def _clear_error_log(self, *args, **kwargs): # real signature unknown
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    error_log = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The log of validation errors and warnings."""


    __pyx_vtable__ = None # (!) real value is ''


