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

class Resolver(object):
    """ This is the base class of all resolvers. """
    def resolve(self, system_url, public_id, context): # real signature unknown; restored from __doc__
        """
        resolve(self, system_url, public_id, context)
        
                Override this method to resolve an external source by
                ``system_url`` and ``public_id``.  The third argument is an
                opaque context object.
        
                Return the result of one of the ``resolve_*()`` methods.
        """
        pass

    def resolve_empty(self, context): # real signature unknown; restored from __doc__
        """
        resolve_empty(self, context)
        
                Return an empty input document.
        
                Pass context as parameter.
        """
        pass

    def resolve_file(self, f, context, base_url=None): # real signature unknown; restored from __doc__
        """
        resolve_file(self, f, context, base_url=None)
        
                Return an open file-like object as input document.
        
                Pass open file and context as parameters.  You can pass the
                base URL or filename of the file through the ``base_url``
                keyword argument.
        
                Note that using ``.resolve_filename()`` is more efficient,
                especially in threaded environments.
        """
        pass

    def resolve_filename(self, filename, context): # real signature unknown; restored from __doc__
        """
        resolve_filename(self, filename, context)
        
                Return the name of a parsable file as input document.
        
                Pass filename and context as parameters.  You can also pass a
                URL with an HTTP, FTP or file target.
        """
        pass

    def resolve_string(self, string, context, base_url=None): # real signature unknown; restored from __doc__
        """
        resolve_string(self, string, context, base_url=None)
        
                Return a parsable string as input document.
        
                Pass data string and context as parameters.  You can pass the
                source URL or filename through the ``base_url`` keyword
                argument.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass


