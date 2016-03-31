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

class PyErrorLog(_BaseErrorLog):
    """
    PyErrorLog(self, logger_name=None, logger=None)
        A global error log that connects to the Python stdlib logging package.
    
        The constructor accepts an optional logger name or a readily
        instantiated logger instance.
    
        If you want to change the mapping between libxml2's ErrorLevels and Python
        logging levels, you can modify the level_map dictionary from a subclass.
    
        The default mapping is::
    
                ErrorLevels.WARNING = logging.WARNING
                ErrorLevels.ERROR   = logging.ERROR
                ErrorLevels.FATAL   = logging.CRITICAL
    
        You can also override the method ``receive()`` that takes a LogEntry
        object and calls ``self.log(log_entry, format_string, arg1, arg2, ...)``
        with appropriate data.
    """
    def copy(self, *args, **kwargs): # real signature unknown
        """ Dummy method that returns an empty error log. """
        pass

    def log(self, log_entry, message, *args): # real signature unknown; restored from __doc__
        """
        log(self, log_entry, message, *args)
        
                Called by the .receive() method to log a _LogEntry instance to
                the Python logging system.  This handles the error level
                mapping.
        
                In the default implementation, the ``message`` argument
                receives a complete log line, and there are no further
                ``args``.  To change the message format, it is best to
                override the .receive() method instead of this one.
        """
        pass

    def receive(self, log_entry): # real signature unknown; restored from __doc__
        """
        receive(self, log_entry)
        
                Receive a _LogEntry instance from the logging system.  Calls
                the .log() method with appropriate parameters::
        
                    self.log(log_entry, repr(log_entry))
        
                You can override this method to provide your own log output
                format.
        """
        pass

    def __init__(self, logger_name=None, logger=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    level_map = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default


    __pyx_vtable__ = None # (!) real value is ''


