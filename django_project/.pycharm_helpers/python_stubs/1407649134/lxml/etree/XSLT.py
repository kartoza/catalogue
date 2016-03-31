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

class XSLT(object):
    """
    XSLT(self, xslt_input, extensions=None, regexp=True, access_control=None)
    
        Turn an XSL document into an XSLT object.
    
        Calling this object on a tree or Element will execute the XSLT::
    
          >>> transform = etree.XSLT(xsl_tree)
          >>> result = transform(xml_tree)
    
        Keyword arguments of the constructor:
    
        - extensions: a dict mapping ``(namespace, name)`` pairs to
          extension functions or extension elements
        - regexp: enable exslt regular expression support in XPath
          (default: True)
        - access_control: access restrictions for network or file
          system (see `XSLTAccessControl`)
    
        Keyword arguments of the XSLT call:
    
        - profile_run: enable XSLT profiling (default: False)
    
        Other keyword arguments of the call are passed to the stylesheet
        as parameters.
    """
    def apply(self, _input, profile_run=False, **kw): # real signature unknown; restored from __doc__
        """
        apply(self, _input,  profile_run=False, **kw)
                
                :deprecated: call the object, not this method.
        """
        pass

    @classmethod
    def strparam(cls, strval): # real signature unknown; restored from __doc__
        """
        strparam(strval)
        
                Mark an XSLT string parameter that requires quote escaping
                before passing it into the transformation.  Use it like this::
        
                    result = transform(doc, some_strval = XSLT.strparam(
                        '''it's "Monty Python's" ...'''))
        
                Escaped string parameters can be reused without restriction.
        """
        pass

    def tostring(self, result_tree): # real signature unknown; restored from __doc__
        """
        tostring(self, result_tree)
        
                Save result doc to string based on stylesheet output method.
        
                :deprecated: use str(result_tree) instead.
        """
        pass

    def __call__(self, _input, profile_run=False, **kw): # real signature unknown; restored from __doc__
        """
        __call__(self, _input, profile_run=False, **kw)
        
                Execute the XSL transformation on a tree or Element.
        
                Pass the ``profile_run`` option to get profile information
                about the XSLT.  The result of the XSLT will have a property
                xslt_profile that holds an XML tree with profiling data.
        """
        pass

    def __copy__(self, *args, **kwargs): # real signature unknown
        pass

    def __deepcopy__(self, *args, **kwargs): # real signature unknown
        pass

    def __init__(self, xslt_input, extensions=None, regexp=True, access_control=None): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    error_log = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The log of errors and warnings of an XSLT execution."""


    __pyx_vtable__ = None # (!) real value is ''


