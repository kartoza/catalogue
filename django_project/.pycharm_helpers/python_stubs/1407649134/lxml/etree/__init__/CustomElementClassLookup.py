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

class CustomElementClassLookup(FallbackElementClassLookup):
    """
    CustomElementClassLookup(self, fallback=None)
        Element class lookup based on a subclass method.
    
        You can inherit from this class and override the method::
    
            lookup(self, type, doc, namespace, name)
    
        to lookup the element class for a node. Arguments of the method:
        * type:      one of 'element', 'comment', 'PI', 'entity'
        * doc:       document that the node is in
        * namespace: namespace URI of the node (or None for comments/PIs/entities)
        * name:      name of the element/entity, None for comments, target for PIs
    
        If you return None from this method, the fallback will be called.
    """
    def lookup(self, type, doc, namespace, name): # real signature unknown; restored from __doc__
        """ lookup(self, type, doc, namespace, name) """
        pass

    def __init__(self, fallback=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


