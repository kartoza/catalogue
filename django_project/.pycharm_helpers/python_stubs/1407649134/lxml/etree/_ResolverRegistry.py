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

class _ResolverRegistry(object):
    # no doc
    def add(self, resolver): # real signature unknown; restored from __doc__
        """
        add(self, resolver)
        
                Register a resolver.
        
                For each requested entity, the 'resolve' method of the resolver will
                be called and the result will be passed to the parser.  If this method
                returns None, the request will be delegated to other resolvers or the
                default resolver.  The resolvers will be tested in an arbitrary order
                until the first match is found.
        """
        pass

    def copy(self): # real signature unknown; restored from __doc__
        """ copy(self) """
        pass

    def remove(self, resolver): # real signature unknown; restored from __doc__
        """ remove(self, resolver) """
        pass

    def resolve(self, system_url, public_id, context): # real signature unknown; restored from __doc__
        """ resolve(self, system_url, public_id, context) """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    __pyx_vtable__ = None # (!) real value is ''


