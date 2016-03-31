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

from _SaxParserTarget import _SaxParserTarget

class TreeBuilder(_SaxParserTarget):
    """
    TreeBuilder(self, element_factory=None, parser=None)
        Parser target that builds a tree.
    
        The final tree is returned by the ``close()`` method.
    """
    def close(self): # real signature unknown; restored from __doc__
        """
        close(self)
        
                Flushes the builder buffers, and returns the toplevel document
                element.
        """
        pass

    def comment(self, comment): # real signature unknown; restored from __doc__
        """ comment(self, comment) """
        pass

    def data(self, data): # real signature unknown; restored from __doc__
        """
        data(self, data)
        
                Adds text to the current element.  The value should be either an
                8-bit string containing ASCII text, or a Unicode string.
        """
        pass

    def end(self, tag): # real signature unknown; restored from __doc__
        """
        end(self, tag)
        
                Closes the current element.
        """
        pass

    def pi(self, target, data): # real signature unknown; restored from __doc__
        """ pi(self, target, data) """
        pass

    def start(self, tag, attrs, nsmap=None): # real signature unknown; restored from __doc__
        """
        start(self, tag, attrs, nsmap=None)
        
                Opens a new element.
        """
        pass

    def __init__(self, element_factory=None, parser=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


