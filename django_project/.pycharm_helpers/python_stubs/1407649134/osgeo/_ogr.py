# encoding: utf-8
# module osgeo._ogr
# from /usr/local/lib/python2.7/site-packages/GDAL-1.9.0-py2.7-linux-x86_64.egg/osgeo/_ogr.so
# by generator 1.138
# no doc
# no imports

# Variables with simple values

ALTER_ALL_FLAG = 7

ALTER_NAME_FLAG = 1

ALTER_TYPE_FLAG = 2

ALTER_WIDTH_PRECISION_FLAG = 4

NullFID = -1

ODrCCreateDataSource = 'CreateDataSource'
ODrCDeleteDataSource = 'DeleteDataSource'
ODsCCreateLayer = 'CreateLayer'
ODsCDeleteLayer = 'DeleteLayer'

OFTBinary = 8
OFTDate = 9
OFTDateTime = 11
OFTInteger = 0
OFTIntegerList = 1
OFTReal = 2
OFTRealList = 3
OFTString = 4
OFTStringList = 5
OFTTime = 10
OFTWideString = 6
OFTWideStringList = 7

OJLeft = 1
OJRight = 2
OJUndefined = 0

OLCAlterFieldDefn = 'AlterFieldDefn'
OLCCreateField = 'CreateField'
OLCDeleteFeature = 'DeleteFeature'
OLCDeleteField = 'DeleteField'
OLCFastFeatureCount = 'FastFeatureCount'
OLCFastGetExtent = 'FastGetExtent'
OLCFastSetNextByIndex = 'FastSetNextByIndex'
OLCFastSpatialFilter = 'FastSpatialFilter'
OLCIgnoreFields = 'IgnoreFields'
OLCRandomRead = 'RandomRead'
OLCRandomWrite = 'RandomWrite'
OLCReorderFields = 'ReorderFields'
OLCSequentialWrite = 'SequentialWrite'
OLCStringsAsUTF8 = 'StringsAsUTF8'
OLCTransactions = 'Transactions'

wkb25Bit = -2147483648
wkb25DBit = -2147483648
wkbGeometryCollection = 7
wkbGeometryCollection25D = -2147483641
wkbLinearRing = 101
wkbLineString = 2
wkbLineString25D = -2147483646
wkbMultiLineString = 5
wkbMultiLineString25D = -2147483643
wkbMultiPoint = 4
wkbMultiPoint25D = -2147483644
wkbMultiPolygon = 6
wkbMultiPolygon25D = -2147483642
wkbNDR = 1
wkbNone = 100
wkbPoint = 1
wkbPoint25D = -2147483647
wkbPolygon = 3
wkbPolygon25D = -2147483645
wkbUnknown = 0
wkbXDR = 0

# functions

def ApproximateArcAngles(double_dfCenterX, double_dfCenterY, double_dfZ, double_dfPrimaryRadius, double_dfSecondaryAxis, double_dfRotation, double_dfStartAngle, double_dfEndAngle, double_dfMaxAngleStepSizeDegrees): # real signature unknown; restored from __doc__
    """
    ApproximateArcAngles(double dfCenterX, double dfCenterY, double dfZ, double dfPrimaryRadius, 
        double dfSecondaryAxis, 
        double dfRotation, double dfStartAngle, double dfEndAngle, 
        double dfMaxAngleStepSizeDegrees) -> Geometry
    """
    pass

def BuildPolygonFromEdges(Geometry_hLineCollection, int_bBestEffort=0, int_bAutoClose=0, double_dfTolerance=0): # real signature unknown; restored from __doc__
    """
    BuildPolygonFromEdges(Geometry hLineCollection, int bBestEffort = 0, int bAutoClose = 0, 
        double dfTolerance = 0) -> Geometry
    """
    pass

def CreateGeometryFromGML(char_input_string): # real signature unknown; restored from __doc__
    """ CreateGeometryFromGML(char input_string) -> Geometry """
    pass

def CreateGeometryFromJson(char_input_string): # real signature unknown; restored from __doc__
    """ CreateGeometryFromJson(char input_string) -> Geometry """
    pass

def CreateGeometryFromWkb(int_len, SpatialReference_reference=None): # real signature unknown; restored from __doc__
    """ CreateGeometryFromWkb(int len, SpatialReference reference = None) -> Geometry """
    pass

def CreateGeometryFromWkt(char_val, SpatialReference_reference=None): # real signature unknown; restored from __doc__
    """ CreateGeometryFromWkt(char val, SpatialReference reference = None) -> Geometry """
    pass

def DataSource_CopyLayer(DataSource_self, Layer_src_layer, char_new_name, char_options=None): # real signature unknown; restored from __doc__
    """
    DataSource_CopyLayer(DataSource self, Layer src_layer, char new_name, char options = None) -> Layer
    
    OGRLayerH
    OGR_DS_CopyLayer(OGRDataSourceH hDS, OGRLayerH hSrcLayer, const char
    *pszNewName, char **papszOptions)
    
    Duplicate an existing layer.
    
    This function creates a new layer, duplicate the field definitions of
    the source layer and then duplicate each features of the source layer.
    The papszOptions argument can be used to control driver specific
    creation options. These options are normally documented in the format
    specific documentation. The source layer may come from another
    dataset.
    
    This function is the same as the C++ method OGRDataSource::CopyLayer
    
    Parameters:
    -----------
    
    hDS:  handle to the data source where to create the new layer
    
    hSrcLayer:  handle to the source layer.
    
    pszNewName:  the name of the layer to create.
    
    papszOptions:  a StringList of name=value options. Options are driver
    specific.
    
    an handle to the layer, or NULL if an error occurs.
    """
    pass

def DataSource_CreateLayer(DataSource_self, char_name, SpatialReference_srs=None, OGRwkbGeometryType_geom_type=None, char_options=None): # real signature unknown; restored from __doc__
    """
    DataSource_CreateLayer(DataSource self, char name, SpatialReference srs = None, 
        OGRwkbGeometryType geom_type = wkbUnknown, 
        char options = None) -> Layer
    
    OGRLayerH
    OGR_DS_CreateLayer(OGRDataSourceH hDS, const char *pszName,
    OGRSpatialReferenceH hSpatialRef, OGRwkbGeometryType eType, char
    **papszOptions)
    
    This function attempts to create a new layer on the data source with
    the indicated name, coordinate system, geometry type.
    
    The papszOptions argument can be used to control driver specific
    creation options. These options are normally documented in the format
    specific documentation.
    
    This function is the same as the C++ method
    OGRDataSource::CreateLayer().
    
    Parameters:
    -----------
    
    hDS:  The dataset handle.
    
    pszName:  the name for the new layer. This should ideally not match
    any existing layer on the datasource.
    
    hSpatialRef:  handle to the coordinate system to use for the new
    layer, or NULL if no coordinate system is available.
    
    eType:  the geometry type for the layer. Use wkbUnknown if there are
    no constraints on the types geometry to be written.
    
    papszOptions:  a StringList of name=value options. Options are driver
    specific, and driver information can be found at the following
    url:http://www.gdal.org/ogr/ogr_formats.html
    
    NULL is returned on failure, or a new OGRLayer handle on success.
    Example:
    """
    pass

def DataSource_DeleteLayer(DataSource_self, int_index): # real signature unknown; restored from __doc__
    """
    DataSource_DeleteLayer(DataSource self, int index) -> OGRErr
    
    OGRErr
    OGR_DS_DeleteLayer(OGRDataSourceH hDS, int iLayer)
    
    Delete the indicated layer from the datasource.
    
    If this method is supported the ODsCDeleteLayer capability will test
    TRUE on the OGRDataSource.
    
    This method is the same as the C++ method
    OGRDataSource::DeleteLayer().
    
    Parameters:
    -----------
    
    hDS:  handle to the datasource
    
    iLayer:  the index of the layer to delete.
    
    OGRERR_NONE on success, or OGRERR_UNSUPPORTED_OPERATION if deleting
    layers is not supported for this datasource.
    """
    pass

def DataSource_ExecuteSQL(DataSource_self, char_statement, Geometry_spatialFilter=None, char_dialect=""): # real signature unknown; restored from __doc__
    """
    DataSource_ExecuteSQL(DataSource self, char statement, Geometry spatialFilter = None, 
        char dialect = "") -> Layer
    
    OGRLayerH
    OGR_DS_ExecuteSQL(OGRDataSourceH hDS, const char *pszStatement,
    OGRGeometryH hSpatialFilter, const char *pszDialect)
    
    Execute an SQL statement against the data store.
    
    The result of an SQL query is either NULL for statements that are in
    error, or that have no results set, or an OGRLayer handle representing
    a results set from the query. Note that this OGRLayer is in addition
    to the layers in the data store and must be destroyed with
    OGR_DS_ReleaseResultSet() before the data source is closed
    (destroyed).
    
    For more information on the SQL dialect supported internally by OGR
    review theOGR SQL document. Some drivers (ie. Oracle and PostGIS) pass
    the SQL directly through to the underlying RDBMS.
    
    This function is the same as the C++ method
    OGRDataSource::ExecuteSQL();
    
    Parameters:
    -----------
    
    hDS:  handle to the data source on which the SQL query is executed.
    
    pszSQLCommand:  the SQL statement to execute.
    
    hSpatialFilter:  handle to a geometry which represents a spatial
    filter. Can be NULL.
    
    pszDialect:  allows control of the statement dialect. If set to NULL,
    the OGR SQL engine will be used, except for RDBMS drivers that will
    use their dedicated SQL engine, unless OGRSQL is explicitely passed as
    the dialect.
    
    an handle to a OGRLayer containing the results of the query.
    Deallocate with OGR_DS_ReleaseResultSet().
    """
    pass

def DataSource_GetDriver(DataSource_self): # real signature unknown; restored from __doc__
    """
    DataSource_GetDriver(DataSource self) -> Driver
    
    OGRSFDriverH
    OGR_DS_GetDriver(OGRDataSourceH hDS)
    
    Returns the driver that the dataset was opened with.
    
    This method is the same as the C++ method OGRDataSource::GetDriver()
    
    Parameters:
    -----------
    
    hDS:  handle to the datasource
    
    NULL if driver info is not available, or pointer to a driver owned by
    the OGRSFDriverManager.
    """
    pass

def DataSource_GetLayerByIndex(DataSource_self, int_index=0): # real signature unknown; restored from __doc__
    """ DataSource_GetLayerByIndex(DataSource self, int index = 0) -> Layer """
    pass

def DataSource_GetLayerByName(DataSource_self, char_layer_name): # real signature unknown; restored from __doc__
    """
    DataSource_GetLayerByName(DataSource self, char layer_name) -> Layer
    
    OGRLayerH
    OGR_DS_GetLayerByName(OGRDataSourceH hDS, const char *pszName)
    
    Fetch a layer by name.
    
    The returned layer remains owned by the OGRDataSource and should not
    be deleted by the application.
    
    This function is the same as the C++ method
    OGRDataSource::GetLayerByName().
    
    Parameters:
    -----------
    
    hDS:  handle to the data source from which to get the layer.
    
    pszLayerName:  Layer the layer name of the layer to fetch.
    
    an handle to the layer, or NULL if the layer is not found or an error
    occurs.
    """
    pass

def DataSource_GetLayerCount(DataSource_self): # real signature unknown; restored from __doc__
    """
    DataSource_GetLayerCount(DataSource self) -> int
    
    int
    OGR_DS_GetLayerCount(OGRDataSourceH hDS)
    
    Get the number of layers in this data source.
    
    This function is the same as the C++ method
    OGRDataSource::GetLayerCount().
    
    Parameters:
    -----------
    
    hDS:  handle to the data source from which to get the number of
    layers.
    
    layer count.
    """
    return 0

def DataSource_GetName(DataSource_self): # real signature unknown; restored from __doc__
    """
    DataSource_GetName(DataSource self) -> char
    
    const char*
    OGR_DS_GetName(OGRDataSourceH hDS)
    
    Returns the name of the data source.
    
    This string should be sufficient to open the data source if passed to
    the same OGRSFDriver that this data source was opened with, but it
    need not be exactly the same string that was used to open the data
    source. Normally this is a filename.
    
    This function is the same as the C++ method OGRDataSource::GetName().
    
    Parameters:
    -----------
    
    hDS:  handle to the data source to get the name from.
    
    pointer to an internal name string which should not be modified or
    freed by the caller.
    """
    return ""

def DataSource_GetRefCount(DataSource_self): # real signature unknown; restored from __doc__
    """
    DataSource_GetRefCount(DataSource self) -> int
    
    int
    OGR_DS_GetRefCount(OGRDataSourceH hDataSource)
    """
    return 0

def DataSource_GetSummaryRefCount(DataSource_self): # real signature unknown; restored from __doc__
    """
    DataSource_GetSummaryRefCount(DataSource self) -> int
    
    int
    OGR_DS_GetSummaryRefCount(OGRDataSourceH hDataSource)
    """
    return 0

def DataSource_name_get(DataSource_self): # real signature unknown; restored from __doc__
    """ DataSource_name_get(DataSource self) -> char """
    return ""

def DataSource_ReleaseResultSet(DataSource_self, Layer_layer): # real signature unknown; restored from __doc__
    """
    DataSource_ReleaseResultSet(DataSource self, Layer layer)
    
    void
    OGR_DS_ReleaseResultSet(OGRDataSourceH hDS, OGRLayerH hLayer)
    
    Release results of OGR_DS_ExecuteSQL().
    
    This function should only be used to deallocate OGRLayers resulting
    from an OGR_DS_ExecuteSQL() call on the same OGRDataSource. Failure to
    deallocate a results set before destroying the OGRDataSource may cause
    errors.
    
    This function is the same as the C++ method
    OGRDataSource::ReleaseResultSet().
    
    Parameters:
    -----------
    
    hDS:  an handle to the data source on which was executed an SQL query.
    
    hLayer:  handle to the result of a previous OGR_DS_ExecuteSQL() call.
    """
    pass

def DataSource_swigregister(*args, **kwargs): # real signature unknown
    pass

def DataSource_SyncToDisk(DataSource_self): # real signature unknown; restored from __doc__
    """
    DataSource_SyncToDisk(DataSource self) -> OGRErr
    
    OGRErr
    OGR_DS_SyncToDisk(OGRDataSourceH hDS)
    
    Flush pending changes to disk.
    
    This call is intended to force the datasource to flush any pending
    writes to disk, and leave the disk file in a consistent state. It
    would not normally have any effect on read-only datasources.
    
    Some data sources do not implement this method, and will still return
    OGRERR_NONE. An error is only returned if an error occurs while
    attempting to flush to disk.
    
    The default implementation of this method just calls the SyncToDisk()
    method on each of the layers. Conceptionally, calling SyncToDisk() on
    a datasource should include any work that might be accomplished by
    calling SyncToDisk() on layers in that data source.
    
    In any event, you should always close any opened datasource with
    OGR_DS_Destroy() that will ensure all data is correctly flushed.
    
    This method is the same as the C++ method OGRDataSource::SyncToDisk()
    
    Parameters:
    -----------
    
    hDS:  handle to the data source
    
    OGRERR_NONE if no error occurs (even if nothing is done) or an error
    code.
    """
    pass

def DataSource_TestCapability(DataSource_self, char_cap): # real signature unknown; restored from __doc__
    """
    DataSource_TestCapability(DataSource self, char cap) -> bool
    
    int
    OGR_DS_TestCapability(OGRDataSourceH hDS, const char *pszCap)
    
    Test if capability is available.
    
    One of the following data source capability names can be passed into
    this function, and a TRUE or FALSE value will be returned indicating
    whether or not the capability is available for this object.
    
    ODsCCreateLayer: True if this datasource can create new layers.
    
    The #define macro forms of the capability names should be used in
    preference to the strings themselves to avoid mispelling.
    
    This function is the same as the C++ method
    OGRDataSource::TestCapability().
    
    Parameters:
    -----------
    
    hDS:  handle to the data source against which to test the capability.
    
    pszCapability:  the capability to test.
    
    TRUE if capability available otherwise FALSE.
    """
    return False

def delete_DataSource(DataSource_self): # real signature unknown; restored from __doc__
    """ delete_DataSource(DataSource self) """
    pass

def delete_Feature(Feature_self): # real signature unknown; restored from __doc__
    """ delete_Feature(Feature self) """
    pass

def delete_FeatureDefn(FeatureDefn_self): # real signature unknown; restored from __doc__
    """ delete_FeatureDefn(FeatureDefn self) """
    pass

def delete_FieldDefn(FieldDefn_self): # real signature unknown; restored from __doc__
    """ delete_FieldDefn(FieldDefn self) """
    pass

def delete_Geometry(Geometry_self): # real signature unknown; restored from __doc__
    """ delete_Geometry(Geometry self) """
    pass

def DontUseExceptions(): # real signature unknown; restored from __doc__
    """ DontUseExceptions() """
    pass

def Driver_CopyDataSource(Driver_self, DataSource_copy_ds, char_utf8_path, char_options=None): # real signature unknown; restored from __doc__
    """
    Driver_CopyDataSource(Driver self, DataSource copy_ds, char utf8_path, char options = None) -> DataSource
    
    OGRDataSourceH
    OGR_Dr_CopyDataSource(OGRSFDriverH hDriver, OGRDataSourceH hSrcDS,
    const char *pszNewName, char **papszOptions)
    
    This function creates a new datasource by copying all the layers from
    the source datasource.
    
    It is important to call OGR_DS_Destroy() when the datasource is no
    longer used to ensure that all data has been properly flushed to disk.
    
    This function is the same as the C++ method
    OGRSFDriver::CopyDataSource().
    
    Parameters:
    -----------
    
    hDriver:  handle to the driver on which data source creation is based.
    
    hSrcDS:  source datasource
    
    pszNewName:  the name for the new data source.
    
    papszOptions:  a StringList of name=value options. Options are driver
    specific, and driver information can be found at the following
    url:http://www.gdal.org/ogr/ogr_formats.html
    
    NULL is returned on failure, or a new OGRDataSource handle on success.
    """
    pass

def Driver_CreateDataSource(Driver_self, char_utf8_path, char_options=None): # real signature unknown; restored from __doc__
    """
    Driver_CreateDataSource(Driver self, char utf8_path, char options = None) -> DataSource
    
    OGRDataSourceH
    OGR_Dr_CreateDataSource(OGRSFDriverH hDriver, const char *pszName,
    char **papszOptions)
    
    This function attempts to create a new data source based on the passed
    driver.
    
    The papszOptions argument can be used to control driver specific
    creation options. These options are normally documented in the format
    specific documentation.
    
    It is important to call OGR_DS_Destroy() when the datasource is no
    longer used to ensure that all data has been properly flushed to disk.
    
    This function is the same as the C++ method
    OGRSFDriver::CreateDataSource().
    
    Parameters:
    -----------
    
    hDriver:  handle to the driver on which data source creation is based.
    
    pszName:  the name for the new data source. UTF-8 encoded.
    
    papszOptions:  a StringList of name=value options. Options are driver
    specific, and driver information can be found at the following
    url:http://www.gdal.org/ogr/ogr_formats.html
    
    NULL is returned on failure, or a new OGRDataSource handle on success.
    """
    pass

def Driver_DeleteDataSource(Driver_self, char_utf8_path): # real signature unknown; restored from __doc__
    """
    Driver_DeleteDataSource(Driver self, char utf8_path) -> int
    
    OGRErr
    OGR_Dr_DeleteDataSource(OGRSFDriverH hDriver, const char
    *pszDataSource)
    
    Delete a datasource.
    
    Delete (from the disk, in the database, ...) the named datasource.
    Normally it would be safest if the datasource was not open at the
    time.
    
    Whether this is a supported operation on this driver case be tested
    using TestCapability() on ODrCDeleteDataSource.
    
    This method is the same as the C++ method
    OGRSFDriver::DeleteDataSource().
    
    Parameters:
    -----------
    
    hDriver:  handle to the driver on which data source deletion is based.
    
    pszDataSource:  the name of the datasource to delete.
    
    OGRERR_NONE on success, and OGRERR_UNSUPPORTED_OPERATION if this is
    not supported by this driver.
    """
    return 0

def Driver_Deregister(Driver_self): # real signature unknown; restored from __doc__
    """ Driver_Deregister(Driver self) """
    pass

def Driver_GetName(Driver_self): # real signature unknown; restored from __doc__
    """
    Driver_GetName(Driver self) -> char
    
    const char*
    OGR_Dr_GetName(OGRSFDriverH hDriver)
    
    Fetch name of driver (file format). This name should be relatively
    short (10-40 characters), and should reflect the underlying file
    format. For instance "ESRI Shapefile".
    
    This function is the same as the C++ method OGRSFDriver::GetName().
    
    Parameters:
    -----------
    
    hDriver:  handle to the the driver to get the name from.
    
    driver name. This is an internal string and should not be modified or
    freed.
    """
    return ""

def Driver_name_get(Driver_self): # real signature unknown; restored from __doc__
    """ Driver_name_get(Driver self) -> char """
    return ""

def Driver_Open(Driver_self, char_utf8_path, int_update=0): # real signature unknown; restored from __doc__
    """
    Driver_Open(Driver self, char utf8_path, int update = 0) -> DataSource
    
    OGRDataSourceH OGR_Dr_Open(OGRSFDriverH
    hDriver, const char *pszName, int bUpdate)
    
    Attempt to open file with this driver.
    
    This function is the same as the C++ method OGRSFDriver::Open().
    
    Parameters:
    -----------
    
    hDriver:  handle to the driver that is used to open file.
    
    pszName:  the name of the file, or data source to try and open.
    
    bUpdate:  TRUE if update access is required, otherwise FALSE (the
    default).
    
    NULL on error or if the pass name is not supported by this driver,
    otherwise an handle to an OGRDataSource. This OGRDataSource should be
    closed by deleting the object when it is no longer needed.
    """
    pass

def Driver_Register(Driver_self): # real signature unknown; restored from __doc__
    """ Driver_Register(Driver self) """
    pass

def Driver_swigregister(*args, **kwargs): # real signature unknown
    pass

def Driver_TestCapability(Driver_self, char_cap): # real signature unknown; restored from __doc__
    """
    Driver_TestCapability(Driver self, char cap) -> bool
    
    int
    OGR_Dr_TestCapability(OGRSFDriverH hDriver, const char *pszCap)
    
    Test if capability is available.
    
    One of the following data source capability names can be passed into
    this function, and a TRUE or FALSE value will be returned indicating
    whether or not the capability is available for this object.
    
    ODrCCreateDataSource: True if this driver can support creating data
    sources.
    
    ODrCDeleteDataSource: True if this driver supports deleting data
    sources.
    
    The #define macro forms of the capability names should be used in
    preference to the strings themselves to avoid mispelling.
    
    This function is the same as the C++ method
    OGRSFDriver::TestCapability().
    
    Parameters:
    -----------
    
    hDriver:  handle to the driver to test the capability against.
    
    pszCap:  the capability to test.
    
    TRUE if capability available otherwise FALSE.
    """
    return False

def FeatureDefn_AddFieldDefn(FeatureDefn_self, FieldDefn_defn): # real signature unknown; restored from __doc__
    """
    FeatureDefn_AddFieldDefn(FeatureDefn self, FieldDefn defn)
    
    void
    OGR_FD_AddFieldDefn(OGRFeatureDefnH hDefn, OGRFieldDefnH hNewField)
    
    Add a new field definition to the passed feature definition.
    
    To add a new field definition to a layer definition, do not use this
    function directly, but use OGR_L_CreateField() instead.
    
    This function should only be called while there are no OGRFeature
    objects in existance based on this OGRFeatureDefn. The OGRFieldDefn
    passed in is copied, and remains the responsibility of the caller.
    
    This function is the same as the C++ method
    OGRFeatureDefn::AddFieldDefn().
    
    Parameters:
    -----------
    
    hDefn:  handle to the feature definition to add the field definition
    to.
    
    hNewField:  handle to the new field definition.
    """
    pass

def FeatureDefn_GetFieldCount(FeatureDefn_self): # real signature unknown; restored from __doc__
    """
    FeatureDefn_GetFieldCount(FeatureDefn self) -> int
    
    int
    OGR_FD_GetFieldCount(OGRFeatureDefnH hDefn)
    
    Fetch number of fields on the passed feature definition.
    
    This function is the same as the C++ OGRFeatureDefn::GetFieldCount().
    
    Parameters:
    -----------
    
    hDefn:  handle to the feature definition to get the fields count from.
    
    count of fields.
    """
    return 0

def FeatureDefn_GetFieldDefn(FeatureDefn_self, int_i): # real signature unknown; restored from __doc__
    """
    FeatureDefn_GetFieldDefn(FeatureDefn self, int i) -> FieldDefn
    
    OGRFieldDefnH
    OGR_FD_GetFieldDefn(OGRFeatureDefnH hDefn, int iField)
    
    Fetch field definition of the passed feature definition.
    
    This function is the same as the C++ method
    OGRFeatureDefn::GetFieldDefn().
    
    Starting with GDAL 1.7.0, this method will also issue an error if the
    index is not valid.
    
    Parameters:
    -----------
    
    hDefn:  handle to the feature definition to get the field definition
    from.
    
    iField:  the field to fetch, between 0 and GetFieldCount()-1.
    
    an handle to an internal field definition object or NULL if invalid
    index. This object should not be modified or freed by the application.
    """
    pass

def FeatureDefn_GetFieldIndex(FeatureDefn_self, char_name): # real signature unknown; restored from __doc__
    """
    FeatureDefn_GetFieldIndex(FeatureDefn self, char name) -> int
    
    int
    OGR_FD_GetFieldIndex(OGRFeatureDefnH hDefn, const char *pszFieldName)
    
    Find field by name.
    
    The field index of the first field matching the passed field name
    (case insensitively) is returned.
    
    This function is the same as the C++ method
    OGRFeatureDefn::GetFieldIndex.
    
    Parameters:
    -----------
    
    hDefn:  handle to the feature definition to get field index from.
    
    pszFieldName:  the field name to search for.
    
    the field index, or -1 if no match found.
    """
    return 0

def FeatureDefn_GetGeomType(FeatureDefn_self): # real signature unknown; restored from __doc__
    """
    FeatureDefn_GetGeomType(FeatureDefn self) -> OGRwkbGeometryType
    
    OGRwkbGeometryType
    OGR_FD_GetGeomType(OGRFeatureDefnH hDefn)
    
    Fetch the geometry base type of the passed feature definition.
    
    This function is the same as the C++ method
    OGRFeatureDefn::GetGeomType().
    
    Parameters:
    -----------
    
    hDefn:  handle to the feature definition to get the geometry type
    from.
    
    the base type for all geometry related to this definition.
    """
    pass

def FeatureDefn_GetName(FeatureDefn_self): # real signature unknown; restored from __doc__
    """
    FeatureDefn_GetName(FeatureDefn self) -> char
    
    const char*
    OGR_FD_GetName(OGRFeatureDefnH hDefn)
    
    Get name of the OGRFeatureDefn passed as an argument.
    
    This function is the same as the C++ method OGRFeatureDefn::GetName().
    
    Parameters:
    -----------
    
    hDefn:  handle to the feature definition to get the name from.
    
    the name. This name is internal and should not be modified, or freed.
    """
    return ""

def FeatureDefn_GetReferenceCount(FeatureDefn_self): # real signature unknown; restored from __doc__
    """
    FeatureDefn_GetReferenceCount(FeatureDefn self) -> int
    
    int
    OGR_FD_GetReferenceCount(OGRFeatureDefnH hDefn)
    
    Fetch current reference count.
    
    This function is the same as the C++ method
    OGRFeatureDefn::GetReferenceCount().
    
    Parameters:
    -----------
    
    hDefn:  hanlde to the feature definition on witch OGRFeature are based
    on.
    
    the current reference count.
    """
    return 0

def FeatureDefn_IsGeometryIgnored(FeatureDefn_self): # real signature unknown; restored from __doc__
    """
    FeatureDefn_IsGeometryIgnored(FeatureDefn self) -> int
    
    int
    OGR_FD_IsGeometryIgnored(OGRFeatureDefnH hDefn)
    
    Determine whether the geometry can be omitted when fetching features.
    
    This function is the same as the C++ method
    OGRFeatureDefn::IsGeometryIgnored().
    
    Parameters:
    -----------
    
    hDefn:  hanlde to the feature definition on witch OGRFeature are based
    on.
    
    ignore state
    """
    return 0

def FeatureDefn_IsStyleIgnored(FeatureDefn_self): # real signature unknown; restored from __doc__
    """
    FeatureDefn_IsStyleIgnored(FeatureDefn self) -> int
    
    int
    OGR_FD_IsStyleIgnored(OGRFeatureDefnH hDefn)
    
    Determine whether the style can be omitted when fetching features.
    
    This function is the same as the C++ method
    OGRFeatureDefn::IsStyleIgnored().
    
    Parameters:
    -----------
    
    hDefn:  handle to the feature definition on which OGRFeature are based
    on.
    
    ignore state
    """
    return 0

def FeatureDefn_SetGeometryIgnored(FeatureDefn_self, int_bIgnored): # real signature unknown; restored from __doc__
    """
    FeatureDefn_SetGeometryIgnored(FeatureDefn self, int bIgnored)
    
    void
    OGR_FD_SetGeometryIgnored(OGRFeatureDefnH hDefn, int bIgnore)
    
    Set whether the geometry can be omitted when fetching features.
    
    This function is the same as the C++ method
    OGRFeatureDefn::SetGeometryIgnored().
    
    Parameters:
    -----------
    
    hDefn:  hanlde to the feature definition on witch OGRFeature are based
    on.
    
    bIgnore:  ignore state
    """
    pass

def FeatureDefn_SetGeomType(FeatureDefn_self, OGRwkbGeometryType_geom_type): # real signature unknown; restored from __doc__
    """
    FeatureDefn_SetGeomType(FeatureDefn self, OGRwkbGeometryType geom_type)
    
    void
    OGR_FD_SetGeomType(OGRFeatureDefnH hDefn, OGRwkbGeometryType eType)
    
    Assign the base geometry type for the passed layer (the same as the
    feature definition).
    
    All geometry objects using this type must be of the defined type or a
    derived type. The default upon creation is wkbUnknown which allows for
    any geometry type. The geometry type should generally not be changed
    after any OGRFeatures have been created against this definition.
    
    This function is the same as the C++ method
    OGRFeatureDefn::SetGeomType().
    
    Parameters:
    -----------
    
    hDefn:  handle to the layer or feature definition to set the geometry
    type to.
    
    eType:  the new type to assign.
    """
    pass

def FeatureDefn_SetStyleIgnored(FeatureDefn_self, int_bIgnored): # real signature unknown; restored from __doc__
    """
    FeatureDefn_SetStyleIgnored(FeatureDefn self, int bIgnored)
    
    void
    OGR_FD_SetStyleIgnored(OGRFeatureDefnH hDefn, int bIgnore)
    
    Set whether the style can be omitted when fetching features.
    
    This function is the same as the C++ method
    OGRFeatureDefn::SetStyleIgnored().
    
    Parameters:
    -----------
    
    hDefn:  hanlde to the feature definition on witch OGRFeature are based
    on.
    
    bIgnore:  ignore state
    """
    pass

def FeatureDefn_swigregister(*args, **kwargs): # real signature unknown
    pass

def Feature_Clone(Feature_self): # real signature unknown; restored from __doc__
    """
    Feature_Clone(Feature self) -> Feature
    
    OGRFeatureH OGR_F_Clone(OGRFeatureH
    hFeat)
    
    Duplicate feature.
    
    The newly created feature is owned by the caller, and will have it's
    own reference to the OGRFeatureDefn.
    
    This function is the same as the C++ method OGRFeature::Clone().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to clone.
    
    an handle to the new feature, exactly matching this feature.
    """
    pass

def Feature_DumpReadable(Feature_self): # real signature unknown; restored from __doc__
    """
    Feature_DumpReadable(Feature self)
    
    void
    OGR_F_DumpReadable(OGRFeatureH hFeat, FILE *fpOut)
    
    Dump this feature in a human readable form.
    
    This dumps the attributes, and geometry; however, it doesn't
    definition information (other than field types and names), nor does it
    report the geometry spatial reference system.
    
    This function is the same as the C++ method
    OGRFeature::DumpReadable().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to dump.
    
    fpOut:  the stream to write to, such as strout.
    """
    pass

def Feature_Equal(Feature_self, Feature_feature): # real signature unknown; restored from __doc__
    """
    Feature_Equal(Feature self, Feature feature) -> bool
    
    int OGR_F_Equal(OGRFeatureH hFeat,
    OGRFeatureH hOtherFeat)
    
    Test if two features are the same.
    
    Two features are considered equal if the share them (handle equality)
    same OGRFeatureDefn, have the same field values, and the same geometry
    (as tested by OGR_G_Equal()) as well as the same feature id.
    
    This function is the same as the C++ method OGRFeature::Equal().
    
    Parameters:
    -----------
    
    hFeat:  handle to one of the feature.
    
    hOtherFeat:  handle to the other feature to test this one against.
    
    TRUE if they are equal, otherwise FALSE.
    """
    return False

def Feature_GetDefnRef(Feature_self): # real signature unknown; restored from __doc__
    """
    Feature_GetDefnRef(Feature self) -> FeatureDefn
    
    OGRFeatureDefnH
    OGR_F_GetDefnRef(OGRFeatureH hFeat)
    
    Fetch feature definition.
    
    This function is the same as the C++ method OGRFeature::GetDefnRef().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to get the feature definition from.
    
    an handle to the feature definition object on which feature depends.
    """
    pass

def Feature_GetFID(Feature_self): # real signature unknown; restored from __doc__
    """
    Feature_GetFID(Feature self) -> int
    
    long OGR_F_GetFID(OGRFeatureH hFeat)
    
    Get feature identifier.
    
    This function is the same as the C++ method OGRFeature::GetFID().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature from which to get the feature
    identifier.
    
    feature id or OGRNullFID if none has been assigned.
    """
    return 0

def Feature_GetFieldAsDateTime(Feature_self, int_id): # real signature unknown; restored from __doc__
    """
    Feature_GetFieldAsDateTime(Feature self, int id)
    
    int
    OGR_F_GetFieldAsDateTime(OGRFeatureH hFeat, int iField, int *pnYear,
    int *pnMonth, int *pnDay, int *pnHour, int *pnMinute, int *pnSecond,
    int *pnTZFlag)
    
    Fetch field value as date and time.
    
    Currently this method only works for OFTDate, OFTTime and OFTDateTime
    fields.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldAsDateTime().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to fetch, from 0 to GetFieldCount()-1.
    
    pnYear:  (including century)
    
    pnMonth:  (1-12)
    
    pnDay:  (1-31)
    
    pnHour:  (0-23)
    
    pnMinute:  (0-59)
    
    pnSecond:  (0-59)
    
    pnTZFlag:  (0=unknown, 1=localtime, 100=GMT, see data model for
    details)
    
    TRUE on success or FALSE on failure.
    """
    pass

def Feature_GetFieldAsDouble(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    GetFieldAsDouble(int id) -> double
    Feature_GetFieldAsDouble(Feature self, char name) -> double
    
    double
    OGR_F_GetFieldAsDouble(OGRFeatureH hFeat, int iField)
    
    Fetch field value as a double.
    
    OFTString features will be translated using atof(). OFTInteger fields
    will be cast to double. Other field types, or errors will result in a
    return value of zero.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldAsDouble().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to fetch, from 0 to GetFieldCount()-1.
    
    the field value.
    """
    return 0.0

def Feature_GetFieldAsDoubleList(Feature_self, int_id): # real signature unknown; restored from __doc__
    """
    Feature_GetFieldAsDoubleList(Feature self, int id)
    
    const double*
    OGR_F_GetFieldAsDoubleList(OGRFeatureH hFeat, int iField, int
    *pnCount)
    
    Fetch field value as a list of doubles.
    
    Currently this function only works for OFTRealList fields.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldAsDoubleList().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to fetch, from 0 to GetFieldCount()-1.
    
    pnCount:  an integer to put the list count (number of doubles) into.
    
    the field value. This list is internal, and should not be modified, or
    freed. Its lifetime may be very brief. If *pnCount is zero on return
    the returned pointer may be NULL or non-NULL.
    """
    pass

def Feature_GetFieldAsInteger(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    GetFieldAsInteger(int id) -> int
    Feature_GetFieldAsInteger(Feature self, char name) -> int
    
    int
    OGR_F_GetFieldAsInteger(OGRFeatureH hFeat, int iField)
    
    Fetch field value as integer.
    
    OFTString features will be translated using atoi(). OFTReal fields
    will be cast to integer. Other field types, or errors will result in a
    return value of zero.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldAsInteger().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to fetch, from 0 to GetFieldCount()-1.
    
    the field value.
    """
    return 0

def Feature_GetFieldAsIntegerList(Feature_self, int_id): # real signature unknown; restored from __doc__
    """
    Feature_GetFieldAsIntegerList(Feature self, int id)
    
    const int*
    OGR_F_GetFieldAsIntegerList(OGRFeatureH hFeat, int iField, int
    *pnCount)
    
    Fetch field value as a list of integers.
    
    Currently this function only works for OFTIntegerList fields.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldAsIntegerList().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to fetch, from 0 to GetFieldCount()-1.
    
    pnCount:  an integer to put the list count (number of integers) into.
    
    the field value. This list is internal, and should not be modified, or
    freed. Its lifetime may be very brief. If *pnCount is zero on return
    the returned pointer may be NULL or non-NULL.
    """
    pass

def Feature_GetFieldAsString(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    GetFieldAsString(int id) -> char
    Feature_GetFieldAsString(Feature self, char name) -> char
    
    const char*
    OGR_F_GetFieldAsString(OGRFeatureH hFeat, int iField)
    
    Fetch field value as a string.
    
    OFTReal and OFTInteger fields will be translated to string using
    sprintf(), but not necessarily using the established formatting rules.
    Other field types, or errors will result in a return value of zero.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldAsString().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to fetch, from 0 to GetFieldCount()-1.
    
    the field value. This string is internal, and should not be modified,
    or freed. Its lifetime may be very brief.
    """
    return ""

def Feature_GetFieldAsStringList(Feature_self, int_id): # real signature unknown; restored from __doc__
    """
    Feature_GetFieldAsStringList(Feature self, int id) -> char
    
    char**
    OGR_F_GetFieldAsStringList(OGRFeatureH hFeat, int iField)
    
    Fetch field value as a list of strings.
    
    Currently this method only works for OFTStringList fields.
    
    The returned list is terminated by a NULL pointer. The number of
    elements can also be calculated using CSLCount().
    
    This function is the same as the C++ method
    OGRFeature::GetFieldAsStringList().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to fetch, from 0 to GetFieldCount()-1.
    
    the field value. This list is internal, and should not be modified, or
    freed. Its lifetime may be very brief.
    """
    return ""

def Feature_GetFieldCount(Feature_self): # real signature unknown; restored from __doc__
    """
    Feature_GetFieldCount(Feature self) -> int
    
    int
    OGR_F_GetFieldCount(OGRFeatureH hFeat)
    
    Fetch number of fields on this feature This will always be the same as
    the field count for the OGRFeatureDefn.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldCount().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to get the fields count from.
    
    count of fields.
    """
    return 0

def Feature_GetFieldDefnRef(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    GetFieldDefnRef(int id) -> FieldDefn
    Feature_GetFieldDefnRef(Feature self, char name) -> FieldDefn
    
    OGRFieldDefnH
    OGR_F_GetFieldDefnRef(OGRFeatureH hFeat, int i)
    
    Fetch definition for this field.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldDefnRef().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature on which the field is found.
    
    i:  the field to fetch, from 0 to GetFieldCount()-1.
    
    an handle to the field definition (from the OGRFeatureDefn). This is
    an internal reference, and should not be deleted or modified.
    """
    pass

def Feature_GetFieldIndex(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    Feature_GetFieldIndex(Feature self, char name) -> int
    
    int
    OGR_F_GetFieldIndex(OGRFeatureH hFeat, const char *pszName)
    
    Fetch the field index given field name.
    
    This is a cover for the OGRFeatureDefn::GetFieldIndex() method.
    
    This function is the same as the C++ method
    OGRFeature::GetFieldIndex().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature on which the field is found.
    
    pszName:  the name of the field to search for.
    
    the field index, or -1 if no matching field is found.
    """
    return 0

def Feature_GetFieldType(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    GetFieldType(int id) -> OGRFieldType
    Feature_GetFieldType(Feature self, char name) -> OGRFieldType
    """
    pass

def Feature_GetGeometryRef(Feature_self): # real signature unknown; restored from __doc__
    """
    Feature_GetGeometryRef(Feature self) -> Geometry
    
    OGRGeometryH
    OGR_F_GetGeometryRef(OGRFeatureH hFeat)
    
    Fetch an handle to feature geometry.
    
    This function is the same as the C++ method
    OGRFeature::GetGeometryRef().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to get geometry from.
    
    an handle to internal feature geometry. This object should not be
    modified.
    """
    pass

def Feature_GetStyleString(Feature_self): # real signature unknown; restored from __doc__
    """
    Feature_GetStyleString(Feature self) -> char
    
    const char*
    OGR_F_GetStyleString(OGRFeatureH hFeat)
    
    Fetch style string for this feature.
    
    Set the OGR Feature Style Specification for details on the format of
    this string, and ogr_featurestyle.h for services available to parse
    it.
    
    This function is the same as the C++ method
    OGRFeature::GetStyleString().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to get the style from.
    
    a reference to a representation in string format, or NULL if there
    isn't one.
    """
    return ""

def Feature_IsFieldSet(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    IsFieldSet(int id) -> bool
    Feature_IsFieldSet(Feature self, char name) -> bool
    
    int OGR_F_IsFieldSet(OGRFeatureH
    hFeat, int iField)
    
    Test if a field has ever been assigned a value or not.
    
    This function is the same as the C++ method OGRFeature::IsFieldSet().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature on which the field is.
    
    iField:  the field to test.
    
    TRUE if the field has been set, otherwise false.
    """
    return False

def Feature_SetFID(Feature_self, int_fid): # real signature unknown; restored from __doc__
    """
    Feature_SetFID(Feature self, int fid) -> OGRErr
    
    OGRErr OGR_F_SetFID(OGRFeatureH hFeat,
    long nFID)
    
    Set the feature identifier.
    
    For specific types of features this operation may fail on illegal
    features ids. Generally it always succeeds. Feature ids should be
    greater than or equal to zero, with the exception of OGRNullFID (-1)
    indicating that the feature id is unknown.
    
    This function is the same as the C++ method OGRFeature::SetFID().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to set the feature id to.
    
    nFID:  the new feature identifier value to assign.
    
    On success OGRERR_NONE, or on failure some other value.
    """
    pass

def Feature_SetField(Feature_self, char_name, int_year, int_month, int_day, int_hour, int_minute, int_second, int_tzflag): # real signature unknown; restored from __doc__
    """
    SetField(int id, char value)
    SetField(char name, char value)
    SetField(int id, int value)
    SetField(char name, int value)
    SetField(int id, double value)
    SetField(char name, double value)
    SetField(int id, int year, int month, int day, int hour, int minute, 
        int second, int tzflag)
    Feature_SetField(Feature self, char name, int year, int month, int day, 
        int hour, int minute, int second, int tzflag)
    """
    pass

def Feature_SetFieldDoubleList(Feature_self, int_id, int_nList): # real signature unknown; restored from __doc__
    """
    Feature_SetFieldDoubleList(Feature self, int id, int nList)
    
    void
    OGR_F_SetFieldDoubleList(OGRFeatureH hFeat, int iField, int nCount,
    double *padfValues)
    
    Set field to list of doubles value.
    
    This function currently on has an effect of OFTRealList fields.
    
    This function is the same as the C++ method OGRFeature::SetField().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to set, from 0 to GetFieldCount()-1.
    
    nCount:  the number of values in the list being assigned.
    
    padfValues:  the values to assign.
    """
    pass

def Feature_SetFieldIntegerList(Feature_self, int_id, int_nList): # real signature unknown; restored from __doc__
    """
    Feature_SetFieldIntegerList(Feature self, int id, int nList)
    
    void
    OGR_F_SetFieldIntegerList(OGRFeatureH hFeat, int iField, int nCount,
    int *panValues)
    
    Set field to list of integers value.
    
    This function currently on has an effect of OFTIntegerList fields.
    
    This function is the same as the C++ method OGRFeature::SetField().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to set, from 0 to GetFieldCount()-1.
    
    nCount:  the number of values in the list being assigned.
    
    panValues:  the values to assign.
    """
    pass

def Feature_SetFieldStringList(Feature_self, int_id, char_pList): # real signature unknown; restored from __doc__
    """
    Feature_SetFieldStringList(Feature self, int id, char pList)
    
    void
    OGR_F_SetFieldStringList(OGRFeatureH hFeat, int iField, char
    **papszValues)
    
    Set field to list of strings value.
    
    This function currently on has an effect of OFTStringList fields.
    
    This function is the same as the C++ method OGRFeature::SetField().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature that owned the field.
    
    iField:  the field to set, from 0 to GetFieldCount()-1.
    
    papszValues:  the values to assign.
    """
    pass

def Feature_SetFrom(Feature_self, Feature_other, int_forgiving=1): # real signature unknown; restored from __doc__
    """
    Feature_SetFrom(Feature self, Feature other, int forgiving = 1) -> OGRErr
    
    OGRErr OGR_F_SetFrom(OGRFeatureH
    hFeat, OGRFeatureH hOtherFeat, int bForgiving)
    
    Set one feature from another.
    
    Overwrite the contents of this feature from the geometry and
    attributes of another. The hOtherFeature does not need to have the
    same OGRFeatureDefn. Field values are copied by corresponding field
    names. Field types do not have to exactly match. OGR_F_SetField*()
    function conversion rules will be applied as needed.
    
    This function is the same as the C++ method OGRFeature::SetFrom().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to set to.
    
    hOtherFeat:  handle to the feature from which geometry, and field
    values will be copied.
    
    bForgiving:  TRUE if the operation should continue despite lacking
    output fields matching some of the source fields.
    
    OGRERR_NONE if the operation succeeds, even if some values are not
    transferred, otherwise an error code.
    """
    pass

def Feature_SetFromWithMap(Feature_self, Feature_other, int_forgiving, int_nList): # real signature unknown; restored from __doc__
    """
    Feature_SetFromWithMap(Feature self, Feature other, int forgiving, int nList) -> OGRErr
    
    OGRErr
    OGR_F_SetFromWithMap(OGRFeatureH hFeat, OGRFeatureH hOtherFeat, int
    bForgiving, int *panMap)
    
    Set one feature from another.
    
    Overwrite the contents of this feature from the geometry and
    attributes of another. The hOtherFeature does not need to have the
    same OGRFeatureDefn. Field values are copied according to the provided
    indices map. Field types do not have to exactly match.
    OGR_F_SetField*() function conversion rules will be applied as needed.
    This is more efficient than OGR_F_SetFrom() in that this doesn't
    lookup the fields by their names. Particularly useful when the field
    names don't match.
    
    This function is the same as the C++ method OGRFeature::SetFrom().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to set to.
    
    hOtherFeat:  handle to the feature from which geometry, and field
    values will be copied.
    
    panMap:  Array of the indices of the destination feature's fields
    stored at the corresponding index of the source feature's fields. A
    value of -1 should be used to ignore the source's field. The array
    should not be NULL and be as long as the number of fields in the
    source feature.
    
    bForgiving:  TRUE if the operation should continue despite lacking
    output fields matching some of the source fields.
    
    OGRERR_NONE if the operation succeeds, even if some values are not
    transferred, otherwise an error code.
    """
    pass

def Feature_SetGeometry(Feature_self, Geometry_geom): # real signature unknown; restored from __doc__
    """
    Feature_SetGeometry(Feature self, Geometry geom) -> OGRErr
    
    OGRErr
    OGR_F_SetGeometry(OGRFeatureH hFeat, OGRGeometryH hGeom)
    
    Set feature geometry.
    
    This function updates the features geometry, and operate exactly as
    SetGeometryDirectly(), except that this function does not assume
    ownership of the passed geometry, but instead makes a copy of it.
    
    This function is the same as the C++ OGRFeature::SetGeometry().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature on which new geometry is applied to.
    
    hGeom:  handle to the new geometry to apply to feature.
    
    OGRERR_NONE if successful, or OGR_UNSUPPORTED_GEOMETRY_TYPE if the
    geometry type is illegal for the OGRFeatureDefn (checking not yet
    implemented).
    """
    pass

def Feature_SetGeometryDirectly(Feature_self, Geometry_geom): # real signature unknown; restored from __doc__
    """
    Feature_SetGeometryDirectly(Feature self, Geometry geom) -> OGRErr
    
    OGRErr
    OGR_F_SetGeometryDirectly(OGRFeatureH hFeat, OGRGeometryH hGeom)
    
    Set feature geometry.
    
    This function updates the features geometry, and operate exactly as
    SetGeometry(), except that this function assumes ownership of the
    passed geometry.
    
    This function is the same as the C++ method
    OGRFeature::SetGeometryDirectly.
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature on which to apply the geometry.
    
    hGeom:  handle to the new geometry to apply to feature.
    
    OGRERR_NONE if successful, or OGR_UNSUPPORTED_GEOMETRY_TYPE if the
    geometry type is illegal for the OGRFeatureDefn (checking not yet
    implemented).
    """
    pass

def Feature_SetStyleString(Feature_self, char_the_string): # real signature unknown; restored from __doc__
    """
    Feature_SetStyleString(Feature self, char the_string)
    
    void
    OGR_F_SetStyleString(OGRFeatureH hFeat, const char *pszStyle)
    
    Set feature style string. This method operate exactly as
    OGR_F_SetStyleStringDirectly() except that it does not assume
    ownership of the passed string, but instead makes a copy of it.
    
    This function is the same as the C++ method
    OGRFeature::SetStyleString().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature to set style to.
    
    pszStyle:  the style string to apply to this feature, cannot be NULL.
    """
    pass

def Feature_swigregister(*args, **kwargs): # real signature unknown
    pass

def Feature_UnsetField(Feature_self, char_name): # real signature unknown; restored from __doc__
    """
    UnsetField(int id)
    Feature_UnsetField(Feature self, char name)
    
    void OGR_F_UnsetField(OGRFeatureH
    hFeat, int iField)
    
    Clear a field, marking it as unset.
    
    This function is the same as the C++ method OGRFeature::UnsetField().
    
    Parameters:
    -----------
    
    hFeat:  handle to the feature on which the field is.
    
    iField:  the field to unset.
    """
    pass

def FieldDefn_GetFieldTypeName(FieldDefn_self, OGRFieldType_type): # real signature unknown; restored from __doc__
    """ FieldDefn_GetFieldTypeName(FieldDefn self, OGRFieldType type) -> char """
    return ""

def FieldDefn_GetJustify(FieldDefn_self): # real signature unknown; restored from __doc__
    """
    FieldDefn_GetJustify(FieldDefn self) -> OGRJustification
    
    OGRJustification
    OGR_Fld_GetJustify(OGRFieldDefnH hDefn)
    
    Get the justification for this field.
    
    This function is the same as the CPP method
    OGRFieldDefn::GetJustify().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to get justification from.
    
    the justification.
    """
    pass

def FieldDefn_GetName(FieldDefn_self): # real signature unknown; restored from __doc__
    """ FieldDefn_GetName(FieldDefn self) -> char """
    return ""

def FieldDefn_GetNameRef(FieldDefn_self): # real signature unknown; restored from __doc__
    """
    FieldDefn_GetNameRef(FieldDefn self) -> char
    
    const char*
    OGR_Fld_GetNameRef(OGRFieldDefnH hDefn)
    
    Fetch name of this field.
    
    This function is the same as the CPP method
    OGRFieldDefn::GetNameRef().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition.
    
    the name of the field definition.
    """
    return ""

def FieldDefn_GetPrecision(FieldDefn_self): # real signature unknown; restored from __doc__
    """
    FieldDefn_GetPrecision(FieldDefn self) -> int
    
    int
    OGR_Fld_GetPrecision(OGRFieldDefnH hDefn)
    
    Get the formatting precision for this field. This should normally be
    zero for fields of types other than OFTReal.
    
    This function is the same as the CPP method
    OGRFieldDefn::GetPrecision().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to get precision from.
    
    the precision.
    """
    return 0

def FieldDefn_GetType(FieldDefn_self): # real signature unknown; restored from __doc__
    """
    FieldDefn_GetType(FieldDefn self) -> OGRFieldType
    
    OGRFieldType
    OGR_Fld_GetType(OGRFieldDefnH hDefn)
    
    Fetch type of this field.
    
    This function is the same as the CPP method OGRFieldDefn::GetType().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to get type from.
    
    field type.
    """
    pass

def FieldDefn_GetTypeName(FieldDefn_self): # real signature unknown; restored from __doc__
    """ FieldDefn_GetTypeName(FieldDefn self) -> char """
    return ""

def FieldDefn_GetWidth(FieldDefn_self): # real signature unknown; restored from __doc__
    """
    FieldDefn_GetWidth(FieldDefn self) -> int
    
    int OGR_Fld_GetWidth(OGRFieldDefnH
    hDefn)
    
    Get the formatting width for this field.
    
    This function is the same as the CPP method OGRFieldDefn::GetWidth().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to get width from.
    
    the width, zero means no specified width.
    """
    return 0

def FieldDefn_IsIgnored(FieldDefn_self): # real signature unknown; restored from __doc__
    """
    FieldDefn_IsIgnored(FieldDefn self) -> int
    
    int OGR_Fld_IsIgnored(OGRFieldDefnH
    hDefn)
    
    Return whether this field should be omitted when fetching features.
    
    This method is the same as the C++ method OGRFieldDefn::IsIgnored().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition
    
    ignore state
    """
    return 0

def FieldDefn_SetIgnored(FieldDefn_self, int_bIgnored): # real signature unknown; restored from __doc__
    """
    FieldDefn_SetIgnored(FieldDefn self, int bIgnored)
    
    void
    OGR_Fld_SetIgnored(OGRFieldDefnH hDefn, int ignore)
    
    Set whether this field should be omitted when fetching features.
    
    This method is the same as the C function OGRFieldDefn::SetIgnored().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition
    
    ignore:  ignore state
    """
    pass

def FieldDefn_SetJustify(FieldDefn_self, OGRJustification_justify): # real signature unknown; restored from __doc__
    """
    FieldDefn_SetJustify(FieldDefn self, OGRJustification justify)
    
    void
    OGR_Fld_SetJustify(OGRFieldDefnH hDefn, OGRJustification eJustify)
    
    Set the justification for this field.
    
    This function is the same as the CPP method
    OGRFieldDefn::SetJustify().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to set justification to.
    
    eJustify:  the new justification.
    """
    pass

def FieldDefn_SetName(FieldDefn_self, char_name): # real signature unknown; restored from __doc__
    """
    FieldDefn_SetName(FieldDefn self, char name)
    
    void OGR_Fld_SetName(OGRFieldDefnH
    hDefn, const char *pszName)
    
    Reset the name of this field.
    
    This function is the same as the CPP method OGRFieldDefn::SetName().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to apply the new name to.
    
    pszName:  the new name to apply.
    """
    pass

def FieldDefn_SetPrecision(FieldDefn_self, int_precision): # real signature unknown; restored from __doc__
    """
    FieldDefn_SetPrecision(FieldDefn self, int precision)
    
    void
    OGR_Fld_SetPrecision(OGRFieldDefnH hDefn, int nPrecision)
    
    Set the formatting precision for this field in characters.
    
    This should normally be zero for fields of types other than OFTReal.
    
    This function is the same as the CPP method
    OGRFieldDefn::SetPrecision().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to set precision to.
    
    nPrecision:  the new precision.
    """
    pass

def FieldDefn_SetType(FieldDefn_self, OGRFieldType_type): # real signature unknown; restored from __doc__
    """
    FieldDefn_SetType(FieldDefn self, OGRFieldType type)
    
    void OGR_Fld_SetType(OGRFieldDefnH
    hDefn, OGRFieldType eType)
    
    Set the type of this field. This should never be done to an
    OGRFieldDefn that is already part of an OGRFeatureDefn.
    
    This function is the same as the CPP method OGRFieldDefn::SetType().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to set type to.
    
    eType:  the new field type.
    """
    pass

def FieldDefn_SetWidth(FieldDefn_self, int_width): # real signature unknown; restored from __doc__
    """
    FieldDefn_SetWidth(FieldDefn self, int width)
    
    void OGR_Fld_SetWidth(OGRFieldDefnH
    hDefn, int nNewWidth)
    
    Set the formatting width for this field in characters.
    
    This function is the same as the CPP method OGRFieldDefn::SetWidth().
    
    Parameters:
    -----------
    
    hDefn:  handle to the field definition to set width to.
    
    nNewWidth:  the new width.
    """
    pass

def FieldDefn_swigregister(*args, **kwargs): # real signature unknown
    pass

def ForceToMultiLineString(Geometry_geom_in): # real signature unknown; restored from __doc__
    """ ForceToMultiLineString(Geometry geom_in) -> Geometry """
    pass

def ForceToMultiPoint(Geometry_geom_in): # real signature unknown; restored from __doc__
    """ ForceToMultiPoint(Geometry geom_in) -> Geometry """
    pass

def ForceToMultiPolygon(Geometry_geom_in): # real signature unknown; restored from __doc__
    """ ForceToMultiPolygon(Geometry geom_in) -> Geometry """
    pass

def ForceToPolygon(Geometry_geom_in): # real signature unknown; restored from __doc__
    """ ForceToPolygon(Geometry geom_in) -> Geometry """
    pass

def GeneralCmdLineProcessor(char_papszArgv, int_nOptions=0): # real signature unknown; restored from __doc__
    """ GeneralCmdLineProcessor(char papszArgv, int nOptions = 0) -> char """
    return ""

def GeometryTypeToName(OGRwkbGeometryType_eType): # real signature unknown; restored from __doc__
    """ GeometryTypeToName(OGRwkbGeometryType eType) -> char """
    return ""

def Geometry_AddGeometry(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """ Geometry_AddGeometry(Geometry self, Geometry other) -> OGRErr """
    pass

def Geometry_AddGeometryDirectly(Geometry_self, Geometry_other_disown): # real signature unknown; restored from __doc__
    """ Geometry_AddGeometryDirectly(Geometry self, Geometry other_disown) -> OGRErr """
    pass

def Geometry_AddPoint(Geometry_self, double_x, double_y, double_z=0): # real signature unknown; restored from __doc__
    """ Geometry_AddPoint(Geometry self, double x, double y, double z = 0) """
    pass

def Geometry_AddPoint_2D(Geometry_self, double_x, double_y): # real signature unknown; restored from __doc__
    """ Geometry_AddPoint_2D(Geometry self, double x, double y) """
    pass

def Geometry_Area(Geometry_self): # real signature unknown; restored from __doc__
    """ Geometry_Area(Geometry self) -> double """
    return 0.0

def Geometry_AssignSpatialReference(Geometry_self, SpatialReference_reference): # real signature unknown; restored from __doc__
    """
    Geometry_AssignSpatialReference(Geometry self, SpatialReference reference)
    
    void
    OGR_G_AssignSpatialReference(OGRGeometryH hGeom, OGRSpatialReferenceH
    hSRS)
    
    Assign spatial reference to this object.
    
    Any existing spatial reference is replaced, but under no circumstances
    does this result in the object being reprojected. It is just changing
    the interpretation of the existing geometry. Note that assigning a
    spatial reference increments the reference count on the
    OGRSpatialReference, but does not copy it.
    
    This is similar to the SFCOM IGeometry::put_SpatialReference() method.
    
    This function is the same as the CPP method
    OGRGeometry::assignSpatialReference.
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to apply the new spatial reference
    system.
    
    hSRS:  handle on the new spatial reference system to apply.
    """
    pass

def Geometry_Boundary(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_Boundary(Geometry self) -> Geometry
    
    OGRGeometryH
    OGR_G_Boundary(OGRGeometryH hTarget)
    
    Compute boundary.
    
    A new geometry object is created and returned containing the boundary
    of the geometry on which the method is invoked.
    
    This function is the same as the C++ method OGR_G_Boundary().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hTarget:  The Geometry to calculate the boundary of.
    
    a handle to a newly allocated geometry now owned by the caller, or
    NULL on failure.
    
    OGR 1.8.0
    """
    pass

def Geometry_Buffer(Geometry_self, double_distance, int_quadsecs=30): # real signature unknown; restored from __doc__
    """
    Geometry_Buffer(Geometry self, double distance, int quadsecs = 30) -> Geometry
    
    OGRGeometryH OGR_G_Buffer(OGRGeometryH
    hTarget, double dfDist, int nQuadSegs)
    
    Compute buffer of geometry.
    
    Builds a new geometry containing the buffer region around the geometry
    on which it is invoked. The buffer is a polygon containing the region
    within the buffer distance of the original geometry.
    
    Some buffer sections are properly described as curves, but are
    converted to approximate polygons. The nQuadSegs parameter can be used
    to control how many segements should be used to define a 90 degree
    curve - a quadrant of a circle. A value of 30 is a reasonable default.
    Large values result in large numbers of vertices in the resulting
    buffer geometry while small numbers reduce the accuracy of the result.
    
    This function is the same as the C++ method OGRGeometry::Buffer().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hTarget:  the geometry.
    
    dfDist:  the buffer distance to be applied.
    
    nQuadSegs:  the number of segments used to approximate a 90 degree
    (quadrant) of curvature.
    
    the newly created geometry, or NULL if an error occurs.
    """
    pass

def Geometry_Centroid(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_Centroid(Geometry self) -> Geometry
    
    int OGR_G_Centroid(OGRGeometryH
    hGeom, OGRGeometryH hCentroidPoint)
    
    Compute the geometry centroid.
    
    The centroid location is applied to the passed in OGRPoint object. The
    centroid is not necessarily within the geometry.
    
    This method relates to the SFCOM ISurface::get_Centroid() method
    however the current implementation based on GEOS can operate on other
    geometry types such as multipoint, linestring, geometrycollection such
    as multipolygons. OGC SF SQL 1.1 defines the operation for surfaces
    (polygons). SQL/MM-Part 3 defines the operation for surfaces and
    multisurfaces (multipolygons).
    
    This function is the same as the C++ method OGRGeometry::Centroid().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    OGRERR_NONE on success or OGRERR_FAILURE on error.
    """
    pass

def Geometry_Clone(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_Clone(Geometry self) -> Geometry
    
    OGRGeometryH OGR_G_Clone(OGRGeometryH
    hGeom)
    
    Make a copy of this object.
    
    This function relates to the SFCOM IGeometry::clone() method.
    
    This function is the same as the CPP method OGRGeometry::clone().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to clone from.
    
    an handle on the copy of the geometry with the spatial reference
    system as the original.
    """
    pass

def Geometry_CloseRings(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_CloseRings(Geometry self)
    
    void OGR_G_CloseRings(OGRGeometryH
    hGeom)
    
    Force rings to be closed.
    
    If this geometry, or any contained geometries has polygon rings that
    are not closed, they will be closed by adding the starting point at
    the end.
    
    Parameters:
    -----------
    
    hGeom:  handle to the geometry.
    """
    pass

def Geometry_Contains(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Contains(Geometry self, Geometry other) -> bool
    
    int OGR_G_Contains(OGRGeometryH
    hThis, OGRGeometryH hOther)
    
    Test for containment.
    
    Tests if this geometry contains the other geometry.
    
    This function is the same as the C++ method OGRGeometry::Contains().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry to compare.
    
    hOther:  the other geometry to compare.
    
    TRUE if hThis contains hOther geometry, otherwise FALSE.
    """
    return False

def Geometry_ConvexHull(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_ConvexHull(Geometry self) -> Geometry
    
    OGRGeometryH
    OGR_G_ConvexHull(OGRGeometryH hTarget)
    
    Compute convex hull.
    
    A new geometry object is created and returned containing the convex
    hull of the geometry on which the method is invoked.
    
    This function is the same as the C++ method OGRGeometry::ConvexHull().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hTarget:  The Geometry to calculate the convex hull of.
    
    a handle to a newly allocated geometry now owned by the caller, or
    NULL on failure.
    """
    pass

def Geometry_Crosses(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Crosses(Geometry self, Geometry other) -> bool
    
    int OGR_G_Crosses(OGRGeometryH hThis,
    OGRGeometryH hOther)
    
    Test for crossing.
    
    Tests if this geometry and the other geometry are crossing.
    
    This function is the same as the C++ method OGRGeometry::Crosses().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry to compare.
    
    hOther:  the other geometry to compare.
    
    TRUE if they are crossing, otherwise FALSE.
    """
    return False

def Geometry_Difference(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Difference(Geometry self, Geometry other) -> Geometry
    
    OGRGeometryH
    OGR_G_Difference(OGRGeometryH hThis, OGRGeometryH hOther)
    
    Compute difference.
    
    Generates a new geometry which is the region of this geometry with the
    region of the other geometry removed.
    
    This function is the same as the C++ method OGRGeometry::Difference().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry.
    
    hOther:  the other geometry.
    
    a new geometry representing the difference or NULL if the difference
    is empty or an error occurs.
    """
    pass

def Geometry_Disjoint(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Disjoint(Geometry self, Geometry other) -> bool
    
    int OGR_G_Disjoint(OGRGeometryH
    hThis, OGRGeometryH hOther)
    
    Test for disjointness.
    
    Tests if this geometry and the other geometry are disjoint.
    
    This function is the same as the C++ method OGRGeometry::Disjoint().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry to compare.
    
    hOther:  the other geometry to compare.
    
    TRUE if they are disjoint, otherwise FALSE.
    """
    return False

def Geometry_Distance(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Distance(Geometry self, Geometry other) -> double
    
    double OGR_G_Distance(OGRGeometryH
    hFirst, OGRGeometryH hOther)
    
    Compute distance between two geometries.
    
    Returns the shortest distance between the two geometries.
    
    This function is the same as the C++ method OGRGeometry::Distance().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hFirst:  the first geometry to compare against.
    
    hOther:  the other geometry to compare against.
    
    the distance between the geometries or -1 if an error occurs.
    """
    return 0.0

def Geometry_Empty(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_Empty(Geometry self)
    
    void OGR_G_Empty(OGRGeometryH hGeom)
    
    Clear geometry information. This restores the geometry to it's initial
    state after construction, and before assignment of actual geometry.
    
    This function relates to the SFCOM IGeometry::Empty() method.
    
    This function is the same as the CPP method OGRGeometry::empty().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to empty.
    """
    pass

def Geometry_Equal(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Equal(Geometry self, Geometry other) -> bool
    
    int OGR_G_Equal(OGRGeometryH hGeom,
    OGRGeometryH hOther)
    """
    return False

def Geometry_Equals(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Equals(Geometry self, Geometry other) -> bool
    
    int OGR_G_Equals(OGRGeometryH hGeom,
    OGRGeometryH hOther)
    
    Returns TRUE if two geometries are equivalent.
    
    This function is the same as the CPP method OGRGeometry::Equals()
    method.
    
    Parameters:
    -----------
    
    hGeom:  handle on the first geometry.
    
    hOther:  handle on the other geometry to test against.
    
    TRUE if equivalent or FALSE otherwise.
    """
    return False

def Geometry_ExportToGML(Geometry_self, char_options=None): # real signature unknown; restored from __doc__
    """ Geometry_ExportToGML(Geometry self, char options = None) -> retStringAndCPLFree """
    pass

def Geometry_ExportToJson(Geometry_self, char_options=None): # real signature unknown; restored from __doc__
    """ Geometry_ExportToJson(Geometry self, char options = None) -> retStringAndCPLFree """
    pass

def Geometry_ExportToKML(Geometry_self, char_altitude_mode=None): # real signature unknown; restored from __doc__
    """ Geometry_ExportToKML(Geometry self, char altitude_mode = None) -> retStringAndCPLFree """
    pass

def Geometry_ExportToWkb(Geometry_self, OGRwkbByteOrder_byte_order=None): # real signature unknown; restored from __doc__
    """
    Geometry_ExportToWkb(Geometry self, OGRwkbByteOrder byte_order = wkbXDR) -> OGRErr
    
    OGRErr
    OGR_G_ExportToWkb(OGRGeometryH hGeom, OGRwkbByteOrder eOrder, unsigned
    char *pabyDstBuffer)
    
    Convert a geometry into well known binary format.
    
    This function relates to the SFCOM IWks::ExportToWKB() method.
    
    This function is the same as the CPP method
    OGRGeometry::exportToWkb().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to convert to a well know binary data
    from.
    
    eOrder:  One of wkbXDR or wkbNDR indicating MSB or LSB byte order
    respectively.
    
    pabyDstBuffer:  a buffer into which the binary representation is
    written. This buffer must be at least OGR_G_WkbSize() byte in size.
    
    Currently OGRERR_NONE is always returned.
    """
    pass

def Geometry_ExportToWkt(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_ExportToWkt(Geometry self) -> OGRErr
    
    OGRErr
    OGR_G_ExportToWkt(OGRGeometryH hGeom, char **ppszSrcText)
    
    Convert a geometry into well known text format.
    
    This function relates to the SFCOM IWks::ExportToWKT() method.
    
    This function is the same as the CPP method
    OGRGeometry::exportToWkt().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to convert to a text format from.
    
    ppszSrcText:  a text buffer is allocated by the program, and assigned
    to the passed pointer.
    
    Currently OGRERR_NONE is always returned.
    """
    pass

def Geometry_FlattenTo2D(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_FlattenTo2D(Geometry self)
    
    void
    OGR_G_FlattenTo2D(OGRGeometryH hGeom)
    
    Convert geometry to strictly 2D. In a sense this converts all Z
    coordinates to 0.0.
    
    This function is the same as the CPP method
    OGRGeometry::flattenTo2D().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to convert.
    """
    pass

def Geometry_GetArea(Geometry_self): # real signature unknown; restored from __doc__
    """ Geometry_GetArea(Geometry self) -> double """
    return 0.0

def Geometry_GetBoundary(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetBoundary(Geometry self) -> Geometry
    
    OGRGeometryH
    OGR_G_GetBoundary(OGRGeometryH hTarget)
    
    Compute boundary (deprecated).
    
    Deprecated See:   OGR_G_Boundary()
    """
    pass

def Geometry_GetCoordinateDimension(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetCoordinateDimension(Geometry self) -> int
    
    int
    OGR_G_GetCoordinateDimension(OGRGeometryH hGeom)
    
    Get the dimension of the coordinates in this geometry.
    
    This function corresponds to the SFCOM IGeometry::GetDimension()
    method.
    
    This function is the same as the CPP method
    OGRGeometry::getCoordinateDimension().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to get the dimension of the coordinates
    from.
    
    in practice this will return 2 or 3. It can also return 0 in the case
    of an empty point.
    """
    return 0

def Geometry_GetDimension(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetDimension(Geometry self) -> int
    
    int
    OGR_G_GetDimension(OGRGeometryH hGeom)
    
    Get the dimension of this geometry.
    
    This function corresponds to the SFCOM IGeometry::GetDimension()
    method. It indicates the dimension of the geometry, but does not
    indicate the dimension of the underlying space (as indicated by
    OGR_G_GetCoordinateDimension() function).
    
    This function is the same as the CPP method
    OGRGeometry::getDimension().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to get the dimension from.
    
    0 for points, 1 for lines and 2 for surfaces.
    """
    return 0

def Geometry_GetEnvelope(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetEnvelope(Geometry self)
    
    void
    OGR_G_GetEnvelope(OGRGeometryH hGeom, OGREnvelope *psEnvelope)
    
    Computes and returns the bounding envelope for this geometry in the
    passed psEnvelope structure.
    
    This function is the same as the CPP method
    OGRGeometry::getEnvelope().
    
    Parameters:
    -----------
    
    hGeom:  handle of the geometry to get envelope from.
    
    psEnvelope:  the structure in which to place the results.
    """
    pass

def Geometry_GetEnvelope3D(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetEnvelope3D(Geometry self)
    
    void
    OGR_G_GetEnvelope3D(OGRGeometryH hGeom, OGREnvelope3D *psEnvelope)
    
    Computes and returns the bounding envelope (3D) for this geometry in
    the passed psEnvelope structure.
    
    This function is the same as the CPP method
    OGRGeometry::getEnvelope().
    
    Parameters:
    -----------
    
    hGeom:  handle of the geometry to get envelope from.
    
    psEnvelope:  the structure in which to place the results.
    
    OGR 1.9.0
    """
    pass

def Geometry_GetGeometryCount(Geometry_self): # real signature unknown; restored from __doc__
    """ Geometry_GetGeometryCount(Geometry self) -> int """
    return 0

def Geometry_GetGeometryName(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetGeometryName(Geometry self) -> char
    
    const char*
    OGR_G_GetGeometryName(OGRGeometryH hGeom)
    
    Fetch WKT name for geometry type.
    
    There is no SFCOM analog to this function.
    
    This function is the same as the CPP method
    OGRGeometry::getGeometryName().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to get name from.
    
    name used for this geometry type in well known text format.
    """
    return ""

def Geometry_GetGeometryRef(Geometry_self, int_geom): # real signature unknown; restored from __doc__
    """ Geometry_GetGeometryRef(Geometry self, int geom) -> Geometry """
    pass

def Geometry_GetGeometryType(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetGeometryType(Geometry self) -> OGRwkbGeometryType
    
    OGRwkbGeometryType
    OGR_G_GetGeometryType(OGRGeometryH hGeom)
    
    Fetch geometry type.
    
    Note that the geometry type may include the 2.5D flag. To get a 2D
    flattened version of the geometry type apply the wkbFlatten() macro to
    the return result.
    
    This function is the same as the CPP method
    OGRGeometry::getGeometryType().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to get type from.
    
    the geometry type code.
    """
    pass

def Geometry_GetPoint(Geometry_self, int_iPoint=0): # real signature unknown; restored from __doc__
    """ Geometry_GetPoint(Geometry self, int iPoint = 0) """
    pass

def Geometry_GetPointCount(Geometry_self): # real signature unknown; restored from __doc__
    """ Geometry_GetPointCount(Geometry self) -> int """
    return 0

def Geometry_GetPoints(Geometry_self, int_nCoordDimension=0): # real signature unknown; restored from __doc__
    """ Geometry_GetPoints(Geometry self, int nCoordDimension = 0) """
    pass

def Geometry_GetPoint_2D(Geometry_self, int_iPoint=0): # real signature unknown; restored from __doc__
    """ Geometry_GetPoint_2D(Geometry self, int iPoint = 0) """
    pass

def Geometry_GetSpatialReference(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_GetSpatialReference(Geometry self) -> SpatialReference
    
    OGRSpatialReferenceH
    OGR_G_GetSpatialReference(OGRGeometryH hGeom)
    
    Returns spatial reference system for geometry.
    
    This function relates to the SFCOM IGeometry::get_SpatialReference()
    method.
    
    This function is the same as the CPP method
    OGRGeometry::getSpatialReference().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to get spatial reference from.
    
    a reference to the spatial reference geometry.
    """
    pass

def Geometry_GetX(Geometry_self, int_point=0): # real signature unknown; restored from __doc__
    """ Geometry_GetX(Geometry self, int point = 0) -> double """
    return 0.0

def Geometry_GetY(Geometry_self, int_point=0): # real signature unknown; restored from __doc__
    """ Geometry_GetY(Geometry self, int point = 0) -> double """
    return 0.0

def Geometry_GetZ(Geometry_self, int_point=0): # real signature unknown; restored from __doc__
    """ Geometry_GetZ(Geometry self, int point = 0) -> double """
    return 0.0

def Geometry_Intersect(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Intersect(Geometry self, Geometry other) -> bool
    
    int OGR_G_Intersect(OGRGeometryH
    hGeom, OGRGeometryH hOtherGeom)
    """
    return False

def Geometry_Intersection(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Intersection(Geometry self, Geometry other) -> Geometry
    
    OGRGeometryH
    OGR_G_Intersection(OGRGeometryH hThis, OGRGeometryH hOther)
    
    Compute intersection.
    
    Generates a new geometry which is the region of intersection of the
    two geometries operated on. The OGR_G_Intersects() function can be
    used to test if two geometries intersect.
    
    This function is the same as the C++ method
    OGRGeometry::Intersection().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry.
    
    hOther:  the other geometry.
    
    a new geometry representing the intersection or NULL if there is no
    intersection or an error occurs.
    """
    pass

def Geometry_Intersects(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Intersects(Geometry self, Geometry other) -> bool
    
    int OGR_G_Intersects(OGRGeometryH
    hGeom, OGRGeometryH hOtherGeom)
    
    Do these features intersect?
    
    Currently this is not implemented in a rigerous fashion, and generally
    just tests whether the envelopes of the two features intersect.
    Eventually this will be made rigerous.
    
    This function is the same as the CPP method OGRGeometry::Intersects.
    
    Parameters:
    -----------
    
    hGeom:  handle on the first geometry.
    
    hOtherGeom:  handle on the other geometry to test against.
    
    TRUE if the geometries intersect, otherwise FALSE.
    """
    return False

def Geometry_IsEmpty(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_IsEmpty(Geometry self) -> bool
    
    int OGR_G_IsEmpty(OGRGeometryH hGeom)
    
    Test if the geometry is empty.
    
    This method is the same as the CPP method OGRGeometry::IsEmpty().
    
    Parameters:
    -----------
    
    hGeom:  The Geometry to test.
    
    TRUE if the geometry has no points, otherwise FALSE.
    """
    return False

def Geometry_IsRing(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_IsRing(Geometry self) -> bool
    
    int OGR_G_IsRing(OGRGeometryH hGeom)
    
    Test if the geometry is a ring.
    
    This function is the same as the C++ method OGRGeometry::IsRing().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always return FALSE.
    
    Parameters:
    -----------
    
    hGeom:  The Geometry to test.
    
    TRUE if the geometry has no points, otherwise FALSE.
    """
    return False

def Geometry_IsSimple(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_IsSimple(Geometry self) -> bool
    
    int OGR_G_IsSimple(OGRGeometryH
    hGeom)
    
    Returns TRUE if the geometry is simple.
    
    Returns TRUE if the geometry has no anomalous geometric points, such
    as self intersection or self tangency. The description of each
    instantiable geometric class will include the specific conditions that
    cause an instance of that class to be classified as not simple.
    
    This function is the same as the c++ method OGRGeometry::IsSimple()
    method.
    
    If OGR is built without the GEOS library, this function will always
    return FALSE.
    
    Parameters:
    -----------
    
    hGeom:  The Geometry to test.
    
    TRUE if object is simple, otherwise FALSE.
    """
    return False

def Geometry_IsValid(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_IsValid(Geometry self) -> bool
    
    int OGR_G_IsValid(OGRGeometryH hGeom)
    
    Test if the geometry is valid.
    
    This function is the same as the C++ method OGRGeometry::IsValid().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always return FALSE.
    
    Parameters:
    -----------
    
    hGeom:  The Geometry to test.
    
    TRUE if the geometry has no points, otherwise FALSE.
    """
    return False

def Geometry_Length(Geometry_self): # real signature unknown; restored from __doc__
    """ Geometry_Length(Geometry self) -> double """
    return 0.0

def Geometry_Overlaps(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Overlaps(Geometry self, Geometry other) -> bool
    
    int OGR_G_Overlaps(OGRGeometryH
    hThis, OGRGeometryH hOther)
    
    Test for overlap.
    
    Tests if this geometry and the other geometry overlap, that is their
    intersection has a non-zero area.
    
    This function is the same as the C++ method OGRGeometry::Overlaps().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry to compare.
    
    hOther:  the other geometry to compare.
    
    TRUE if they are overlapping, otherwise FALSE.
    """
    return False

def Geometry_Segmentize(Geometry_self, double_dfMaxLength): # real signature unknown; restored from __doc__
    """
    Geometry_Segmentize(Geometry self, double dfMaxLength)
    
    void OGR_G_Segmentize(OGRGeometryH
    hGeom, double dfMaxLength)
    
    Modify the geometry such it has no segment longer then the given
    distance.
    
    Interpolated points will have Z and M values (if needed) set to 0.
    Distance computation is performed in 2d only
    
    This function is the same as the CPP method OGRGeometry::segmentize().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to segmentize
    
    dfMaxLength:  the maximum distance between 2 points after
    segmentization
    """
    pass

def Geometry_SetCoordinateDimension(Geometry_self, int_dimension): # real signature unknown; restored from __doc__
    """
    Geometry_SetCoordinateDimension(Geometry self, int dimension)
    
    void
    OGR_G_SetCoordinateDimension(OGRGeometryH hGeom, int nNewDimension)
    
    Set the coordinate dimension.
    
    This method sets the explicit coordinate dimension. Setting the
    coordinate dimension of a geometry to 2 should zero out any existing Z
    values. Setting the dimension of a geometry collection will not
    necessarily affect the children geometries.
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to set the dimension of the
    coordinates.
    
    nNewDimension:  New coordinate dimension value, either 2 or 3.
    """
    pass

def Geometry_SetPoint(Geometry_self, int_point, double_x, double_y, double_z=0): # real signature unknown; restored from __doc__
    """ Geometry_SetPoint(Geometry self, int point, double x, double y, double z = 0) """
    pass

def Geometry_SetPoint_2D(Geometry_self, int_point, double_x, double_y): # real signature unknown; restored from __doc__
    """ Geometry_SetPoint_2D(Geometry self, int point, double x, double y) """
    pass

def Geometry_Simplify(Geometry_self, double_tolerance): # real signature unknown; restored from __doc__
    """
    Geometry_Simplify(Geometry self, double tolerance) -> Geometry
    
    OGRGeometryH
    OGR_G_Simplify(OGRGeometryH hThis, double dTolerance)
    
    Compute a simplified geometry.
    
    This function is the same as the C++ method OGRGeometry::Simplify().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry.
    
    dTolerance:  the distance tolerance for the simplification.
    
    the simplified geometry or NULL if an error occurs.
    
    OGR 1.8.0
    """
    pass

def Geometry_SimplifyPreserveTopology(Geometry_self, double_tolerance): # real signature unknown; restored from __doc__
    """
    Geometry_SimplifyPreserveTopology(Geometry self, double tolerance) -> Geometry
    
    OGRGeometryH
    OGR_G_SimplifyPreserveTopology(OGRGeometryH hThis, double dTolerance)
    
    Compute a simplified geometry.
    
    This function is the same as the C++ method
    OGRGeometry::SimplifyPreserveTopology().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry.
    
    dTolerance:  the distance tolerance for the simplification.
    
    the simplified geometry or NULL if an error occurs.
    
    OGR 1.9.0
    """
    pass

def Geometry_swigregister(*args, **kwargs): # real signature unknown
    pass

def Geometry_SymDifference(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_SymDifference(Geometry self, Geometry other) -> Geometry
    
    OGRGeometryH
    OGR_G_SymDifference(OGRGeometryH hThis, OGRGeometryH hOther)
    
    Compute symmetric difference.
    
    Generates a new geometry which is the symmetric difference of this
    geometry and the other geometry.
    
    This function is the same as the C++ method
    OGRGeometry::SymmetricDifference().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry.
    
    hOther:  the other geometry.
    
    a new geometry representing the symmetric difference or NULL if the
    difference is empty or an error occurs.
    
    OGR 1.8.0
    """
    pass

def Geometry_SymmetricDifference(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_SymmetricDifference(Geometry self, Geometry other) -> Geometry
    
    OGRGeometryH
    OGR_G_SymmetricDifference(OGRGeometryH hThis, OGRGeometryH hOther)
    
    Compute symmetric difference (deprecated).
    
    Deprecated See:   OGR_G_SymmetricDifference()
    """
    pass

def Geometry_Touches(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Touches(Geometry self, Geometry other) -> bool
    
    int OGR_G_Touches(OGRGeometryH hThis,
    OGRGeometryH hOther)
    
    Test for touching.
    
    Tests if this geometry and the other geometry are touching.
    
    This function is the same as the C++ method OGRGeometry::Touches().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry to compare.
    
    hOther:  the other geometry to compare.
    
    TRUE if they are touching, otherwise FALSE.
    """
    return False

def Geometry_Transform(Geometry_self, CoordinateTransformation_trans): # real signature unknown; restored from __doc__
    """
    Geometry_Transform(Geometry self, CoordinateTransformation trans) -> OGRErr
    
    OGRErr OGR_G_Transform(OGRGeometryH
    hGeom, OGRCoordinateTransformationH hTransform)
    
    Apply arbitrary coordinate transformation to geometry.
    
    This function will transform the coordinates of a geometry from their
    current spatial reference system to a new target spatial reference
    system. Normally this means reprojecting the vectors, but it could
    include datum shifts, and changes of units.
    
    Note that this function does not require that the geometry already
    have a spatial reference system. It will be assumed that they can be
    treated as having the source spatial reference system of the
    OGRCoordinateTransformation object, and the actual SRS of the geometry
    will be ignored. On successful completion the output
    OGRSpatialReference of the OGRCoordinateTransformation will be
    assigned to the geometry.
    
    This function is the same as the CPP method OGRGeometry::transform.
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to apply the transform to.
    
    hTransform:  handle on the transformation to apply.
    
    OGRERR_NONE on success or an error code.
    """
    pass

def Geometry_TransformTo(Geometry_self, SpatialReference_reference): # real signature unknown; restored from __doc__
    """
    Geometry_TransformTo(Geometry self, SpatialReference reference) -> OGRErr
    
    OGRErr
    OGR_G_TransformTo(OGRGeometryH hGeom, OGRSpatialReferenceH hSRS)
    
    Transform geometry to new spatial reference system.
    
    This function will transform the coordinates of a geometry from their
    current spatial reference system to a new target spatial reference
    system. Normally this means reprojecting the vectors, but it could
    include datum shifts, and changes of units.
    
    This function will only work if the geometry already has an assigned
    spatial reference system, and if it is transformable to the target
    coordinate system.
    
    Because this function requires internal creation and initialization of
    an OGRCoordinateTransformation object it is significantly more
    expensive to use this function to transform many geometries than it is
    to create the OGRCoordinateTransformation in advance, and call
    transform() with that transformation. This function exists primarily
    for convenience when only transforming a single geometry.
    
    This function is the same as the CPP method OGRGeometry::transformTo.
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to apply the transform to.
    
    hSRS:  handle on the spatial reference system to apply.
    
    OGRERR_NONE on success, or an error code.
    """
    pass

def Geometry_Union(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Union(Geometry self, Geometry other) -> Geometry
    
    OGRGeometryH OGR_G_Union(OGRGeometryH
    hThis, OGRGeometryH hOther)
    
    Compute union.
    
    Generates a new geometry which is the region of union of the two
    geometries operated on.
    
    This function is the same as the C++ method OGRGeometry::Union().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry.
    
    hOther:  the other geometry.
    
    a new geometry representing the union or NULL if an error occurs.
    """
    pass

def Geometry_UnionCascaded(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_UnionCascaded(Geometry self) -> Geometry
    
    OGRGeometryH
    OGR_G_UnionCascaded(OGRGeometryH hThis)
    
    Compute union using cascading.
    
    This function is the same as the C++ method
    OGRGeometry::UnionCascaded().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry.
    
    a new geometry representing the union or NULL if an error occurs.
    """
    pass

def Geometry_Within(Geometry_self, Geometry_other): # real signature unknown; restored from __doc__
    """
    Geometry_Within(Geometry self, Geometry other) -> bool
    
    int OGR_G_Within(OGRGeometryH hThis,
    OGRGeometryH hOther)
    
    Test for containment.
    
    Tests if this geometry is within the other geometry.
    
    This function is the same as the C++ method OGRGeometry::Within().
    
    This function is built on the GEOS library, check it for the
    definition of the geometry operation. If OGR is built without the GEOS
    library, this function will always fail, issuing a CPLE_NotSupported
    error.
    
    Parameters:
    -----------
    
    hThis:  the geometry to compare.
    
    hOther:  the other geometry to compare.
    
    TRUE if hThis is within hOther, otherwise FALSE.
    """
    return False

def Geometry_WkbSize(Geometry_self): # real signature unknown; restored from __doc__
    """
    Geometry_WkbSize(Geometry self) -> int
    
    int OGR_G_WkbSize(OGRGeometryH hGeom)
    
    Returns size of related binary representation.
    
    This function returns the exact number of bytes required to hold the
    well known binary representation of this geometry object. Its
    computation may be slightly expensive for complex geometries.
    
    This function relates to the SFCOM IWks::WkbSize() method.
    
    This function is the same as the CPP method OGRGeometry::WkbSize().
    
    Parameters:
    -----------
    
    hGeom:  handle on the geometry to get the binary size from.
    
    size of binary representation in bytes.
    """
    return 0

def GetDriver(int_driver_number): # real signature unknown; restored from __doc__
    """ GetDriver(int driver_number) -> Driver """
    pass

def GetDriverByName(char_name): # real signature unknown; restored from __doc__
    """ GetDriverByName(char name) -> Driver """
    pass

def GetDriverCount(): # real signature unknown; restored from __doc__
    """ GetDriverCount() -> int """
    return 0

def GetFieldTypeName(OGRFieldType_type): # real signature unknown; restored from __doc__
    """ GetFieldTypeName(OGRFieldType type) -> char """
    return ""

def GetOpenDS(int_ds_number): # real signature unknown; restored from __doc__
    """ GetOpenDS(int ds_number) -> DataSource """
    pass

def GetOpenDSCount(): # real signature unknown; restored from __doc__
    """ GetOpenDSCount() -> int """
    return 0

def GetUseExceptions(): # real signature unknown; restored from __doc__
    """ GetUseExceptions() -> int """
    return 0

def Layer_AlterFieldDefn(Layer_self, int_iField, FieldDefn_field_def, int_nFlags): # real signature unknown; restored from __doc__
    """
    Layer_AlterFieldDefn(Layer self, int iField, FieldDefn field_def, int nFlags) -> OGRErr
    
    OGRErr
    OGR_L_AlterFieldDefn(OGRLayerH hLayer, int iField, OGRFieldDefnH
    hNewFieldDefn, int nFlags)
    
    Alter the definition of an existing field on a layer.
    
    You must use this to alter the definition of an existing field of a
    real layer. Internally the OGRFeatureDefn for the layer will be
    updated to reflect the altered field. Applications should never modify
    the OGRFeatureDefn used by a layer directly.
    
    This function should not be called while there are feature objects in
    existance that were obtained or created with the previous layer
    definition.
    
    Not all drivers support this function. You can query a layer to check
    if it supports it with the OLCAlterFieldDefn capability. Some drivers
    may only support this method while there are still no features in the
    layer. When it is supported, the existings features of the backing
    file/database should be updated accordingly. Some drivers might also
    not support all update flags.
    
    This function is the same as the C++ method
    OGRLayer::AlterFieldDefn().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer.
    
    iField:  index of the field whose definition must be altered.
    
    hNewFieldDefn:  new field definition
    
    nFlags:  combination of ALTER_NAME_FLAG, ALTER_TYPE_FLAG and
    ALTER_WIDTH_PRECISION_FLAG to indicate which of the name and/or type
    and/or width and precision fields from the new field definition must
    be taken into account.
    
    OGRERR_NONE on success.
    
    OGR 1.9.0
    """
    pass

def Layer_CommitTransaction(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_CommitTransaction(Layer self) -> OGRErr
    
    OGRErr
    OGR_L_CommitTransaction(OGRLayerH hLayer)
    
    For datasources which support transactions, CommitTransaction commits
    a transaction.
    
    If no transaction is active, or the commit fails, will return
    OGRERR_FAILURE. Datasources which do not support transactions will
    always return OGRERR_NONE.
    
    This function is the same as the C++ method
    OGRLayer::CommitTransaction().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    OGRERR_NONE on success.
    """
    pass

def Layer_CreateFeature(Layer_self, Feature_feature): # real signature unknown; restored from __doc__
    """
    Layer_CreateFeature(Layer self, Feature feature) -> OGRErr
    
    OGRErr
    OGR_L_CreateFeature(OGRLayerH hLayer, OGRFeatureH hFeat)
    
    Create and write a new feature within a layer.
    
    The passed feature is written to the layer as a new feature, rather
    than overwriting an existing one. If the feature has a feature id
    other than OGRNullFID, then the native implementation may use that as
    the feature id of the new feature, but not necessarily. Upon
    successful return the passed feature will have been updated with the
    new feature id.
    
    This function is the same as the C++ method OGRLayer::CreateFeature().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer to write the feature to.
    
    hFeat:  the handle of the feature to write to disk.
    
    OGRERR_NONE on success.
    """
    pass

def Layer_CreateField(Layer_self, FieldDefn_field_def, int_approx_ok=1): # real signature unknown; restored from __doc__
    """
    Layer_CreateField(Layer self, FieldDefn field_def, int approx_ok = 1) -> OGRErr
    
    OGRErr
    OGR_L_CreateField(OGRLayerH hLayer, OGRFieldDefnH hField, int
    bApproxOK)
    
    Create a new field on a layer.
    
    You must use this to create new fields on a real layer. Internally the
    OGRFeatureDefn for the layer will be updated to reflect the new field.
    Applications should never modify the OGRFeatureDefn used by a layer
    directly.
    
    This function should not be called while there are feature objects in
    existance that were obtained or created with the previous layer
    definition.
    
    Not all drivers support this function. You can query a layer to check
    if it supports it with the OLCCreateField capability. Some drivers may
    only support this method while there are still no features in the
    layer. When it is supported, the existings features of the backing
    file/database should be updated accordingly.
    
    This function is the same as the C++ method OGRLayer::CreateField().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer to write the field definition.
    
    hField:  handle of the field definition to write to disk.
    
    bApproxOK:  If TRUE, the field may be created in a slightly different
    form depending on the limitations of the format driver.
    
    OGRERR_NONE on success.
    """
    pass

def Layer_DeleteFeature(Layer_self, long_fid): # real signature unknown; restored from __doc__
    """
    Layer_DeleteFeature(Layer self, long fid) -> OGRErr
    
    OGRErr
    OGR_L_DeleteFeature(OGRLayerH hDS, long nFID)
    
    Delete feature from layer.
    
    The feature with the indicated feature id is deleted from the layer if
    supported by the driver. Most drivers do not support feature deletion,
    and will return OGRERR_UNSUPPORTED_OPERATION. The
    OGR_L_TestCapability() function may be called with OLCDeleteFeature to
    check if the driver supports feature deletion.
    
    This method is the same as the C++ method OGRLayer::DeleteFeature().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    nFID:  the feature id to be deleted from the layer
    
    OGRERR_NONE on success.
    """
    pass

def Layer_DeleteField(Layer_self, int_iField): # real signature unknown; restored from __doc__
    """
    Layer_DeleteField(Layer self, int iField) -> OGRErr
    
    OGRErr
    OGR_L_DeleteField(OGRLayerH hLayer, int iField)
    
    Create a new field on a layer.
    
    You must use this to delete existing fields on a real layer.
    Internally the OGRFeatureDefn for the layer will be updated to reflect
    the deleted field. Applications should never modify the OGRFeatureDefn
    used by a layer directly.
    
    This function should not be called while there are feature objects in
    existance that were obtained or created with the previous layer
    definition.
    
    Not all drivers support this function. You can query a layer to check
    if it supports it with the OLCDeleteField capability. Some drivers may
    only support this method while there are still no features in the
    layer. When it is supported, the existings features of the backing
    file/database should be updated accordingly.
    
    This function is the same as the C++ method OGRLayer::DeleteField().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer.
    
    iField:  index of the field to delete.
    
    OGRERR_NONE on success.
    
    OGR 1.9.0
    """
    pass

def Layer_GetExtent(Layer_self, int_force=1, int_can_return_null=0): # real signature unknown; restored from __doc__
    """
    Layer_GetExtent(Layer self, int force = 1, int can_return_null = 0)
    
    OGRErr OGR_L_GetExtent(OGRLayerH
    hLayer, OGREnvelope *psExtent, int bForce)
    
    Fetch the extent of this layer.
    
    Returns the extent (MBR) of the data in the layer. If bForce is FALSE,
    and it would be expensive to establish the extent then OGRERR_FAILURE
    will be returned indicating that the extent isn't know. If bForce is
    TRUE then some implementations will actually scan the entire layer
    once to compute the MBR of all the features in the layer.
    
    Depending on the drivers, the returned extent may or may not take the
    spatial filter into account. So it is safer to call OGR_L_GetExtent()
    without setting a spatial filter.
    
    Layers without any geometry may return OGRERR_FAILURE just indicating
    that no meaningful extents could be collected.
    
    Note that some implementations of this method may alter the read
    cursor of the layer.
    
    This function is the same as the C++ method OGRLayer::GetExtent().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer from which to get extent.
    
    psExtent:  the structure in which the extent value will be returned.
    
    bForce:  Flag indicating whether the extent should be computed even if
    it is expensive.
    
    OGRERR_NONE on success, OGRERR_FAILURE if extent not known.
    """
    pass

def Layer_GetFeature(Layer_self, long_fid): # real signature unknown; restored from __doc__
    """
    Layer_GetFeature(Layer self, long fid) -> Feature
    
    OGRFeatureH
    OGR_L_GetFeature(OGRLayerH hLayer, long nFeatureId)
    
    Fetch a feature by its identifier.
    
    This function will attempt to read the identified feature. The nFID
    value cannot be OGRNullFID. Success or failure of this operation is
    unaffected by the spatial or attribute filters.
    
    If this function returns a non-NULL feature, it is guaranteed that its
    feature id ( OGR_F_GetFID()) will be the same as nFID.
    
    Use OGR_L_TestCapability(OLCRandomRead) to establish if this layer
    supports efficient random access reading via OGR_L_GetFeature();
    however, the call should always work if the feature exists as a
    fallback implementation just scans all the features in the layer
    looking for the desired feature.
    
    Sequential reads are generally considered interrupted by a
    OGR_L_GetFeature() call.
    
    The returned feature should be free with OGR_F_Destroy().
    
    This function is the same as the C++ method OGRLayer::GetFeature( ).
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer that owned the feature.
    
    nFeatureId:  the feature id of the feature to read.
    
    an handle to a feature now owned by the caller, or NULL on failure.
    """
    pass

def Layer_GetFeatureCount(Layer_self, int_force=1): # real signature unknown; restored from __doc__
    """
    Layer_GetFeatureCount(Layer self, int force = 1) -> int
    
    int
    OGR_L_GetFeatureCount(OGRLayerH hLayer, int bForce)
    
    Fetch the feature count in this layer.
    
    Returns the number of features in the layer. For dynamic databases the
    count may not be exact. If bForce is FALSE, and it would be expensive
    to establish the feature count a value of -1 may be returned
    indicating that the count isn't know. If bForce is TRUE some
    implementations will actually scan the entire layer once to count
    objects.
    
    The returned count takes the spatial filter into account.
    
    Note that some implementations of this method may alter the read
    cursor of the layer.
    
    This function is the same as the CPP OGRLayer::GetFeatureCount().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer that owned the features.
    
    bForce:  Flag indicating whether the count should be computed even if
    it is expensive.
    
    feature count, -1 if count not known.
    """
    return 0

def Layer_GetFeaturesRead(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetFeaturesRead(Layer self) -> GIntBig
    
    GIntBig
    OGR_L_GetFeaturesRead(OGRLayerH hLayer)
    """
    pass

def Layer_GetFIDColumn(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetFIDColumn(Layer self) -> char
    
    const char*
    OGR_L_GetFIDColumn(OGRLayerH hLayer)
    
    This method returns the name of the underlying database column being
    used as the FID column, or "" if not supported.
    
    This method is the same as the C++ method OGRLayer::GetFIDColumn()
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    fid column name.
    """
    return ""

def Layer_GetGeometryColumn(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetGeometryColumn(Layer self) -> char
    
    const char*
    OGR_L_GetGeometryColumn(OGRLayerH hLayer)
    
    This method returns the name of the underlying database column being
    used as the geometry column, or "" if not supported.
    
    This method is the same as the C++ method
    OGRLayer::GetGeometryColumn()
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    geometry column name.
    """
    return ""

def Layer_GetGeomType(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetGeomType(Layer self) -> OGRwkbGeometryType
    
    OGRwkbGeometryType
    OGR_L_GetGeomType(OGRLayerH hLayer)
    
    Return the layer geometry type.
    
    This returns the same result as
    OGR_FD_GetGeomType(OGR_L_GetLayerDefn(hLayer)), but for a few drivers,
    calling OGR_L_GetGeomType() directly can avoid lengthy layer
    definition initialization.
    
    This function is the same as the C++ method OGRLayer::GetGeomType().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer.
    
    the geometry type
    
    OGR 1.8.0
    """
    pass

def Layer_GetLayerDefn(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetLayerDefn(Layer self) -> FeatureDefn
    
    OGRFeatureDefnH
    OGR_L_GetLayerDefn(OGRLayerH hLayer)
    
    Fetch the schema information for this layer.
    
    The returned handle to the OGRFeatureDefn is owned by the OGRLayer,
    and should not be modified or freed by the application. It
    encapsulates the attribute schema of the features of the layer.
    
    This function is the same as the C++ method OGRLayer::GetLayerDefn().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer to get the schema information.
    
    an handle to the feature definition.
    """
    pass

def Layer_GetName(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetName(Layer self) -> char
    
    const char* OGR_L_GetName(OGRLayerH
    hLayer)
    
    Return the layer name.
    
    This returns the same content as
    OGR_FD_GetName(OGR_L_GetLayerDefn(hLayer)), but for a few drivers,
    calling OGR_L_GetName() directly can avoid lengthy layer definition
    initialization.
    
    This function is the same as the C++ method OGRLayer::GetName().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer.
    
    the layer name (must not been freed)
    
    OGR 1.8.0
    """
    return ""

def Layer_GetNextFeature(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetNextFeature(Layer self) -> Feature
    
    OGRFeatureH
    OGR_L_GetNextFeature(OGRLayerH hLayer)
    
    Fetch the next available feature from this layer.
    
    The returned feature becomes the responsiblity of the caller to delete
    with OGR_F_Destroy(). It is critical that all features associated with
    an OGRLayer (more specifically an OGRFeatureDefn) be deleted before
    that layer/datasource is deleted.
    
    Only features matching the current spatial filter (set with
    SetSpatialFilter()) will be returned.
    
    This function implements sequential access to the features of a layer.
    The OGR_L_ResetReading() function can be used to start at the
    beginning again.
    
    This function is the same as the C++ method
    OGRLayer::GetNextFeature().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer from which feature are read.
    
    an handle to a feature, or NULL if no more features are available.
    """
    pass

def Layer_GetRefCount(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetRefCount(Layer self) -> int
    
    int OGR_L_GetRefCount(OGRLayerH
    hLayer)
    """
    return 0

def Layer_GetSpatialFilter(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetSpatialFilter(Layer self) -> Geometry
    
    OGRGeometryH
    OGR_L_GetSpatialFilter(OGRLayerH hLayer)
    
    This function returns the current spatial filter for this layer.
    
    The returned pointer is to an internally owned object, and should not
    be altered or deleted by the caller.
    
    This function is the same as the C++ method
    OGRLayer::GetSpatialFilter().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer to get the spatial filter from.
    
    an handle to the spatial filter geometry.
    """
    pass

def Layer_GetSpatialRef(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_GetSpatialRef(Layer self) -> SpatialReference
    
    OGRSpatialReferenceH
    OGR_L_GetSpatialRef(OGRLayerH hLayer)
    
    Fetch the spatial reference system for this layer.
    
    The returned object is owned by the OGRLayer and should not be
    modified or freed by the application.
    
    This function is the same as the C++ method OGRLayer::GetSpatialRef().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer to get the spatial reference from.
    
    spatial reference, or NULL if there isn't one.
    """
    pass

def Layer_ReorderField(Layer_self, int_iOldFieldPos, int_iNewFieldPos): # real signature unknown; restored from __doc__
    """
    Layer_ReorderField(Layer self, int iOldFieldPos, int iNewFieldPos) -> OGRErr
    
    OGRErr
    OGR_L_ReorderField(OGRLayerH hLayer, int iOldFieldPos, int
    iNewFieldPos)
    
    Reorder an existing field on a layer.
    
    This function is a conveniency wrapper of OGR_L_ReorderFields()
    dedicated to move a single field.
    
    You must use this to reorder existing fields on a real layer.
    Internally the OGRFeatureDefn for the layer will be updated to reflect
    the reordering of the fields. Applications should never modify the
    OGRFeatureDefn used by a layer directly.
    
    This function should not be called while there are feature objects in
    existance that were obtained or created with the previous layer
    definition.
    
    The field definition that was at initial position iOldFieldPos will be
    moved at position iNewFieldPos, and elements between will be shuffled
    accordingly.
    
    For example, let suppose the fields were "0","1","2","3","4"
    initially. ReorderField(1, 3) will reorder them as
    "0","2","3","1","4".
    
    Not all drivers support this function. You can query a layer to check
    if it supports it with the OLCReorderFields capability. Some drivers
    may only support this method while there are still no features in the
    layer. When it is supported, the existings features of the backing
    file/database should be updated accordingly.
    
    This function is the same as the C++ method OGRLayer::ReorderField().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer.
    
    iOldFieldPos:  previous position of the field to move. Must be in the
    range [0,GetFieldCount()-1].
    
    iNewFieldPos:  new position of the field to move. Must be in the range
    [0,GetFieldCount()-1].
    
    OGRERR_NONE on success.
    
    OGR 1.9.0
    """
    pass

def Layer_ReorderFields(Layer_self, int_nList): # real signature unknown; restored from __doc__
    """
    Layer_ReorderFields(Layer self, int nList) -> OGRErr
    
    OGRErr
    OGR_L_ReorderFields(OGRLayerH hLayer, int *panMap)
    
    Reorder all the fields of a layer.
    
    You must use this to reorder existing fields on a real layer.
    Internally the OGRFeatureDefn for the layer will be updated to reflect
    the reordering of the fields. Applications should never modify the
    OGRFeatureDefn used by a layer directly.
    
    This function should not be called while there are feature objects in
    existance that were obtained or created with the previous layer
    definition.
    
    panMap is such that,for each field definition at position i after
    reordering, its position before reordering was panMap[i].
    
    For example, let suppose the fields were "0","1","2","3","4"
    initially. ReorderFields([0,2,3,1,4]) will reorder them as
    "0","2","3","1","4".
    
    Not all drivers support this function. You can query a layer to check
    if it supports it with the OLCReorderFields capability. Some drivers
    may only support this method while there are still no features in the
    layer. When it is supported, the existings features of the backing
    file/database should be updated accordingly.
    
    This function is the same as the C++ method OGRLayer::ReorderFields().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer.
    
    panMap:  an array of GetLayerDefn()->GetFieldCount() elements which is
    a permutation of [0, GetLayerDefn()->GetFieldCount()-1].
    
    OGRERR_NONE on success.
    
    OGR 1.9.0
    """
    pass

def Layer_ResetReading(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_ResetReading(Layer self)
    
    void
    OGR_L_ResetReading(OGRLayerH hLayer)
    
    Reset feature reading to start on the first feature.
    
    This affects GetNextFeature().
    
    This function is the same as the C++ method OGRLayer::ResetReading().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer on which features are read.
    """
    pass

def Layer_RollbackTransaction(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_RollbackTransaction(Layer self) -> OGRErr
    
    OGRErr
    OGR_L_RollbackTransaction(OGRLayerH hLayer)
    
    For datasources which support transactions, RollbackTransaction will
    roll back a datasource to its state before the start of the current
    transaction. If no transaction is active, or the rollback fails, will
    return OGRERR_FAILURE. Datasources which do not support transactions
    will always return OGRERR_NONE.
    
    This function is the same as the C++ method
    OGRLayer::RollbackTransaction().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    OGRERR_NONE on success.
    """
    pass

def Layer_SetAttributeFilter(Layer_self, char_filter_string): # real signature unknown; restored from __doc__
    """
    Layer_SetAttributeFilter(Layer self, char filter_string) -> OGRErr
    
    OGRErr
    OGR_L_SetAttributeFilter(OGRLayerH hLayer, const char *pszQuery)
    
    Set a new attribute query.
    
    This function sets the attribute query string to be used when fetching
    features via the OGR_L_GetNextFeature() function. Only features for
    which the query evaluates as true will be returned.
    
    The query string should be in the format of an SQL WHERE clause. For
    instance "population > 1000000 and population < 5000000" where
    population is an attribute in the layer. The query format is a
    restricted form of SQL WHERE clause as defined
    "eq_format=restricted_where" about half way through this document:
    
    http://ogdi.sourceforge.net/prop/6.2.CapabilitiesMetadata.html
    
    Note that installing a query string will generally result in resetting
    the current reading position (ala OGR_L_ResetReading()).
    
    This function is the same as the C++ method
    OGRLayer::SetAttributeFilter().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer on which attribute query will be
    executed.
    
    pszQuery:  query in restricted SQL WHERE format, or NULL to clear the
    current query.
    
    OGRERR_NONE if successfully installed, or an error code if the query
    expression is in error, or some other failure occurs.
    """
    pass

def Layer_SetFeature(Layer_self, Feature_feature): # real signature unknown; restored from __doc__
    """
    Layer_SetFeature(Layer self, Feature feature) -> OGRErr
    
    OGRErr OGR_L_SetFeature(OGRLayerH
    hLayer, OGRFeatureH hFeat)
    
    Rewrite an existing feature.
    
    This function will write a feature to the layer, based on the feature
    id within the OGRFeature.
    
    Use OGR_L_TestCapability(OLCRandomWrite) to establish if this layer
    supports random access writing via OGR_L_SetFeature().
    
    This function is the same as the C++ method OGRLayer::SetFeature().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer to write the feature.
    
    hFeat:  the feature to write.
    
    OGRERR_NONE if the operation works, otherwise an appropriate error
    code.
    """
    pass

def Layer_SetIgnoredFields(Layer_self, char_options): # real signature unknown; restored from __doc__
    """
    Layer_SetIgnoredFields(Layer self, char options) -> OGRErr
    
    OGRErr
    OGR_L_SetIgnoredFields(OGRLayerH hLayer, const char **papszFields)
    
    Set which fields can be omitted when retrieving features from the
    layer.
    
    If the driver supports this functionality (testable using
    OLCIgnoreFields capability), it will not fetch the specified fields in
    subsequent calls to GetFeature() / GetNextFeature() and thus save some
    processing time and/or bandwidth.
    
    Besides field names of the layers, the following special fields can be
    passed: "OGR_GEOMETRY" to ignore geometry and "OGR_STYLE" to
    ignore layer style.
    
    By default, no fields are ignored.
    
    This method is the same as the C++ method OGRLayer::SetIgnoredFields()
    
    Parameters:
    -----------
    
    papszFields:  an array of field names terminated by NULL item. If NULL
    is passed, the ignored list is cleared.
    
    OGRERR_NONE if all field names have been resolved (even if the driver
    does not support this method)
    """
    pass

def Layer_SetNextByIndex(Layer_self, long_new_index): # real signature unknown; restored from __doc__
    """
    Layer_SetNextByIndex(Layer self, long new_index) -> OGRErr
    
    OGRErr
    OGR_L_SetNextByIndex(OGRLayerH hLayer, long nIndex)
    
    Move read cursor to the nIndex'th feature in the current resultset.
    
    This method allows positioning of a layer such that the
    GetNextFeature() call will read the requested feature, where nIndex is
    an absolute index into the current result set. So, setting it to 3
    would mean the next feature read with GetNextFeature() would have been
    the 4th feature to have been read if sequential reading took place
    from the beginning of the layer, including accounting for spatial and
    attribute filters.
    
    Only in rare circumstances is SetNextByIndex() efficiently
    implemented. In all other cases the default implementation which calls
    ResetReading() and then calls GetNextFeature() nIndex times is used.
    To determine if fast seeking is available on the current layer use the
    TestCapability() method with a value of OLCFastSetNextByIndex.
    
    This method is the same as the C++ method OGRLayer::SetNextByIndex()
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    nIndex:  the index indicating how many steps into the result set to
    seek.
    
    OGRERR_NONE on success or an error code.
    """
    pass

def Layer_SetSpatialFilter(Layer_self, Geometry_filter): # real signature unknown; restored from __doc__
    """
    Layer_SetSpatialFilter(Layer self, Geometry filter)
    
    void
    OGR_L_SetSpatialFilter(OGRLayerH hLayer, OGRGeometryH hGeom)
    
    Set a new spatial filter.
    
    This function set the geometry to be used as a spatial filter when
    fetching features via the OGR_L_GetNextFeature() function. Only
    features that geometrically intersect the filter geometry will be
    returned.
    
    Currently this test is may be inaccurately implemented, but it is
    guaranteed that all features who's envelope (as returned by
    OGR_G_GetEnvelope()) overlaps the envelope of the spatial filter will
    be returned. This can result in more shapes being returned that should
    strictly be the case.
    
    This function makes an internal copy of the passed geometry. The
    passed geometry remains the responsibility of the caller, and may be
    safely destroyed.
    
    For the time being the passed filter geometry should be in the same
    SRS as the layer (as returned by OGR_L_GetSpatialRef()). In the future
    this may be generalized.
    
    This function is the same as the C++ method
    OGRLayer::SetSpatialFilter.
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer on which to set the spatial filter.
    
    hGeom:  handle to the geometry to use as a filtering region. NULL may
    be passed indicating that the current spatial filter should be
    cleared, but no new one instituted.
    """
    pass

def Layer_SetSpatialFilterRect(Layer_self, double_minx, double_miny, double_maxx, double_maxy): # real signature unknown; restored from __doc__
    """
    Layer_SetSpatialFilterRect(Layer self, double minx, double miny, double maxx, 
        double maxy)
    
    void
    OGR_L_SetSpatialFilterRect(OGRLayerH hLayer, double dfMinX, double
    dfMinY, double dfMaxX, double dfMaxY)
    
    Set a new rectangular spatial filter.
    
    This method set rectangle to be used as a spatial filter when fetching
    features via the OGR_L_GetNextFeature() method. Only features that
    geometrically intersect the given rectangle will be returned.
    
    The x/y values should be in the same coordinate system as the layer as
    a whole (as returned by OGRLayer::GetSpatialRef()). Internally this
    method is normally implemented as creating a 5 vertex closed
    rectangular polygon and passing it to OGRLayer::SetSpatialFilter(). It
    exists as a convenience.
    
    The only way to clear a spatial filter set with this method is to call
    OGRLayer::SetSpatialFilter(NULL).
    
    This method is the same as the C++ method
    OGRLayer::SetSpatialFilterRect().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer on which to set the spatial filter.
    
    dfMinX:  the minimum X coordinate for the rectangular region.
    
    dfMinY:  the minimum Y coordinate for the rectangular region.
    
    dfMaxX:  the maximum X coordinate for the rectangular region.
    
    dfMaxY:  the maximum Y coordinate for the rectangular region.
    """
    pass

def Layer_StartTransaction(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_StartTransaction(Layer self) -> OGRErr
    
    OGRErr
    OGR_L_StartTransaction(OGRLayerH hLayer)
    
    For datasources which support transactions, StartTransaction creates a
    transaction.
    
    If starting the transaction fails, will return OGRERR_FAILURE.
    Datasources which do not support transactions will always return
    OGRERR_NONE.
    
    This function is the same as the C++ method
    OGRLayer::StartTransaction().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    OGRERR_NONE on success.
    """
    pass

def Layer_swigregister(*args, **kwargs): # real signature unknown
    pass

def Layer_SyncToDisk(Layer_self): # real signature unknown; restored from __doc__
    """
    Layer_SyncToDisk(Layer self) -> OGRErr
    
    OGRErr OGR_L_SyncToDisk(OGRLayerH
    hDS)
    
    Flush pending changes to disk.
    
    This call is intended to force the layer to flush any pending writes
    to disk, and leave the disk file in a consistent state. It would not
    normally have any effect on read-only datasources.
    
    Some layers do not implement this method, and will still return
    OGRERR_NONE. The default implementation just returns OGRERR_NONE. An
    error is only returned if an error occurs while attempting to flush to
    disk.
    
    In any event, you should always close any opened datasource with
    OGR_DS_Destroy() that will ensure all data is correctly flushed.
    
    This method is the same as the C++ method OGRLayer::SyncToDisk()
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer
    
    OGRERR_NONE if no error occurs (even if nothing is done) or an error
    code.
    """
    pass

def Layer_TestCapability(Layer_self, char_cap): # real signature unknown; restored from __doc__
    """
    Layer_TestCapability(Layer self, char cap) -> bool
    
    int
    OGR_L_TestCapability(OGRLayerH hLayer, const char *pszCap)
    
    Test if this layer supported the named capability.
    
    The capability codes that can be tested are represented as strings,
    but #defined constants exists to ensure correct spelling. Specific
    layer types may implement class specific capabilities, but this can't
    generally be discovered by the caller.
    
    OLCRandomRead / "RandomRead": TRUE if the GetFeature() method is
    implemented in an optimized way for this layer, as opposed to the
    default implementation using ResetReading() and GetNextFeature() to
    find the requested feature id.
    
    OLCSequentialWrite / "SequentialWrite": TRUE if the CreateFeature()
    method works for this layer. Note this means that this particular
    layer is writable. The same OGRLayer class may returned FALSE for
    other layer instances that are effectively read-only.
    
    OLCRandomWrite / "RandomWrite": TRUE if the SetFeature() method is
    operational on this layer. Note this means that this particular layer
    is writable. The same OGRLayer class may returned FALSE for other
    layer instances that are effectively read-only.
    
    OLCFastSpatialFilter / "FastSpatialFilter": TRUE if this layer
    implements spatial filtering efficiently. Layers that effectively read
    all features, and test them with the OGRFeature intersection methods
    should return FALSE. This can be used as a clue by the application
    whether it should build and maintain its own spatial index for
    features in this layer.
    
    OLCFastFeatureCount / "FastFeatureCount": TRUE if this layer can
    return a feature count (via OGR_L_GetFeatureCount()) efficiently ...
    ie. without counting the features. In some cases this will return TRUE
    until a spatial filter is installed after which it will return FALSE.
    
    OLCFastGetExtent / "FastGetExtent": TRUE if this layer can return
    its data extent (via OGR_L_GetExtent()) efficiently ... ie. without
    scanning all the features. In some cases this will return TRUE until a
    spatial filter is installed after which it will return FALSE.
    
    OLCFastSetNextByIndex / "FastSetNextByIndex": TRUE if this layer can
    perform the SetNextByIndex() call efficiently, otherwise FALSE.
    
    OLCCreateField / "CreateField": TRUE if this layer can create new
    fields on the current layer using CreateField(), otherwise FALSE.
    
    OLCDeleteField / "DeleteField": TRUE if this layer can delete
    existing fields on the current layer using DeleteField(), otherwise
    FALSE.
    
    OLCReorderFields / "ReorderFields": TRUE if this layer can reorder
    existing fields on the current layer using ReorderField() or
    ReorderFields(), otherwise FALSE.
    
    OLCAlterFieldDefn / "AlterFieldDefn": TRUE if this layer can alter
    the definition of an existing field on the current layer using
    AlterFieldDefn(), otherwise FALSE.
    
    OLCDeleteFeature / "DeleteFeature": TRUE if the DeleteFeature()
    method is supported on this layer, otherwise FALSE.
    
    OLCStringsAsUTF8 / "StringsAsUTF8": TRUE if values of OFTString
    fields are assured to be in UTF-8 format. If FALSE the encoding of
    fields is uncertain, though it might still be UTF-8.
    
    OLCTransactions / "Transactions": TRUE if the StartTransaction(),
    CommitTransaction() and RollbackTransaction() methods work in a
    meaningful way, otherwise FALSE.
    
    This function is the same as the C++ method
    OGRLayer::TestCapability().
    
    Parameters:
    -----------
    
    hLayer:  handle to the layer to get the capability from.
    
    pszCap:  the name of the capability to test.
    
    TRUE if the layer has the requested capability, or FALSE otherwise.
    OGRLayers will return FALSE for any unrecognised capabilities.
    """
    return False

def new_Feature(FeatureDefn_feature_def): # real signature unknown; restored from __doc__
    """ new_Feature(FeatureDefn feature_def) -> Feature """
    pass

def new_FeatureDefn(char_name_null_ok=None): # real signature unknown; restored from __doc__
    """ new_FeatureDefn(char name_null_ok = None) -> FeatureDefn """
    pass

def new_FieldDefn(char_name_null_ok="unnamed", OGRFieldType_field_type=None): # real signature unknown; restored from __doc__
    """ new_FieldDefn(char name_null_ok = "unnamed", OGRFieldType field_type = OFTString) -> FieldDefn """
    pass

def new_Geometry(OGRwkbGeometryType_type=None, char_wkt=None, int_wkb=0, char_gml=None): # real signature unknown; restored from __doc__
    """
    new_Geometry(OGRwkbGeometryType type = wkbUnknown, char wkt = None, 
        int wkb = 0, char gml = None) -> Geometry
    """
    pass

def Open(char_utf8_path, int_update=0): # real signature unknown; restored from __doc__
    """ Open(char utf8_path, int update = 0) -> DataSource """
    pass

def OpenShared(char_utf8_path, int_update=0): # real signature unknown; restored from __doc__
    """ OpenShared(char utf8_path, int update = 0) -> DataSource """
    pass

def RegisterAll(): # real signature unknown; restored from __doc__
    """ RegisterAll() """
    pass

def SetGenerate_DB2_V72_BYTE_ORDER(int_bGenerate_DB2_V72_BYTE_ORDER): # real signature unknown; restored from __doc__
    """ SetGenerate_DB2_V72_BYTE_ORDER(int bGenerate_DB2_V72_BYTE_ORDER) -> OGRErr """
    pass

def SWIG_PyInstanceMethod_New(*args, **kwargs): # real signature unknown
    pass

def UseExceptions(): # real signature unknown; restored from __doc__
    """ UseExceptions() """
    pass

# no classes
