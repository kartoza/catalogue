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

class PythonElementClassLookup(FallbackElementClassLookup):
    """
    PythonElementClassLookup(self, fallback=None)
        Element class lookup based on a subclass method.
    
        This class lookup scheme allows access to the entire XML tree in
        read-only mode.  To use it, re-implement the ``lookup(self, doc,
        root)`` method in a subclass::
    
            >>> from lxml import etree, pyclasslookup
            >>>
            >>> class MyElementClass(etree.ElementBase):
            ...     honkey = True
            ...
            >>> class MyLookup(pyclasslookup.PythonElementClassLookup):
            ...     def lookup(self, doc, root):
            ...         if root.tag == "sometag":
            ...             return MyElementClass
            ...         else:
            ...             for child in root:
            ...                 if child.tag == "someothertag":
            ...                     return MyElementClass
            ...         # delegate to default
            ...         return None
    
        If you return None from this method, the fallback will be called.
    
        The first argument is the opaque document instance that contains
        the Element.  The second argument is a lightweight Element proxy
        implementation that is only valid during the lookup.  Do not try
        to keep a reference to it.  Once the lookup is done, the proxy
        will be invalid.
    
        Also, you cannot wrap such a read-only Element in an ElementTree,
        and you must take care not to keep a reference to them outside of
        the `lookup()` method.
    
        Note that the API of the Element objects is not complete.  It is
        purely read-only and does not support all features of the normal
        `lxml.etree` API (such as XPath, extended slicing or some
        iteration methods).
    
        See http://codespeak.net/lxml/element_classes.html
    """
    def lookup(self, doc, element): # real signature unknown; restored from __doc__
        """
        lookup(self, doc, element)
        
                Override this method to implement your own lookup scheme.
        """
        pass

    def __init__(self, fallback=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


