# encoding: utf-8
# module psycopg2._psycopg
# from /usr/local/lib/python2.7/site-packages/psycopg2/_psycopg.so
# by generator 1.138
""" psycopg PostgreSQL driver """

# imports
import psycopg2 as __psycopg2


# Variables with simple values

apilevel = '2.0'

paramstyle = 'pyformat'

threadsafety = 2

__version__ = '2.2.2 (dt dec ext pq3)'

# functions

def adapt(obj, protocol, alternate): # real signature unknown; restored from __doc__
    """ adapt(obj, protocol, alternate) -> object -- adapt obj to given protocol """
    return object()

def AsIs(obj): # real signature unknown; restored from __doc__
    """ AsIs(obj) -> new AsIs wrapper object """
    pass

def Binary(buffer): # real signature unknown; restored from __doc__
    """
    Binary(buffer) -> new binary object
    
    Build an object capable to hold a bynary string value.
    """
    pass

def BINARY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def BINARYARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def Boolean(*args, **kwargs): # real signature unknown
    """ Float(obj) -> new float value """
    pass

def BOOLEAN(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def BOOLEANARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def connect(dsn, *more): # real signature unknown; restored from __doc__
    """
    connect(dsn, ...) -- Create a new database connection.
    
    This function supports two different but equivalent sets of arguments.
    A single data source name or ``dsn`` string can be used to specify the
    connection parameters, as follows::
    
        psycopg2.connect("dbname=xxx user=xxx ...")
    
    If ``dsn`` is not provided it is possible to pass the parameters as
    keyword arguments; e.g.::
    
        psycopg2.connect(database='xxx', user='xxx', ...)
    
    The full list of available parameters is:
    
    - ``dbname`` -- database name (only in 'dsn')
    - ``database`` -- database name (only as keyword argument)
    - ``host`` -- host address (defaults to UNIX socket if not provided)
    - ``port`` -- port number (defaults to 5432 if not provided)
    - ``user`` -- user name used to authenticate
    - ``password`` -- password used to authenticate
    - ``sslmode`` -- SSL mode (see PostgreSQL documentation)
    
    - ``async`` -- if the connection should provide asynchronous API
    
    If the ``connection_factory`` keyword argument is not provided this
    function always return an instance of the `connection` class.
    Else the given sub-class of `extensions.connection` will be used to
    instantiate the connection object.
    
    :return: New database connection
    :rtype: `extensions.connection`
    """
    pass

def DATE(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def Date(year, month, day): # real signature unknown; restored from __doc__
    """
    Date(year, month, day) -> new date
    
    Build an object holding a date value.
    """
    pass

def DATEARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def DateFromPy(datetime_date): # real signature unknown; restored from __doc__
    """ DateFromPy(datetime.date) -> new wrapper """
    pass

def DateFromTicks(ticks): # real signature unknown; restored from __doc__
    """
    DateFromTicks(ticks) -> new date
    
    Build an object holding a date value from the given ticks value.
    
    Ticks are the number of seconds since the epoch; see the documentation of the standard Python time module for details).
    """
    pass

def DATETIME(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def DATETIMEARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def DECIMAL(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def Decimal(*args, **kwargs): # real signature unknown
    """ Boolean(obj) -> new boolean value """
    pass

def DECIMALARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def Float(*args, **kwargs): # real signature unknown
    """ Decimal(obj) -> new decimal.Decimal value """
    pass

def FLOAT(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def FLOATARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def get_wait_callback(*args, **kwargs): # real signature unknown
    """
    Return the currently registered wait callback.
    
    Return `None` if no callback is currently registered.
    """
    pass

def INTEGER(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def INTEGERARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def INTERVAL(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def INTERVALARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def IntervalFromPy(datetime_timedelta): # real signature unknown; restored from __doc__
    """ IntervalFromPy(datetime.timedelta) -> new wrapper """
    pass

def List(p_list, enc): # real signature unknown; restored from __doc__
    """ List(list, enc) -> new quoted list """
    pass

def LONGINTEGER(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def LONGINTEGERARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def new_type(oids, name, adapter): # real signature unknown; restored from __doc__
    """
    new_type(oids, name, adapter) -> new type object
    
    Create a new binding object. The object can be used with the
    `register_type()` function to bind PostgreSQL objects to python objects.
    
    :Parameters:
      * `oids`: Tuple of ``oid`` of the PostgreSQL types to convert.
      * `name`: Name for the new type
      * `adapter`: Callable to perform type conversion.
        It must have the signature ``fun(value, cur)`` where ``value`` is
        the string representation returned by PostgreSQL (`None` if ``NULL``)
        and ``cur`` is the cursor from which data are read.
    """
    pass

def NUMBER(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYDATE(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYDATEARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYDATETIME(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYDATETIMEARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYINTERVAL(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYINTERVALARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYTIME(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def PYTIMEARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def QuotedString(p_str, enc): # real signature unknown; restored from __doc__
    """ QuotedString(str, enc) -> new quoted string """
    pass

def register_type(obj, conn_or_curs): # real signature unknown; restored from __doc__
    """
    register_type(obj, conn_or_curs) -> None -- register obj with psycopg type system
    
    :Parameters:
      * `obj`: A type adapter created by `new_type()`
      * `conn_or_curs`: A connection, cursor or None
    """
    pass

def ROWID(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def ROWIDARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def set_wait_callback(None): # real signature unknown; restored from __doc__
    """
    Register a callback function to block waiting for data.
    
    The callback should have signature :samp:`fun({conn})` and
    is called to wait for data available whenever a blocking function from the
    libpq is called.  Use `!set_wait_callback(None)` to revert to the
    original behaviour (i.e. using blocking libpq functions).
    
    The function is an hook to allow coroutine-based libraries (such as
    Eventlet_ or gevent_) to switch when Psycopg is blocked, allowing
    other coroutines to run concurrently.
    
    See `~psycopg2.extras.wait_select()` for an example of a wait callback
    implementation.
    
    .. _Eventlet: http://eventlet.net/
    .. _gevent: http://www.gevent.org/
    """
    pass

def STRING(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def STRINGARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def TIME(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def Time(hour, minutes, seconds, tzinfo=None): # real signature unknown; restored from __doc__
    """
    Time(hour, minutes, seconds, tzinfo=None) -> new time
    
    Build an object holding a time value.
    """
    pass

def TIMEARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def TimeFromPy(datetime_time): # real signature unknown; restored from __doc__
    """ TimeFromPy(datetime.time) -> new wrapper """
    pass

def TimeFromTicks(ticks): # real signature unknown; restored from __doc__
    """
    TimeFromTicks(ticks) -> new time
    
    Build an object holding a time value from the given ticks value.
    
    Ticks are the number of seconds since the epoch; see the documentation of the standard Python time module for details).
    """
    pass

def Timestamp(year, month, day, hour, minutes, seconds, tzinfo=None): # real signature unknown; restored from __doc__
    """
    Timestamp(year, month, day, hour, minutes, seconds, tzinfo=None) -> new timestamp
    
    Build an object holding a timestamp value.
    """
    pass

def TimestampFromPy(datetime_datetime): # real signature unknown; restored from __doc__
    """ TimestampFromPy(datetime.datetime) -> new wrapper """
    pass

def TimestampFromTicks(ticks): # real signature unknown; restored from __doc__
    """
    TimestampFromTicks(ticks) -> new timestamp
    
    Build an object holding a timestamp value from the given ticks value.
    
    Ticks are the number of seconds since the epoch; see the documentation of the standard Python time module for details).
    """
    pass

def UNICODE(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

def UNICODEARRAY(*args, **kwargs): # real signature unknown
    """ psycopg type-casting object """
    pass

# classes

class connection(object):
    """
    connection(dsn, ...) -> new connection object
    
    :Groups:
      * `DBAPI-2.0 errors`: Error, Warning, InterfaceError,
        DatabaseError, InternalError, OperationalError,
        ProgrammingError, IntegrityError, DataError, NotSupportedError
    """
    def close(self): # real signature unknown; restored from __doc__
        """ close() -- Close the connection. """
        pass

    def commit(self): # real signature unknown; restored from __doc__
        """ commit() -- Commit all changes to database. """
        pass

    def cursor(self, cursor_factory=None): # real signature unknown; restored from __doc__
        """
        cursor(cursor_factory=extensions.cursor) -- new cursor
        
        Return a new cursor.
        
        The ``cursor_factory`` argument can be used to
        create non-standard cursors by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.cursor`.
        
        :rtype: `extensions.cursor`
        """
        pass

    def fileno(self): # real signature unknown; restored from __doc__
        """ fileno() -> int -- Return file descriptor associated to database connection. """
        return 0

    def get_backend_pid(self): # real signature unknown; restored from __doc__
        """ get_backend_pid() -- Get backend process id. """
        pass

    def get_parameter_status(self, parameter): # real signature unknown; restored from __doc__
        """
        get_parameter_status(parameter) -- Get backend parameter status.
        
        Potential values for ``parameter``:
          server_version, server_encoding, client_encoding, is_superuser,
          session_authorization, DateStyle, TimeZone, integer_datetimes,
          and standard_conforming_strings
        If server did not report requested parameter, None is returned.
        
        See libpq docs for PQparameterStatus() for further details.
        """
        pass

    def get_transaction_status(self): # real signature unknown; restored from __doc__
        """ get_transaction_status() -- Get backend transaction status. """
        pass

    def isexecuting(self): # real signature unknown; restored from __doc__
        """ isexecuting() -> bool -- Return True if the connection is executing an asynchronous operation. """
        return False

    def lobject(self, *args, **kwargs): # real signature unknown
        """
        cursor(oid=0, mode=0, new_oid=0, new_file=None,
               lobject_factory=extensions.lobject) -- new lobject
        
        Return a new lobject.
        
        The ``lobject_factory`` argument can be used
        to create non-standard lobjects by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.lobject`.
        
        :rtype: `extensions.lobject`
        """
        pass

    def poll(self, *args, **kwargs): # real signature unknown
        """
        cursor(oid=0, mode=0, new_oid=0, new_file=None,
               lobject_factory=extensions.lobject) -- new lobject
        
        Return a new lobject.
        
        The ``lobject_factory`` argument can be used
        to create non-standard lobjects by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.lobject`.
        
        :rtype: `extensions.lobject`
        """
        pass

    def reset(self): # real signature unknown; restored from __doc__
        """ reset() -- Reset current connection to defaults. """
        pass

    def rollback(self): # real signature unknown; restored from __doc__
        """ rollback() -- Roll back all changes done to database. """
        pass

    def set_client_encoding(self, encoding): # real signature unknown; restored from __doc__
        """ set_client_encoding(encoding) -- Set client encoding to ``encoding``. """
        pass

    def set_isolation_level(self, level): # real signature unknown; restored from __doc__
        """ set_isolation_level(level) -- Switch isolation level to ``level``. """
        pass

    def __init__(self, dsn, *more): # real signature unknown; restored from __doc__
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    def __str__(self): # real signature unknown; restored from __doc__
        """ x.__str__() <==> str(x) """
        pass

    async = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """True if the connection is asynchronous."""

    binary_types = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """A set of typecasters to convert binary values."""

    closed = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """True if the connection is closed."""

    DatabaseError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Error related to the database engine."""

    DataError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Error related to problems with the processed data."""

    dsn = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The current connection string."""

    encoding = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The current client encoding."""

    Error = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Base class for error exceptions."""

    IntegrityError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Error related to database integrity."""

    InterfaceError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Error related to the database interface."""

    InternalError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The database encountered an internal error."""

    isolation_level = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The current isolation level."""

    notices = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    notifies = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    NotSupportedError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """A method or database API was used which is not supported by the database."""

    OperationalError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Error related to database operation (disconnect, memory allocation etc)."""

    ProgrammingError = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Error related to database programming (SQL error, table not found etc)."""

    protocol_version = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Protocol version (2 or 3) used for this connection."""

    server_version = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Server version."""

    status = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The current transaction status."""

    string_types = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """A set of typecasters to convert textual values."""

    Warning = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """A database warning."""



class cursor(object):
    """ A database cursor. """
    def callproc(self, procname, parameters=None): # real signature unknown; restored from __doc__
        """ callproc(procname, parameters=None) -- Execute stored procedure. """
        pass

    def close(self): # real signature unknown; restored from __doc__
        """ close() -- Close the cursor. """
        pass

    def copy_expert(self, sql, file, size=None): # real signature unknown; restored from __doc__
        """
        copy_expert(sql, file, size=None) -- Submit a user-composed COPY statement.
        `file` must be an open, readable file for COPY FROM or an open, writeable
        file for COPY TO. The optional `size` argument, when specified for a COPY
        FROM statement, will be passed to file's read method to control the read
        buffer size.
        """
        pass

    def copy_from(self, file, table, sep=None, null=None, columns=None): # real signature unknown; restored from __doc__
        """ copy_from(file, table, sep='\t', null='\N', columns=None) -- Copy table from file. """
        pass

    def copy_to(self, file, table, sep=None, null=None, columns=None): # real signature unknown; restored from __doc__
        """ copy_to(file, table, sep='\t', null='\N', columns=None) -- Copy table to file. """
        pass

    def execute(self, query, vars=None): # real signature unknown; restored from __doc__
        """ execute(query, vars=None) -- Execute query with bound vars. """
        pass

    def executemany(self, query, vars_list): # real signature unknown; restored from __doc__
        """ executemany(query, vars_list) -- Execute many queries with bound vars. """
        pass

    def fetchall(self): # real signature unknown; restored from __doc__
        """
        fetchall() -> list of tuple
        
        Return all the remaining rows of a query result set.
        
        Rows are returned in the form of a list of tuples (by default) or using
        the sequence factory previously set in the `row_factory` attribute.
        Return `None` when no more data is available.
        """
        return []

    def fetchmany(self, size=None): # real signature unknown; restored from __doc__
        """
        fetchmany(size=self.arraysize) -> list of tuple
        
        Return the next `size` rows of a query result set in the form of a list
        of tuples (by default) or using the sequence factory previously set in
        the `row_factory` attribute. Return `None` when no more data is available.
        """
        return []

    def fetchone(self): # real signature unknown; restored from __doc__
        """
        fetchone() -> tuple or None
        
        Return the next row of a query result set in the form of a tuple (by
        default) or using the sequence factory previously set in the
        `row_factory` attribute. Return `None` when no more data is available.
        """
        return ()

    def mogrify(self, query, vars=None): # real signature unknown; restored from __doc__
        """ mogrify(query, vars=None) -> str -- Return query after vars binding. """
        return ""

    def next(self): # real signature unknown; restored from __doc__
        """ x.next() -> the next value, or raise StopIteration """
        pass

    def nextset(self): # real signature unknown; restored from __doc__
        """
        nextset() -- Skip to next set of data.
        
        This method is not supported (PostgreSQL does not have multiple data 
        sets) and will raise a NotSupportedError exception.
        """
        pass

    def scroll(self, value, mode='relative'): # real signature unknown; restored from __doc__
        """ scroll(value, mode='relative') -- Scroll to new position according to mode. """
        pass

    def setinputsizes(self, sizes): # real signature unknown; restored from __doc__
        """
        setinputsizes(sizes) -- Set memory areas before execute.
        
        This method currently does nothing but it is safe to call it.
        """
        pass

    def setoutputsize(self, size, column=None): # real signature unknown; restored from __doc__
        """
        setoutputsize(size, column=None) -- Set column buffer size.
        
        This method currently does nothing but it is safe to call it.
        """
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

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    def __str__(self): # real signature unknown; restored from __doc__
        """ x.__str__() <==> str(x) """
        pass

    arraysize = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Number of records `fetchmany()` must fetch if not explicitly specified."""

    binary_types = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    closed = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """True if cursor is closed, False if cursor is open"""

    connection = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The connection where the cursor comes from."""

    description = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Cursor description as defined in DBAPI-2.0."""

    lastrowid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The ``oid`` of the last row inserted by the cursor."""

    name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    query = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The last query text sent to the backend."""

    rowcount = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Number of rows read from the backend in the last command."""

    rownumber = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The current row position."""

    row_factory = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    statusmessage = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The return message of the last command."""

    string_types = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    typecaster = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    tzinfo_factory = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default



class Error(StandardError):
    """ Base class for error exceptions. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""


    cursor = None
    pgcode = None
    pgerror = None


class DatabaseError(__psycopg2.Error):
    """ Error related to the database engine. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class DataError(__psycopg2.DatabaseError):
    """ Error related to problems with the processed data. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class IntegrityError(__psycopg2.DatabaseError):
    """ Error related to database integrity. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class InterfaceError(__psycopg2.Error):
    """ Error related to the database interface. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class InternalError(__psycopg2.DatabaseError):
    """ The database encountered an internal error. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class ISQLQuote(object):
    """
    Abstract ISQLQuote protocol
    
    An object conform to this protocol should expose a ``getquoted()`` method
    returning the SQL representation of the object.
    """
    def getbinary(self): # real signature unknown; restored from __doc__
        """ getbinary() -- return SQL-quoted binary representation of this object """
        pass

    def getbuffer(self): # real signature unknown; restored from __doc__
        """ getbuffer() -- return this object """
        pass

    def getquoted(self): # real signature unknown; restored from __doc__
        """ getquoted() -- return SQL-quoted representation of this object """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    _wrapped = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default



class lobject(object):
    """ A database large object. """
    def close(self): # real signature unknown; restored from __doc__
        """ close() -- Close the lobject. """
        pass

    def export(self, filename): # real signature unknown; restored from __doc__
        """ export(filename) -- Export large object to given file. """
        pass

    def read(self, size=-1): # real signature unknown; restored from __doc__
        """ read(size=-1) -- Read at most size bytes or to the end of the large object. """
        pass

    def seek(self, offset, whence=0): # real signature unknown; restored from __doc__
        """ seek(offset, whence=0) -- Set the lobject's current position. """
        pass

    def tell(self): # real signature unknown; restored from __doc__
        """ tell() -- Return the lobject's current position. """
        pass

    def truncate(self, len=0): # real signature unknown; restored from __doc__
        """ truncate(len=0) -- Truncate large object to given size. """
        pass

    def unlink(self): # real signature unknown; restored from __doc__
        """ unlink() -- Close and then remove the lobject. """
        pass

    def write(self, p_str): # real signature unknown; restored from __doc__
        """ write(str) -- Write a string to the large object. """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    def __str__(self): # real signature unknown; restored from __doc__
        """ x.__str__() <==> str(x) """
        pass

    closed = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The if the large object is closed (no file-like methods)."""

    mode = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Open mode ('r', 'w', 'rw' or 'n')."""

    oid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The backend OID associated to this lobject."""



class NotSupportedError(__psycopg2.DatabaseError):
    """ A method or database API was used which is not supported by the database. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class OperationalError(__psycopg2.DatabaseError):
    """ Error related to database operation (disconnect, memory allocation etc). """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class ProgrammingError(__psycopg2.DatabaseError):
    """ Error related to database programming (SQL error, table not found etc). """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class QueryCanceledError(__psycopg2.OperationalError):
    """ Error related to SQL query cancellation. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class TransactionRollbackError(__psycopg2.OperationalError):
    """ Error causing transaction rollback (deadlocks, serialisation failures, etc). """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass


class Warning(StandardError):
    """ A database warning. """
    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""



# variables with complex values

adapters = {
    (
        None, # (!) real value is ''
        ISQLQuote,
    ): 
        None # (!) real value is ''
    ,
    (
        None, # (!) real value is ''
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) forward: TimeFromPy, real value is ''
    ,
    (
        None, # (!) real value is ''
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) forward: IntervalFromPy, real value is ''
    ,
    (
        None, # (!) real value is ''
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) forward: TimestampFromPy, real value is ''
    ,
    (
        None, # (!) real value is ''
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) forward: DateFromPy, real value is ''
    ,
    (
        bool,
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) real value is ''
    ,
    (
        buffer,
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) real value is ''
    ,
    (
        float,
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) real value is ''
    ,
    (
        int,
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) real value is ''
    ,
    (
        list,
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) real value is ''
    ,
    (
        long,
        '<value is a self-reference, replaced by this string>',
    ): 
        '<value is a self-reference, replaced by this string>'
    ,
    (
        bytes,
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) real value is ''
    ,
    (
        tuple,
        '<value is a self-reference, replaced by this string>',
    ): 
        None # (!) real value is ''
    ,
    (
        unicode,
        '<value is a self-reference, replaced by this string>',
    ): 
        '<value is a self-reference, replaced by this string>'
    ,
}

binary_types = {}

encodings = {
    'ABC': 'cp1258',
    'ALT': 'cp866',
    'BIG5': 'big5',
    'EUC_JP': 'euc_jp',
    'EUC_KR': 'euc_kr',
    'GB18030': 'gb18030',
    'GBK': 'gbk',
    'ISO88591': 'iso8859_1',
    'ISO885913': 'iso8859_13',
    'ISO885914': 'iso8859_14',
    'ISO885915': 'iso8859_15',
    'ISO88592': 'iso8859_2',
    'ISO88593': 'iso8859_3',
    'ISO88595': 'iso8859_5',
    'ISO88596': 'iso8859_6',
    'ISO88597': 'iso8859_7',
    'ISO88598': 'iso8859_8',
    'ISO88599': 'iso8859_9',
    'JOHAB': 'johab',
    'KOI8': 'koi8_r',
    'KOI8R': 'koi8_r',
    'LATIN1': 'iso8859_1',
    'LATIN2': 'iso8859_2',
    'LATIN3': 'iso8859_3',
    'LATIN4': 'iso8859_4',
    'LATIN5': 'iso8859_9',
    'LATIN6': 'iso8859_10',
    'LATIN7': 'iso8859_13',
    'LATIN8': 'iso8859_14',
    'LATIN9': 'iso8859_15',
    'Mskanji': 'cp932',
    'SJIS': 'cp932',
    'SQL_ASCII': 'ascii',
    'ShiftJIS': 'cp932',
    'TCVN': 'cp1258',
    'TCVN5712': 'cp1258',
    'UHC': 'cp949',
    'UNICODE': 'utf_8',
    'UTF8': 'utf_8',
    'VSCII': 'cp1258',
    'WIN': 'cp1251',
    'WIN1250': 'cp1250',
    'WIN1251': 'cp1251',
    'WIN1252': 'cp1252',
    'WIN1253': 'cp1253',
    'WIN1254': 'cp1254',
    'WIN1255': 'cp1255',
    'WIN1256': 'cp1256',
    'WIN1257': 'cp1257',
    'WIN1258': 'cp1258',
    'WIN866': 'cp866',
    'WIN874': 'cp874',
    'WIN932': 'cp932',
    'WIN936': 'gbk',
    'WIN949': 'cp949',
    'WIN950': 'cp950',
    'Windows932': 'cp932',
    'Windows936': 'gbk',
    'Windows949': 'cp949',
    'Windows950': 'cp950',
}

string_types = {} # real value of type <type 'dict'> replaced

_C_API = None # (!) real value is ''

