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

class ElementDefaultClassLookup(ElementClassLookup):
    """
    ElementDefaultClassLookup(self, element=None, comment=None, pi=None, entity=None)
        Element class lookup scheme that always returns the default Element
        class.
    
        The keyword arguments ``element``, ``comment``, ``pi`` and ``entity``
        accept the respective Element classes.
    """
    def __init__(self, element=None, comment=None, pi=None, entity=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    comment_class = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    element_class = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    entity_class = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    pi_class = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default



