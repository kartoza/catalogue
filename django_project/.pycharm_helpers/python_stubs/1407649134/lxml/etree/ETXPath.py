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

from XPath import XPath

class ETXPath(XPath):
    """
    ETXPath(self, path, extensions=None, regexp=True, smart_strings=True)
        Special XPath class that supports the ElementTree {uri} notation for namespaces.
    
        Note that this class does not accept the ``namespace`` keyword
        argument. All namespaces must be passed as part of the path
        string.  Smart strings will be returned for string results unless
        you pass ``smart_strings=False``.
    """
    def __init__(self, path, extensions=None, regexp=True, smart_strings=True): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


