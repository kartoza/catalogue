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

class RelaxNG(_Validator):
    """
    RelaxNG(self, etree=None, file=None)
        Turn a document into a Relax NG validator.
    
        Either pass a schema as Element or ElementTree, or pass a file or
        filename through the ``file`` keyword argument.
    """
    def __call__(self, etree): # real signature unknown; restored from __doc__
        """
        __call__(self, etree)
        
                Validate doc using Relax NG.
        
                Returns true if document is valid, false if not.
        """
        pass

    def __init__(self, etree=None, file=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


