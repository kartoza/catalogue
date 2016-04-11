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

class _Element(object):
    """
    Element class.
    
        References a document object and a libxml node.
    
        By pointing to a Document instance, a reference is kept to
        _Document as long as there is some pointer to a node in it.
    """
    def addnext(self, element): # real signature unknown; restored from __doc__
        """
        addnext(self, element)
        
                Adds the element as a following sibling directly after this
                element.
        
                This is normally used to set a processing instruction or comment after
                the root node of a document.  Note that tail text is automatically
                discarded when adding at the root level.
        """
        pass

    def addprevious(self, element): # real signature unknown; restored from __doc__
        """
        addprevious(self, element)
        
                Adds the element as a preceding sibling directly before this
                element.
        
                This is normally used to set a processing instruction or comment
                before the root node of a document.  Note that tail text is
                automatically discarded when adding at the root level.
        """
        pass

    def append(self, element): # real signature unknown; restored from __doc__
        """
        append(self, element)
        
                Adds a subelement to the end of this element.
        """
        pass

    def clear(self): # real signature unknown; restored from __doc__
        """
        clear(self)
        
                Resets an element.  This function removes all subelements, clears
                all attributes and sets the text and tail properties to None.
        """
        pass

    def extend(self, elements): # real signature unknown; restored from __doc__
        """
        extend(self, elements)
        
                Extends the current children by the elements in the iterable.
        """
        pass

    def find(self, path, namespaces=None): # real signature unknown; restored from __doc__
        """
        find(self, path, namespaces=None)
        
                Finds the first matching subelement, by tag name or path.
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def findall(self, path, namespaces=None): # real signature unknown; restored from __doc__
        """
        findall(self, path, namespaces=None)
        
                Finds all matching subelements, by tag name or path.
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def findtext(self, path, default=None, namespaces=None): # real signature unknown; restored from __doc__
        """
        findtext(self, path, default=None, namespaces=None)
        
                Finds text for the first matching subelement, by tag name or path.
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def get(self, key, default=None): # real signature unknown; restored from __doc__
        """
        get(self, key, default=None)
        
                Gets an element attribute.
        """
        pass

    def getchildren(self): # real signature unknown; restored from __doc__
        """
        getchildren(self)
        
                Returns all direct children.  The elements are returned in document
                order.
        
                :deprecated: Note that this method has been deprecated as of
                  ElementTree 1.3 and lxml 2.0.  New code should use
                  ``list(element)`` or simply iterate over elements.
        """
        pass

    def getiterator(self, tag=None): # real signature unknown; restored from __doc__
        """
        getiterator(self, tag=None)
        
                Returns a sequence or iterator of all elements in the subtree in
                document order (depth first pre-order), starting with this
                element.
        
                Can be restricted to find only elements with a specific tag
                (pass ``tag="xyz"``) or from a namespace (pass ``tag="{ns}*"``).
        
                You can also pass the Element, Comment, ProcessingInstruction and
                Entity factory functions to look only for the specific element type.
        
                :deprecated: Note that this method is deprecated as of
                  ElementTree 1.3 and lxml 2.0.  It returns an iterator in
                  lxml, which diverges from the original ElementTree
                  behaviour.  If you want an efficient iterator, use the
                  ``element.iter()`` method instead.  You should only use this
                  method in new code if you require backwards compatibility
                  with older versions of lxml or ElementTree.
        """
        pass

    def getnext(self): # real signature unknown; restored from __doc__
        """
        getnext(self)
        
                Returns the following sibling of this element or None.
        """
        pass

    def getparent(self): # real signature unknown; restored from __doc__
        """
        getparent(self)
        
                Returns the parent of this element or None for the root element.
        """
        pass

    def getprevious(self): # real signature unknown; restored from __doc__
        """
        getprevious(self)
        
                Returns the preceding sibling of this element or None.
        """
        pass

    def getroottree(self): # real signature unknown; restored from __doc__
        """
        getroottree(self)
        
                Return an ElementTree for the root node of the document that
                contains this element.
        
                This is the same as following element.getparent() up the tree until it
                returns None (for the root element) and then build an ElementTree for
                the last parent that was returned.
        """
        pass

    def index(self, child, start=None, stop=None): # real signature unknown; restored from __doc__
        """
        index(self, child, start=None, stop=None)
        
                Find the position of the child within the parent.
        
                This method is not part of the original ElementTree API.
        """
        pass

    def insert(self, index, element): # real signature unknown; restored from __doc__
        """
        insert(self, index, element)
        
                Inserts a subelement at the given position in this element
        """
        pass

    def items(self): # real signature unknown; restored from __doc__
        """
        items(self)
        
                Gets element attributes, as a sequence. The attributes are returned in
                an arbitrary order.
        """
        pass

    def iter(self, tag=None): # real signature unknown; restored from __doc__
        """
        iter(self, tag=None)
        
                Iterate over all elements in the subtree in document order (depth
                first pre-order), starting with this element.
        
                Can be restricted to find only elements with a specific tag
                (pass ``tag="xyz"``) or from a namespace (pass ``tag="{ns}*"``).
        
                You can also pass the Element, Comment, ProcessingInstruction and
                Entity factory functions to look only for the specific element type.
        """
        pass

    def iterancestors(self, tag=None): # real signature unknown; restored from __doc__
        """
        iterancestors(self, tag=None)
        
                Iterate over the ancestors of this element (from parent to parent).
        
                The generated elements can be restricted to a specific tag name with
                the 'tag' keyword.
        """
        pass

    def iterchildren(self, tag=None, reversed=False): # real signature unknown; restored from __doc__
        """
        iterchildren(self, tag=None, reversed=False)
        
                Iterate over the children of this element.
        
                As opposed to using normal iteration on this element, the generated
                elements can be restricted to a specific tag name with the 'tag'
                keyword and reversed with the 'reversed' keyword.
        """
        pass

    def iterdescendants(self, tag=None): # real signature unknown; restored from __doc__
        """
        iterdescendants(self, tag=None)
        
                Iterate over the descendants of this element in document order.
        
                As opposed to ``el.iter()``, this iterator does not yield the element
                itself.  The generated elements can be restricted to a specific tag
                name with the 'tag' keyword.
        """
        pass

    def iterfind(self, path, namespaces=None): # real signature unknown; restored from __doc__
        """
        iterfind(self, path, namespaces=None)
        
                Iterates over all matching subelements, by tag name or path.
        
                The optional ``namespaces`` argument accepts a
                prefix-to-namespace mapping that allows the usage of XPath
                prefixes in the path expression.
        """
        pass

    def itersiblings(self, tag=None, preceding=False): # real signature unknown; restored from __doc__
        """
        itersiblings(self, tag=None, preceding=False)
        
                Iterate over the following or preceding siblings of this element.
        
                The direction is determined by the 'preceding' keyword which
                defaults to False, i.e. forward iteration over the following
                siblings.  When True, the iterator yields the preceding
                siblings in reverse document order, i.e. starting right before
                the current element and going left.  The generated elements
                can be restricted to a specific tag name with the 'tag'
                keyword.
        """
        pass

    def itertext(self, tag=None, with_tail=True): # real signature unknown; restored from __doc__
        """
        itertext(self, tag=None, with_tail=True)
        
                Iterates over the text content of a subtree.
        
                You can pass the ``tag`` keyword argument to restrict text content to
                a specific tag name.
        
                You can set the ``with_tail`` keyword argument to ``False`` to skip
                over tail text.
        """
        pass

    def keys(self): # real signature unknown; restored from __doc__
        """
        keys(self)
        
                Gets a list of attribute names.  The names are returned in an
                arbitrary order (just like for an ordinary Python dictionary).
        """
        pass

    def makeelement(self, _tag, attrib=None, nsmap=None, **_extra): # real signature unknown; restored from __doc__
        """
        makeelement(self, _tag, attrib=None, nsmap=None, **_extra)
        
                Creates a new element associated with the same document.
        """
        pass

    def remove(self, element): # real signature unknown; restored from __doc__
        """
        remove(self, element)
        
                Removes a matching subelement. Unlike the find methods, this
                method compares elements based on identity, not on tag value
                or contents.
        """
        pass

    def replace(self, old_element, new_element): # real signature unknown; restored from __doc__
        """
        replace(self, old_element, new_element)
        
                Replaces a subelement with the element passed as second argument.
        """
        pass

    def set(self, key, value): # real signature unknown; restored from __doc__
        """
        set(self, key, value)
        
                Sets an element attribute.
        """
        pass

    def values(self): # real signature unknown; restored from __doc__
        """
        values(self)
        
                Gets element attribute values as a sequence of strings.  The
                attributes are returned in an arbitrary order.
        """
        pass

    def xpath(self, _path, namespaces=None, extensions=None, smart_strings=True, **_variables): # real signature unknown; restored from __doc__
        """
        xpath(self, _path, namespaces=None, extensions=None, smart_strings=True, **_variables)
        
                Evaluate an xpath expression using the element as context node.
        """
        pass

    def _init(self): # real signature unknown; restored from __doc__
        """
        _init(self)
        
                Called after object initialisation.  Custom subclasses may override
                this if they recursively call _init() in the superclasses.
        """
        pass

    def __contains__(self, element): # real signature unknown; restored from __doc__
        """ __contains__(self, element) """
        pass

    def __copy__(self): # real signature unknown; restored from __doc__
        """ __copy__(self) """
        pass

    def __deepcopy__(self, memo): # real signature unknown; restored from __doc__
        """ __deepcopy__(self, memo) """
        pass

    def __delitem__(self, x): # real signature unknown; restored from __doc__
        """
        __delitem__(self, x)
        
                Deletes the given subelement or a slice.
        """
        pass

    def __getitem__(self, *args, **kwargs): # real signature unknown
        """
        Returns the subelement at the given position or the requested
                slice.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    def __iter__(self): # real signature unknown; restored from __doc__
        """ __iter__(self) """
        pass

    def __len__(self): # real signature unknown; restored from __doc__
        """
        __len__(self)
        
                Returns the number of subelements.
        """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __nonzero__(self): # real signature unknown; restored from __doc__
        """ x.__nonzero__() <==> x != 0 """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ __repr__(self) """
        pass

    def __reversed__(self): # real signature unknown; restored from __doc__
        """ __reversed__(self) """
        pass

    def __setitem__(self, x, value): # real signature unknown; restored from __doc__
        """
        __setitem__(self, x, value)
        
                Replaces the given subelement index or slice.
        """
        pass

    attrib = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Element attribute dictionary. Where possible, use get(), set(),
        keys(), values() and items() to access element attributes.
        """

    base = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The base URI of the Element (xml:base or HTML base URL).
        None if the base URI is unknown.

        Note that the value depends on the URL of the document that
        holds the Element if there is no xml:base attribute on the
        Element or its ancestors.

        Setting this property will set an xml:base attribute on the
        Element, regardless of the document type (XML or HTML).
        """

    nsmap = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Namespace prefix->URI mapping known in the context of this
        Element.  This includes all namespace declarations of the
        parents.

        Note that changing the returned dict has no effect on the Element.
        """

    prefix = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Namespace prefix or None.
        """

    sourceline = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Original line number as found by the parser or None if unknown.
        """

    tag = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Element tag
        """

    tail = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Text after this element's end tag, but before the next sibling
        element's start tag. This is either a string or the value None, if
        there was no text.
        """

    text = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Text before the first subelement. This is either a string or 
        the value None, if there was no text.
        """



