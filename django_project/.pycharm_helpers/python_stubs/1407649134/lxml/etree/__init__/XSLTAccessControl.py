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

class XSLTAccessControl(object):
    """
    XSLTAccessControl(self, read_file=True, write_file=True, create_dir=True, read_network=True, write_network=True)
    
        Access control for XSLT: reading/writing files, directories and
        network I/O.  Access to a type of resource is granted or denied by
        passing any of the following boolean keyword arguments.  All of
        them default to True to allow access.
    
        - read_file
        - write_file
        - create_dir
        - read_network
        - write_network
    
        For convenience, there is also a class member `DENY_ALL` that
        provides an XSLTAccessControl instance that is readily configured
        to deny everything, and a `DENY_WRITE` member that denies all
        write access but allows read access.
    
        See `XSLT`.
    """
    def __init__(self, read_file=True, write_file=True, create_dir=True, read_network=True, write_network=True): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    options = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The access control configuration as a map of options."""


    DENY_ALL = None # (!) real value is ''
    DENY_WRITE = None # (!) real value is ''
    __pyx_vtable__ = None # (!) real value is ''


