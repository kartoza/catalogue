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

from _ReadOnlyElementProxy import _ReadOnlyElementProxy

class _AppendOnlyElementProxy(_ReadOnlyElementProxy):
    """
    A read-only element that allows adding children and changing the
        text content (i.e. everything that adds to the subtree).
    """
    def append(self, *args, **kwargs): # real signature unknown
        """ Append a copy of an Element to the list of children. """
        pass

    def extend(self, *args, **kwargs): # real signature unknown
        """
        Append a copy of all Elements from a sequence to the list of
                children.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    text = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Text before the first subelement. This is either a string or the
        value None, if there was no text.
        """


    __pyx_vtable__ = None # (!) real value is ''


