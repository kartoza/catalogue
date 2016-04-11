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

from _XPathEvaluatorBase import _XPathEvaluatorBase

class XPath(_XPathEvaluatorBase):
    """
    XPath(self, path, namespaces=None, extensions=None, regexp=True, smart_strings=True)
        A compiled XPath expression that can be called on Elements and ElementTrees.
    
        Besides the XPath expression, you can pass prefix-namespace
        mappings and extension functions to the constructor through the
        keyword arguments ``namespaces`` and ``extensions``.  EXSLT
        regular expression support can be disabled with the 'regexp'
        boolean keyword (defaults to True).  Smart strings will be
        returned for string results unless you pass
        ``smart_strings=False``.
    """
    def __call__(self, _etree_or_element, **_variables): # real signature unknown; restored from __doc__
        """ __call__(self, _etree_or_element, **_variables) """
        pass

    def __init__(self, path, namespaces=None, extensions=None, regexp=True, smart_strings=True): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    path = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The literal XPath expression.
        """


    __pyx_vtable__ = None # (!) real value is ''


