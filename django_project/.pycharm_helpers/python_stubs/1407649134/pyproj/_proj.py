# encoding: utf-8
# module pyproj._proj
# from /usr/local/lib/python2.7/site-packages/pyproj/_proj.so
# by generator 1.138
# no doc

# imports
import __builtin__ as __builtins__ # <module '__builtin__' (built-in)>
import math as math # /usr/local/lib/python2.7/lib-dynload/math.so

# Variables with simple values

_doublesize = 8

__version__ = '1.9.3'

# functions

def set_datapath(*args, **kwargs): # real signature unknown
    pass

def _transform(*args, **kwargs): # real signature unknown
    pass

# classes

class Geod(object):
    # no doc
    def _fwd(self, *args, **kwargs): # real signature unknown
        """
        forward transformation - determine longitude, latitude and back azimuth 
         of a terminus point given an initial point longitude and latitude, plus
         forward azimuth and distance.
         if radians=True, lons/lats are radians instead of degrees.
        """
        pass

    def _inv(self, *args, **kwargs): # real signature unknown
        """
        inverse transformation - return forward and back azimuths, plus distance
         between an initial and terminus lat/lon pair.
         if radians=True, lons/lats are radians instead of degrees.
        """
        pass

    def _npts(self, *args, **kwargs): # real signature unknown
        """ given initial and terminus lat/lon, find npts intermediate points. """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __reduce__(self, *args, **kwargs): # real signature unknown
        """ special method that allows pyproj.Geod instance to be pickled """
        pass

    initstring = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default



class Proj(object):
    # no doc
    def is_geocent(self, *args, **kwargs): # real signature unknown
        pass

    def is_latlong(self, *args, **kwargs): # real signature unknown
        pass

    def _fwd(self, *args, **kwargs): # real signature unknown
        """
        forward transformation - lons,lats to x,y (done in place).
         if radians=True, lons/lats are radians instead of degrees.
         if errcheck=True, an exception is raised if the forward transformation is invalid.
         if errcheck=False and the forward transformation is invalid, no exception is
         raised and 1.e30 is returned.
        """
        pass

    def _inv(self, *args, **kwargs): # real signature unknown
        """
        inverse transformation - x,y to lons,lats (done in place).
         if radians=True, lons/lats are radians instead of degrees.
         if errcheck=True, an exception is raised if the inverse transformation is invalid.
         if errcheck=False and the inverse transformation is invalid, no exception is
         raised and 1.e30 is returned.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __reduce__(self, *args, **kwargs): # real signature unknown
        """ special method that allows pyproj.Proj instance to be pickled """
        pass

    proj_version = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    srs = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default



# variables with complex values

__test__ = {}

