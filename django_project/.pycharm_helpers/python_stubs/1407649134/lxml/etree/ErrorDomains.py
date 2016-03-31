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

from object import object

class ErrorDomains(object):
    """ Libxml2 error domains """
    def _getName(self, *args, **kwargs): # real signature unknown
        """ D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None. """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""


    C14N = 21
    CATALOG = 20
    CHECK = 24
    DATATYPE = 15
    DTD = 4
    FTP = 9
    HTML = 5
    HTTP = 10
    I18N = 27
    IO = 8
    MEMORY = 6
    MODULE = 26
    NAMESPACE = 3
    NONE = 0
    OUTPUT = 7
    PARSER = 1
    REGEXP = 14
    RELAXNGP = 18
    RELAXNGV = 19
    SCHEMASP = 16
    SCHEMASV = 17
    SCHEMATRONV = 28
    TREE = 2
    VALID = 23
    WRITER = 25
    XINCLUDE = 11
    XPATH = 12
    XPOINTER = 13
    XSLT = 22
    _names = {
        0: u'NONE',
        1: u'PARSER',
        2: u'TREE',
        3: u'NAMESPACE',
        4: u'DTD',
        5: u'HTML',
        6: u'MEMORY',
        7: u'OUTPUT',
        8: u'IO',
        9: u'FTP',
        10: u'HTTP',
        11: u'XINCLUDE',
        12: u'XPATH',
        13: u'XPOINTER',
        14: u'REGEXP',
        15: u'DATATYPE',
        16: u'SCHEMASP',
        17: u'SCHEMASV',
        18: u'RELAXNGP',
        19: u'RELAXNGV',
        20: u'CATALOG',
        21: u'C14N',
        22: u'XSLT',
        23: u'VALID',
        24: u'CHECK',
        25: u'WRITER',
        26: u'MODULE',
        27: u'I18N',
        28: u'SCHEMATRONV',
    }
    __dict__ = None # (!) real value is ''


