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

class _XPathEvaluatorBase(object):
    # no doc
    def evaluate(self, _eval_arg, **_variables): # real signature unknown; restored from __doc__
        """
        evaluate(self, _eval_arg, **_variables)
        
                Evaluate an XPath expression.
        
                Instead of calling this method, you can also call the evaluator object
                itself.
        
                Variables may be provided as keyword arguments.  Note that namespaces
                are currently not supported for variables.
        
                :deprecated: call the object, not its method.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    error_log = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default


    __pyx_vtable__ = None # (!) real value is ''


