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

from _BaseErrorLog import _BaseErrorLog

class _ListErrorLog(_BaseErrorLog):
    """ Immutable base version of a list based error log. """
    def copy(self, *args, **kwargs): # real signature unknown
        """
        Creates a shallow copy of this error log.  Reuses the list of
                entries.
        """
        pass

    def filter_domains(self, *args, **kwargs): # real signature unknown
        """
        Filter the errors by the given domains and return a new error log
                containing the matches.
        """
        pass

    def filter_from_errors(self): # real signature unknown; restored from __doc__
        """
        filter_from_errors(self)
        
                Convenience method to get all error messages or worse.
        """
        pass

    def filter_from_fatals(self): # real signature unknown; restored from __doc__
        """
        filter_from_fatals(self)
        
                Convenience method to get all fatal error messages.
        """
        pass

    def filter_from_level(self, level): # real signature unknown; restored from __doc__
        """
        filter_from_level(self, level)
        
                Return a log with all messages of the requested level of worse.
        """
        pass

    def filter_from_warnings(self): # real signature unknown; restored from __doc__
        """
        filter_from_warnings(self)
        
                Convenience method to get all warnings or worse.
        """
        pass

    def filter_levels(self, levels): # real signature unknown; restored from __doc__
        """
        filter_levels(self, levels)
        
                Filter the errors by the given error levels and return a new
                error log containing the matches.
        """
        pass

    def filter_types(self, types): # real signature unknown; restored from __doc__
        """
        filter_types(self, types)
        
                Filter the errors by the given types and return a new error
                log containing the matches.
        """
        pass

    def __contains__(self, y): # real signature unknown; restored from __doc__
        """ x.__contains__(y) <==> y in x """
        pass

    def __getitem__(self, y): # real signature unknown; restored from __doc__
        """ x.__getitem__(y) <==> x[y] """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    def __iter__(self): # real signature unknown; restored from __doc__
        """ x.__iter__() <==> iter(x) """
        pass

    def __len__(self): # real signature unknown; restored from __doc__
        """ x.__len__() <==> len(x) """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __nonzero__(self): # real signature unknown; restored from __doc__
        """ x.__nonzero__() <==> x != 0 """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    __pyx_vtable__ = None # (!) real value is ''


