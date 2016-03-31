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

class XMLParser(_FeedParser):
    """
    XMLParser(self, encoding=None, attribute_defaults=False, dtd_validation=False, load_dtd=False, no_network=True, ns_clean=False, recover=False, XMLSchema schema=None, remove_blank_text=False, resolve_entities=True, remove_comments=False, remove_pis=False, strip_cdata=True, target=None, compact=True)
    
        The XML parser.
    
        Parsers can be supplied as additional argument to various parse
        functions of the lxml API.  A default parser is always available
        and can be replaced by a call to the global function
        'set_default_parser'.  New parsers can be created at any time
        without a major run-time overhead.
    
        The keyword arguments in the constructor are mainly based on the
        libxml2 parser configuration.  A DTD will also be loaded if DTD
        validation or attribute default values are requested (unless you
        additionally provide an XMLSchema from which the default
        attributes can be read).
    
        Available boolean keyword arguments:
    
        - attribute_defaults - inject default attributes from DTD or XMLSchema
        - dtd_validation     - validate against a DTD referenced by the document
        - load_dtd           - use DTD for parsing
        - no_network         - prevent network access for related files (default: True)
        - ns_clean           - clean up redundant namespace declarations
        - recover            - try hard to parse through broken XML
        - remove_blank_text  - discard blank text nodes
        - remove_comments    - discard comments
        - remove_pis         - discard processing instructions
        - strip_cdata        - replace CDATA sections by normal text content (default: True)
        - compact            - safe memory for short text content (default: True)
        - resolve_entities   - replace entities by their text value (default: True)
        - huge_tree          - disable security restrictions and support very deep trees
                               and very long text content (only affects libxml2 2.7+)
    
        Other keyword arguments:
    
        - encoding - override the document encoding
        - target   - a parser target object that will receive the parse events
        - schema   - an XMLSchema to validate against
    
        Note that you should avoid sharing parsers between threads.  While this is
        not harmful, it is more efficient to use separate parsers.  This does not
        apply to the default parser.
    """
    def __init__(self, encoding=None, attribute_defaults=False, dtd_validation=False, load_dtd=False, no_network=True, ns_clean=False, recover=False, XMLSchema_schema=None, remove_blank_text=False, resolve_entities=True, remove_comments=False, remove_pis=False, strip_cdata=True, target=None, compact=True): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    __pyx_vtable__ = None # (!) real value is ''


