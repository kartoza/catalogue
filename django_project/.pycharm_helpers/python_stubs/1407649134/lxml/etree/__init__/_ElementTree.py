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

class _ElementTree(object):
    # no doc
    def find(self, path, namespaces=None): # real signature unknown; restored from __doc__
        """
        find(self, path, namespaces=None)
        
                Finds the first toplevel element with given tag.  Same as
                ``tree.getroot().find(path)``.
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def findall(self, path, namespaces=None): # real signature unknown; restored from __doc__
        """
        findall(self, path, namespaces=None)
        
                Finds all elements matching the ElementPath expression.  Same as
                getroot().findall(path).
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def findtext(self, path, default=None, namespaces=None): # real signature unknown; restored from __doc__
        """
        findtext(self, path, default=None, namespaces=None)
        
                Finds the text for the first element matching the ElementPath
                expression.  Same as getroot().findtext(path)
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def getiterator(self, tag=None): # real signature unknown; restored from __doc__
        """
        getiterator(self, tag=None)
        
                Returns a sequence or iterator of all elements in document order
                (depth first pre-order), starting with the root element.
        
                Can be restricted to find only elements with a specific tag
                (pass ``tag="xyz"`` or ``tag="{ns}xyz"``) or from a namespace
                (pass ``tag="{ns}*"``).
        
                You can also pass the Element, Comment, ProcessingInstruction and
                Entity factory functions to look only for the specific element type.
        
                :deprecated: Note that this method is deprecated as of
                  ElementTree 1.3 and lxml 2.0.  It returns an iterator in
                  lxml, which diverges from the original ElementTree
                  behaviour.  If you want an efficient iterator, use the
                  ``tree.iter()`` method instead.  You should only use this
                  method in new code if you require backwards compatibility
                  with older versions of lxml or ElementTree.
        """
        pass

    def getpath(self, element): # real signature unknown; restored from __doc__
        """
        getpath(self, element)
        
                Returns a structural, absolute XPath expression to find that element.
        """
        pass

    def getroot(self): # real signature unknown; restored from __doc__
        """
        getroot(self)
        
                Gets the root element for this tree.
        """
        pass

    def iter(self, tag=None): # real signature unknown; restored from __doc__
        """
        iter(self, tag=None)
        
                Creates an iterator for the root element.  The iterator loops over
                all elements in this tree, in document order.
        """
        pass

    def iterfind(self, path, namespaces=None): # real signature unknown; restored from __doc__
        """
        iterfind(self, path, namespaces=None)
        
                Iterates over all elements matching the ElementPath expression.
                Same as getroot().iterfind(path).
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def parse(self, source, parser=None, base_url=None): # real signature unknown; restored from __doc__
        """
        parse(self, source, parser=None, base_url=None)
        
                Updates self with the content of source and returns its root
        """
        pass

    def relaxng(self, relaxng): # real signature unknown; restored from __doc__
        """
        relaxng(self, relaxng)
        
                Validate this document using other document.
        
                The relaxng argument is a tree that should contain a Relax NG schema.
        
                Returns True or False, depending on whether validation
                succeeded.
        
                Note: if you are going to apply the same Relax NG schema against
                multiple documents, it is more efficient to use the RelaxNG
                class directly.
        """
        pass

    def write(self, file, encoding=None, method="xml", pretty_print=False, xml_declaration=None, with_tail=True, standalone=None, compression=0, exclusive=False, with_comments=True): # real signature unknown; restored from __doc__
        """
        write(self, file, encoding=None, method="xml",
                          pretty_print=False, xml_declaration=None, with_tail=True,
                          standalone=None, compression=0,
                          exclusive=False, with_comments=True)
        
                Write the tree to a filename, file or file-like object.
        
                Defaults to ASCII encoding and writing a declaration as needed.
        
                The keyword argument 'method' selects the output method:
                'xml', 'html', 'text' or 'c14n'.  Default is 'xml'.
        
                The ``exclusive`` and ``with_comments`` arguments are only
                used with C14N output, where they request exclusive and
                uncommented C14N serialisation respectively.
        
                Passing a boolean value to the ``standalone`` option will
                output an XML declaration with the corresponding
                ``standalone`` flag.
        
                The ``compression`` option enables GZip compression level 1-9.
        """
        pass

    def write_c14n(self, file, exclusive=False, with_comments=True, compression=0): # real signature unknown; restored from __doc__
        """
        write_c14n(self, file, exclusive=False, with_comments=True,
                               compression=0)
        
                C14N write of document. Always writes UTF-8.
        
                The ``compression`` option enables GZip compression level 1-9.
        """
        pass

    def xinclude(self): # real signature unknown; restored from __doc__
        """
        xinclude(self)
        
                Process the XInclude nodes in this document and include the
                referenced XML fragments.
        
                There is support for loading files through the file system, HTTP and
                FTP.
        
                Note that XInclude does not support custom resolvers in Python space
                due to restrictions of libxml2 <= 2.6.29.
        """
        pass

    def xmlschema(self, xmlschema): # real signature unknown; restored from __doc__
        """
        xmlschema(self, xmlschema)
        
                Validate this document using other document.
        
                The xmlschema argument is a tree that should contain an XML Schema.
        
                Returns True or False, depending on whether validation
                succeeded.
        
                Note: If you are going to apply the same XML Schema against
                multiple documents, it is more efficient to use the XMLSchema
                class directly.
        """
        pass

    def xpath(self, _path, namespaces=None, extensions=None, smart_strings=True, **_variables): # real signature unknown; restored from __doc__
        """
        xpath(self, _path, namespaces=None, extensions=None, smart_strings=True, **_variables)
        
                XPath evaluate in context of document.
        
                ``namespaces`` is an optional dictionary with prefix to namespace URI
                mappings, used by XPath.  ``extensions`` defines additional extension
                functions.
                
                Returns a list (nodeset), or bool, float or string.
        
                In case of a list result, return Element for element nodes,
                string for text and attribute values.
        
                Note: if you are going to apply multiple XPath expressions
                against the same document, it is more efficient to use
                XPathEvaluator directly.
        """
        pass

    def xslt(self, _xslt, extensions=None, access_control=None, **_kw): # real signature unknown; restored from __doc__
        """
        xslt(self, _xslt, extensions=None, access_control=None, **_kw)
        
                Transform this document using other document.
        
                xslt is a tree that should be XSLT
                keyword parameters are XSLT transformation parameters.
        
                Returns the transformed tree.
        
                Note: if you are going to apply the same XSLT stylesheet against
                multiple documents, it is more efficient to use the XSLT
                class directly.
        """
        pass

    def _setroot(self, root): # real signature unknown; restored from __doc__
        """
        _setroot(self, root)
        
                Relocate the ElementTree to a new root node.
        """
        pass

    def __copy__(self, *args, **kwargs): # real signature unknown
        pass

    def __deepcopy__(self, *args, **kwargs): # real signature unknown
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    docinfo = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Information about the document provided by parser and DTD.  This
        value is only defined for ElementTree objects based on the root node
        of a parsed document (e.g.  those returned by the parse functions),
        not for trees that were built manually.
        """

    parser = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The parser that was used to parse the document in this ElementTree.
        """


    __pyx_vtable__ = None # (!) real value is ''


