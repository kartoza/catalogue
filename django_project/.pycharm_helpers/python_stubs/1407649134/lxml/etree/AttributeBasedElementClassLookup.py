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

class AttributeBasedElementClassLookup(FallbackElementClassLookup):
    """
    AttributeBasedElementClassLookup(self, attribute_name, class_mapping, fallback=None)
        Checks an attribute of an Element and looks up the value in a
        class dictionary.
    
        Arguments:
          - attribute name - '{ns}name' style string
          - class mapping  - Python dict mapping attribute values to Element classes
          - fallback       - optional fallback lookup mechanism
    
        A None key in the class mapping will be checked if the attribute is
        missing.
    """
    def __init__(self, attribute_name, class_mapping, fallback=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


