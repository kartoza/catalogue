# encoding: utf-8
# module _renderPM
# from /usr/local/lib/python2.7/site-packages/_renderPM.so
# by generator 1.138
"""
Helper extension module for renderPM.

Interface summary:

	import _render
	gstate(width,height[,depth=3,bg=0xffffff])		#create an initialised graphics state
	makeT1Font(fontName,pfbPath,names[,reader])		#make a T1 font
	delCache()										#delete all font info
	pil2pict(cols,rows,datastr,palette) return PICT version of im as a string
    ft_get_face(fontName) --> ft_face instance

	Error			# module level error
	error			# alias for Error
	_libart_version	# base library version string
	_version		# module version string
"""
# no imports

# Variables with simple values

_libart_version = '2.3.12'

_version = '1.07'

# functions

def delCache(): # real signature unknown; restored from __doc__
    """ delCache() """
    pass

def ft_get_face(fontName): # real signature unknown; restored from __doc__
    """ ft_get_face(fontName) --> ft_face instance """
    pass

def gstate(width, height, depth=3, *args, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
    """ gstate(width,height[,depth=3][,bg=0xffffff]) create an initialised graphics state """
    pass

def makeT1Font(fontName, pfbPath, names): # real signature unknown; restored from __doc__
    """ makeT1Font(fontName,pfbPath,names) """
    pass

def parse_utf8(utf8_string): # real signature unknown; restored from __doc__
    """ parse_utf8(utf8_string) return UCS list """
    pass

def pil2pict(cols, rows, datastr, palette): # real signature unknown; restored from __doc__
    """ pil2pict(cols,rows,datastr,palette) return PICT version of im as a string """
    pass

# classes

class Error(Exception):
    # no doc
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""



