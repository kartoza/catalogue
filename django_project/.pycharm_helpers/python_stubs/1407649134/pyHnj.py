# encoding: utf-8
# module pyHnj
# from /usr/local/lib/python2.7/site-packages/pyHnj.so
# by generator 1.138
"""
This is the pyHnj module.  This code is based on the hyphenization
algorithm in Donald Knuth's TeX.  This particular implementation has
been written by Raph Levien (raph@acm.org).

This module provides a single Hyphen class which is a wrapper around
Levien's nice pyHnj library.

Hyphen's constructor takes in, optionally, the name of a prefix text
file.  This module should be distributed with 'hyphen.mashed', which
can process English.

Functions within Hyphen:

    getCodes(word)
    hyphenate(word)
"""
# no imports

# Variables with simple values

error = 'pyHnj.error'

# functions

def Hyphen(*args, **kwargs): # real signature unknown
    """
    name of hyphen dictionary -> instance of Hyphen.
    
    pyHnj needs a source of hyphen prefixes, so we read it here.  If no
    such dictionary exists, or if we cannot read is succesfully, we raise
    pyHnj.Error.
    """
    pass

# no classes
