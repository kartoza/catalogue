# encoding: utf-8
# module hgext.inotify.linux._inotify
# from /usr/local/lib/python2.7/site-packages/hgext/inotify/linux/_inotify.so
# by generator 1.138
""" Low-level inotify interface wrappers. """
# no imports

# Variables with simple values

IN_ACCESS = 1

IN_ALL_EVENTS = 4095

IN_ATTRIB = 4
IN_CLOSE = 24

IN_CLOSE_NOWRITE = 16
IN_CLOSE_WRITE = 8

IN_CREATE = 256
IN_DELETE = 512

IN_DELETE_SELF = 1024

IN_DONT_FOLLOW = 33554432

IN_IGNORED = 32768
IN_ISDIR = 1073741824

IN_MASK_ADD = 536870912

IN_MODIFY = 2
IN_MOVE = 192

IN_MOVED_FROM = 64
IN_MOVED_TO = 128

IN_MOVE_SELF = 2048

IN_ONESHOT = 2147483648
IN_ONLYDIR = 16777216
IN_OPEN = 32

IN_Q_OVERFLOW = 16384

IN_UNMOUNT = 8192

# functions

def add_watch(fd, path, mask): # real signature unknown; restored from __doc__
    """
    add_watch(fd, path, mask) -> wd
    
    Add a watch to an inotify instance, or modify an existing watch.
    
            fd: file descriptor returned by init()
            path: path to watch
            mask: mask of events to watch for
    
    Return a unique numeric watch descriptor for the inotify instance
    mapped by the file descriptor.
    """
    pass

def decode_mask(mask): # real signature unknown; restored from __doc__
    """
    decode_mask(mask) -> list_of_strings
    
    Decode an inotify mask value into a list of strings that give the
    name of each bit set in the mask.
    """
    pass

def init(): # real signature unknown; restored from __doc__
    """
    init() -> fd
    
    Initialize an inotify instance.
    Return a file descriptor associated with a new inotify event queue.
    """
    pass

def read(fd, bufsize, *args, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__ 
    """
    read(fd, bufsize[=65536]) -> list_of_events
    
    
    Read inotify events from a file descriptor.
    
            fd: file descriptor returned by init()
            bufsize: size of buffer to read into, in bytes
    
    Return a list of event objects.
    
    If bufsize is > 0, block until events are available to be read.
    Otherwise, immediately return all events that can be read without
    blocking.
    """
    pass

def remove_watch(fd, wd): # real signature unknown; restored from __doc__
    """
    remove_watch(fd, wd)
    
            fd: file descriptor returned by init()
            wd: watch descriptor returned by add_watch()
    
    Remove a watch associated with the watch descriptor wd from the
    inotify instance associated with the file descriptor fd.
    
    Removing a watch causes an IN_IGNORED event to be generated for this
    watch descriptor.
    """
    pass

# no classes
