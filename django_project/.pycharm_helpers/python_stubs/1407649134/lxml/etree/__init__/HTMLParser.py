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

from _FeedParser import _FeedParser

class HTMLParser(_FeedParser):
    """
    HTMLParser(self, encoding=None, remove_blank_text=False,                    remove_comments=False, remove_pis=False, strip_cdata=True,                    no_network=True, target=None, XMLSchema schema=None,                    recover=True, compact=True)
    
        The HTML parser.
    
        This parser allows reading HTML into a normal XML tree.  By
        default, it can read broken (non well-formed) HTML, depending on
        the capabilities of libxml2.  Use the 'recover' option to switch
        this off.
    
        Available boolean keyword arguments:
    
        - recover            - try hard to parse through broken HTML (default: True)
        - no_network         - prevent network access for related files (default: True)
        - remove_blank_text  - discard empty text nodes
        - remove_comments    - discard comments
        - remove_pis         - discard processing instructions
        - strip_cdata        - replace CDATA sections by normal text content (default: True)
        - compact            - safe memory for short text content (default: True)
    
        Other keyword arguments:
    
        - encoding - override the document encoding
        - target   - a parser target object that will receive the parse events
        - schema   - an XMLSchema to validate against
    
        Note that you should avoid sharing parsers between threads for performance
        reasons.
    """
    def __init__(self, encoding=None, remove_blank_text=False, remove_comments=False, remove_pis=False, strip_cdata=True, no_network=True, target=None, XMLSchema_schema=None, recover=True, compact=True): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


