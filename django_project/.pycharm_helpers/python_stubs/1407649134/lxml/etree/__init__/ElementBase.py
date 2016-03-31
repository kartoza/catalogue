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

from _Element import _Element

class ElementBase(_Element):
    """
    ElementBase(*children, attrib=None, nsmap=None, **_extra)
    
        The public Element class.  All custom Element classes must inherit
        from this one.  To create an Element, use the `Element()` factory.
    
        BIG FAT WARNING: Subclasses *must not* override __init__ or
        __new__ as it is absolutely undefined when these objects will be
        created or destroyed.  All persistent state of Elements must be
        stored in the underlying XML.  If you really need to initialize
        the object after creation, you can implement an ``_init(self)``
        method that will be called directly after object creation.
    
        Subclasses of this class can be instantiated to create a new
        Element.  By default, the tag name will be the class name and the
        namespace will be empty.  You can modify this with the following
        class attributes:
    
        * TAG - the tag name, possibly containing a namespace in Clark
          notation
    
        * NAMESPACE - the default namespace URI, unless provided as part
          of the TAG attribute.
    
        * HTML - flag if the class is an HTML tag, as opposed to an XML
          tag.  This only applies to un-namespaced tags and defaults to
          false (i.e. XML).
    
        * PARSER - the parser that provides the configuration for the
          newly created document.  Providing an HTML parser here will
          default to creating an HTML element.
    
        In user code, the latter three are commonly inherited in class
        hierarchies that implement a common namespace.
    """
    def __init__(self, *children, attrib=None, nsmap=None, **_extra): # real signature unknown; restored from __doc__
        """ ElementBase(*children, attrib=None, nsmap=None, **_extra) """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass


