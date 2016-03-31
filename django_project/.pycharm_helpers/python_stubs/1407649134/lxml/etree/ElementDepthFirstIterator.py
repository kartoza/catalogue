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

from _ElementTagMatcher import _ElementTagMatcher

class ElementDepthFirstIterator(_ElementTagMatcher):
    """
    ElementDepthFirstIterator(self, node, tag=None, inclusive=True)
        Iterates over an element and its sub-elements in document order (depth
        first pre-order).
    
        Note that this also includes comments, entities and processing
        instructions.  To filter them out, check if the ``tag`` property
        of the returned element is a string (i.e. not None and not a
        factory function), or pass the ``Element`` factory for the ``tag``
        keyword.
    
        If the optional ``tag`` argument is not None, the iterator returns only
        the elements that match the respective name and namespace.
    
        The optional boolean argument 'inclusive' defaults to True and can be set
        to False to exclude the start element itself.
    
        Note that the behaviour of this iterator is completely undefined if the
        tree it traverses is modified during iteration.
    """
    def next(self): # real signature unknown; restored from __doc__
        """ x.next() -> the next value, or raise StopIteration """
        pass

    def __init__(self, node, tag=None, inclusive=True): # real signature unknown; restored from __doc__
        pass

    def __iter__(self): # real signature unknown; restored from __doc__
        """ x.__iter__() <==> iter(x) """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __next__(self, *args, **kwargs): # real signature unknown
        pass

    __pyx_vtable__ = None # (!) real value is ''


