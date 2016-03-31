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

class _LogEntry(object):
    """
    A log message entry from an error log.
    
        Attributes:
    
        - message: the message text
        - domain: the domain ID (see lxml.etree.ErrorDomains)
        - type: the message type ID (see lxml.etree.ErrorTypes)
        - level: the log level ID (see lxml.etree.ErrorLevels)
        - line: the line at which the message originated (if applicable)
        - column: the character column at which the message originated (if applicable)
        - filename: the name of the file in which the message originated (if applicable)
    """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    column = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    domain = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    domain_name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The name of the error domain.  See lxml.etree.ErrorDomains
        """

    filename = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    level = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    level_name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The name of the error level.  See lxml.etree.ErrorLevels
        """

    line = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    message = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    type = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    type_name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The name of the error type.  See lxml.etree.ErrorTypes
        """


    __pyx_vtable__ = None # (!) real value is ''


