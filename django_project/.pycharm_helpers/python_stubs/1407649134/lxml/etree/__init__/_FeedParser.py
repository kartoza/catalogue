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

from _BaseParser import _BaseParser

class _FeedParser(_BaseParser):
    # no doc
    def close(self): # real signature unknown; restored from __doc__
        """
        close(self)
        
                Terminates feeding data to this parser.  This tells the parser to
                process any remaining data in the feed buffer, and then returns the
                root Element of the tree that was parsed.
        
                This method must be called after passing the last chunk of data into
                the ``feed()`` method.  It should only be called when using the feed
                parser interface, all other usage is undefined.
        """
        pass

    def feed(self, data): # real signature unknown; restored from __doc__
        """
        feed(self, data)
        
                Feeds data to the parser.  The argument should be an 8-bit string
                buffer containing encoded data, although Unicode is supported as long
                as both string types are not mixed.
        
                This is the main entry point to the consumer interface of a
                parser.  The parser will parse as much of the XML stream as it
                can on each call.  To finish parsing or to reset the parser,
                call the ``close()`` method.  Both methods may raise
                ParseError if errors occur in the input data.  If an error is
                raised, there is no longer a need to call ``close()``.
        
                The feed parser interface is independent of the normal parser
                usage.  You can use the same parser as a feed parser and in
                the ``parse()`` function concurrently.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    feed_error_log = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The error log of the last (or current) run of the feed parser.

        Note that this is local to the feed parser and thus is
        different from what the ``error_log`` property returns.
        """


    __pyx_vtable__ = None # (!) real value is ''


