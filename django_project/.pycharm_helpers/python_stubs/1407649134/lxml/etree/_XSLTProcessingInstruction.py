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

from PIBase import PIBase

class _XSLTProcessingInstruction(PIBase):
    # no doc
    def get(self, key, default=None): # real signature unknown; restored from __doc__
        """
        get(self, key, default=None)
        
                Parses a pseudo attribute from the text of the processing instruction.
        """
        pass

    def parseXSL(self, parser=None): # real signature unknown; restored from __doc__
        """
        parseXSL(self, parser=None)
        
                Try to parse the stylesheet referenced by this PI and return
                an ElementTree for it.  If the stylesheet is embedded in the
                same document (referenced via xml:id), find and return an
                ElementTree for the stylesheet Element.
        
                The optional ``parser`` keyword argument can be passed to specify the
                parser used to read from external stylesheet URLs.
        """
        pass

    def set(self, key, value): # real signature unknown; restored from __doc__
        """
        set(self, key, value)
        
                Sets a pseudo attribute in the text of the processing instruction.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


