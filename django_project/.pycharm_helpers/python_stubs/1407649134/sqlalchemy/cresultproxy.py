# encoding: utf-8
# module sqlalchemy.cresultproxy
# from /usr/local/lib/python2.7/site-packages/sqlalchemy/cresultproxy.so
# by generator 1.138
""" Module containing C versions of core ResultProxy classes. """
# no imports

# functions

def safe_rowproxy_reconstructor(*args, **kwargs): # real signature unknown
    """ reconstruct a RowProxy instance from its pickled form. """
    pass

# classes

class BaseRowProxy(object):
    """ BaseRowProxy is a abstract base class for RowProxy """
    def values(self, *args, **kwargs): # real signature unknown
        """ Return the values represented by this BaseRowProxy as a list. """
        pass

    def __getattribute__(self, name): # real signature unknown; restored from __doc__
        """ x.__getattribute__('name') <==> x.name """
        pass

    def __getitem__(self, y): # real signature unknown; restored from __doc__
        """ x.__getitem__(y) <==> x[y] """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    def __iter__(self): # real signature unknown; restored from __doc__
        """ x.__iter__() <==> iter(x) """
        pass

    def __len__(self): # real signature unknown; restored from __doc__
        """ x.__len__() <==> len(x) """
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __reduce__(self, *args, **kwargs): # real signature unknown
        """ Pickle support method. """
        pass

    _keymap = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Key to (processor, index) dict"""

    _parent = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """ResultMetaData"""

    _processors = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of type processors"""

    _row = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Original row tuple"""



