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

class DocInfo(object):
    """ Document information provided by parser and DTD. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    doctype = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns a DOCTYPE declaration string for the document."""

    encoding = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns the encoding name as declared by the document."""

    externalDTD = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns a DTD validator based on the external subset of the document."""

    internalDTD = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns a DTD validator based on the internal subset of the document."""

    public_id = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns the public ID of the DOCTYPE."""

    root_name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns the name of the root node as defined by the DOCTYPE."""

    standalone = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns the standalone flag as declared by the document.  The possible
        values are True (``standalone='yes'``), False
        (``standalone='no'`` or flag not provided in the declaration),
        and None (unknown or no declaration found).  Note that a
        normal truth test on this value will always tell if the
        ``standalone`` flag was set to ``'yes'`` or not.
        """

    system_url = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns the system ID of the DOCTYPE."""

    URL = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The source URL of the document (or None if unknown)."""

    xml_version = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Returns the XML version as declared by the document."""



