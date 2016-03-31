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

class _ReadOnlyProxy(object):
    """ A read-only proxy class suitable for PIs/Comments (for internal use only!). """
    def getchildren(self, *args, **kwargs): # real signature unknown
        """
        Returns all subelements. The elements are returned in document
                order.
        """
        pass

    def getnext(self, *args, **kwargs): # real signature unknown
        """ Returns the following sibling of this element or None. """
        pass

    def getparent(self, *args, **kwargs): # real signature unknown
        """ Returns the parent of this element or None for the root element. """
        pass

    def getprevious(self, *args, **kwargs): # real signature unknown
        """ Returns the preceding sibling of this element or None. """
        pass

    def iterchildren(self, tag=None, reversed=False): # real signature unknown; restored from __doc__
        """
        iterchildren(self, tag=None, reversed=False)
        
                Iterate over the children of this element.
        """
        pass

    def __copy__(self): # real signature unknown; restored from __doc__
        """ __copy__(self) """
        pass

    def __deepcopy__(self, memo): # real signature unknown; restored from __doc__
        """ __deepcopy__(self, memo) """
        pass

    def __getitem__(self, *args, **kwargs): # real signature unknown
        """
        Returns the subelement at the given position or the requested
                slice.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    def __iter__(self): # real signature unknown; restored from __doc__
        """ x.__iter__() <==> iter(x) """
        pass

    def __len__(self, *args, **kwargs): # real signature unknown
        """ Returns the number of subelements. """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __nonzero__(self): # real signature unknown; restored from __doc__
        """ x.__nonzero__() <==> x != 0 """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    sourceline = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Original line number as found by the parser or None if unknown.
        """

    tag = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Element tag
        """

    tail = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Text after this element's end tag, but before the next sibling
        element's start tag. This is either a string or the value None, if
        there was no text.
        """

    text = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Text before the first subelement. This is either a string or 
        the value None, if there was no text.
        """


    __pyx_vtable__ = None # (!) real value is ''


