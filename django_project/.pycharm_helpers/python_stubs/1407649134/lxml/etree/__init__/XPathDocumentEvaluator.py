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

from XPathElementEvaluator import XPathElementEvaluator

class XPathDocumentEvaluator(XPathElementEvaluator):
    """
    XPathDocumentEvaluator(self, etree, namespaces=None, extensions=None, regexp=True, smart_strings=True)
        Create an XPath evaluator for an ElementTree.
    
        Additional namespace declarations can be passed with the
        'namespace' keyword argument.  EXSLT regular expression support
        can be disabled with the 'regexp' boolean keyword (defaults to
        True).  Smart strings will be returned for string results unless
        you pass ``smart_strings=False``.
    """
    def __call__(self, _path, **_variables): # real signature unknown; restored from __doc__
        """
        __call__(self, _path, **_variables)
        
                Evaluate an XPath expression on the document.
        
                Variables may be provided as keyword arguments.  Note that namespaces
                are currently not supported for variables.
        """
        pass

    def __init__(self, etree, namespaces=None, extensions=None, regexp=True, smart_strings=True): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


