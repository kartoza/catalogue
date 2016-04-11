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

from _Comment import _Comment

class CommentBase(_Comment):
    """
    All custom Comment classes must inherit from this one.
    
        To create an XML Comment instance, use the ``Comment()`` factory.
    
        Subclasses *must not* override __init__ or __new__ as it is
        absolutely undefined when these objects will be created or
        destroyed.  All persistent state of Comments must be stored in the
        underlying XML.  If you really need to initialize the object after
        creation, you can implement an ``_init(self)`` method that will be
        called after object creation.
    """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


