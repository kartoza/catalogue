# encoding: utf-8
# module mercurial.parsers
# from /usr/local/lib/python2.7/site-packages/mercurial/parsers.so
# by generator 1.138
""" Efficient content parsing. """
# no imports

# functions

def encodedir(*args, **kwargs): # real signature unknown
    """ encodedir a path """
    pass

def lowerencode(*args, **kwargs): # real signature unknown
    """ lower-encode a path """
    pass

def pack_dirstate(*args, **kwargs): # real signature unknown
    """ pack a dirstate """
    pass

def parse_dirstate(*args, **kwargs): # real signature unknown
    """ parse a dirstate """
    pass

def parse_index2(*args, **kwargs): # real signature unknown
    """ parse a revlog index """
    pass

def parse_manifest(*args, **kwargs): # real signature unknown
    """ parse a manifest """
    pass

def pathencode(*args, **kwargs): # real signature unknown
    """ fncache-encode a path """
    pass

# classes

class dirs(object):
    """ dirs """
    def addpath(self, *args, **kwargs): # real signature unknown
        """ add a path """
        pass

    def delpath(self, *args, **kwargs): # real signature unknown
        """ remove a path """
        pass

    def __contains__(self, y): # real signature unknown; restored from __doc__
        """ x.__contains__(y) <==> y in x """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    def __iter__(self): # real signature unknown; restored from __doc__
        """ x.__iter__() <==> iter(x) """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass


class index(object):
    """ revlog index """
    def ancestors(self, *args, **kwargs): # real signature unknown
        """ return the gca set of the given revs """
        pass

    def clearcaches(self, *args, **kwargs): # real signature unknown
        """ clear the index caches """
        pass

    def get(self, *args, **kwargs): # real signature unknown
        """ get an index entry """
        pass

    def headrevs(self, *args, **kwargs): # real signature unknown
        """ get head revisions """
        pass

    def insert(self, *args, **kwargs): # real signature unknown
        """ insert an index entry """
        pass

    def partialmatch(self, *args, **kwargs): # real signature unknown
        """ match a potentially ambiguous node ID """
        pass

    def stats(self, *args, **kwargs): # real signature unknown
        """ stats for the index """
        pass

    def __contains__(self, y): # real signature unknown; restored from __doc__
        """ x.__contains__(y) <==> y in x """
        pass

    def __delitem__(self, y): # real signature unknown; restored from __doc__
        """ x.__delitem__(y) <==> del x[y] """
        pass

    def __getitem__(self, y): # real signature unknown; restored from __doc__
        """ x.__getitem__(y) <==> x[y] """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    def __len__(self): # real signature unknown; restored from __doc__
        """ x.__len__() <==> len(x) """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __setitem__(self, i, y): # real signature unknown; restored from __doc__
        """ x.__setitem__(i, y) <==> x[i]=y """
        pass

    nodemap = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """nodemap"""



