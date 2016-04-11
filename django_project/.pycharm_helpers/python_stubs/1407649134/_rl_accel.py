# encoding: utf-8
# module _rl_accel
# from /usr/local/lib/python2.7/site-packages/_rl_accel.so
# by generator 1.138
"""
_rl_accel contains various accelerated utilities

	escapePDF makes a string safe for PDF
	_instanceEscapePDF method equivalent of escapePDF

	_AsciiBase85Encode does what is says
	_AsciiBase85Decode does what is says

	fp_str converts numeric arguments to a single blank separated string
	calcChecksum calculate checksums for TTFs (legacy)
	calcChecksumL calculate checksums for TTFs (returns long)
	add32 32 bit unsigned addition (legacy)
	add32L 32 bit unsigned addition (returns long)
	hex32 32 bit unsigned to 0X8.8X string
	_instanceStringWidthU version2 Font instance stringWidth
	_instanceStringWidthTTF version2 TTFont instance stringWidth
	unicode2T1 version2 pdfmetrics.unicode2T1
	_reset() version2 clears _rl_accel state
	Box(width,character=None) creates a Knuth character Box with the specified width.
	Glue(width,stretch,shrink) creates a Knuth glue Box with the specified width, stretch and shrink.
	Penalty(width,penalty,flagged=0) creates a Knuth penalty Box with the specified width and penalty.
	BoxList() creates a knuth box list.
"""
# no imports

# Variables with simple values

version = '0.63'

# functions

def add32(x, y): # real signature unknown; restored from __doc__
    """ add32(x,y)  32 bit unsigned x+y (legacy) """
    pass

def add32L(x, y): # real signature unknown; restored from __doc__
    """ add32L(x,y)  32 bit unsigned x+y (returns long) """
    pass

def Box(width, character=None): # real signature unknown; restored from __doc__
    """ Box(width,character=None) create a Knuth Box instance """
    pass

def calcChecksum(string): # real signature unknown; restored from __doc__
    """ calcChecksum(string) calculate checksums for TTFs (legacy) """
    pass

def calcChecksumL(string): # real signature unknown; restored from __doc__
    """ calcChecksumL(string) calculate checksums for TTFs (returns long) """
    pass

def escapePDF(s): # real signature unknown; restored from __doc__
    """ escapePDF(s) return PDF safed string """
    pass

def fp_str(a0, a1, *more): # real signature unknown; restored from __doc__
    """ fp_str(a0, a1,...) convert numerics to blank separated string """
    pass

def Glue(width, stretch, shrink): # real signature unknown; restored from __doc__
    """ Glue(width,stretch,shrink) create a Knuth Glue instance """
    pass

def hex32(x): # real signature unknown; restored from __doc__
    """ hex32(x)  32 bit unsigned-->0X8.8X string """
    pass

def Penalty(width, penalty, flagged=0): # real signature unknown; restored from __doc__
    """ Penalty(width,penalty,flagged=0) create a Knuth Penalty instance """
    pass

def unicode2T1(*args, **kwargs): # real signature unknown
    """ return a list of (font,string) pairs representing the unicode text """
    pass

def _AsciiBase85Decode(*args, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
    """ _AsciiBase85Decode(".....") return decoded string """
    pass

def _AsciiBase85Encode(*args, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
    """ _AsciiBase85Encode(".....") return encoded string """
    pass

def _instanceEscapePDF(s): # real signature unknown; restored from __doc__
    """ _instanceEscapePDF(s) return PDF safed string """
    pass

def _instanceStringWidthTTF(*args, **kwargs): # real signature unknown
    """ TTFont.stringWidth(self,text,fontName,fontSize,encoding='utf8') --> width """
    pass

def _instanceStringWidthU(*args, **kwargs): # real signature unknown
    """ Font.stringWidth(self,text,fontName,fontSize,encoding='utf8') --> width """
    pass

def _reset(): # real signature unknown; restored from __doc__
    """ _rl_accel._reset() reset _rl_accel state """
    pass

def _sameFrag(f, g): # real signature unknown; restored from __doc__
    """ _sameFrag(f,g) return 1 if fragments have same style """
    pass

# classes

class BoxList(list):
    # no doc
    @classmethod
    def classmeth(cls, *args, **kw): # real signature unknown; restored from __doc__
        """ classmeth(*args, **kw) """
        pass

    def getstate(self): # real signature unknown; restored from __doc__
        """ getstate() -> state """
        pass

    def setstate(self, state): # real signature unknown; restored from __doc__
        """ setstate(state) """
        pass

    def staticmeth(self, *args, **kw): # real signature unknown; restored from __doc__
        """ staticmeth(*args, **kw) """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    state = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """an int variable for demonstration purposes"""



class error(Exception):
    # no doc
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""



