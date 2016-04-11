# encoding: utf-8
# module osgeo._gdal calls itself _gdal
# from /usr/local/lib/python2.7/site-packages/GDAL-1.9.0-py2.7-linux-x86_64.egg/osgeo/_gdal.so
# by generator 1.138
# no doc

# imports
from _gdal import (AllRegister, ApplyGeoTransform, AsyncReader_GetBuffer, 
    AsyncReader_GetNextUpdatedRegion, AsyncReader_LockBuffer, 
    AsyncReader_UnlockBuffer, AsyncReader_swigregister, AutoCreateWarpedVRT, 
    Band_Checksum, Band_ComputeBandStats, Band_ComputeRasterMinMax, 
    Band_ComputeStatistics, Band_CreateMaskBand, Band_DataType_get, Band_Fill, 
    Band_FlushCache, Band_GetBand, Band_GetBlockSize, Band_GetCategoryNames, 
    Band_GetColorInterpretation, Band_GetColorTable, Band_GetDefaultHistogram, 
    Band_GetDefaultRAT, Band_GetHistogram, Band_GetMaskBand, 
    Band_GetMaskFlags, Band_GetMaximum, Band_GetMinimum, Band_GetNoDataValue, 
    Band_GetOffset, Band_GetOverview, Band_GetOverviewCount, 
    Band_GetRasterCategoryNames, Band_GetRasterColorInterpretation, 
    Band_GetRasterColorTable, Band_GetScale, Band_GetStatistics, 
    Band_GetUnitType, Band_HasArbitraryOverviews, Band_ReadRaster1, 
    Band_SetCategoryNames, Band_SetColorInterpretation, Band_SetColorTable, 
    Band_SetDefaultHistogram, Band_SetDefaultRAT, Band_SetNoDataValue, 
    Band_SetOffset, Band_SetRasterCategoryNames, 
    Band_SetRasterColorInterpretation, Band_SetRasterColorTable, 
    Band_SetScale, Band_SetStatistics, Band_SetUnitType, Band_WriteRaster, 
    Band_XSize_get, Band_YSize_get, Band_swigregister, CPLBinaryToHex, 
    CPLHexToBinary, ColorEntry_c1_get, ColorEntry_c1_set, ColorEntry_c2_get, 
    ColorEntry_c2_set, ColorEntry_c3_get, ColorEntry_c3_set, 
    ColorEntry_c4_get, ColorEntry_c4_set, ColorEntry_swigregister, 
    ColorTable_Clone, ColorTable_CreateColorRamp, ColorTable_GetColorEntry, 
    ColorTable_GetColorEntryAsRGB, ColorTable_GetCount, 
    ColorTable_GetPaletteInterpretation, ColorTable_SetColorEntry, 
    ColorTable_swigregister, ComputeMedianCutPCT, ComputeProximity, 
    ContourGenerate, DataTypeIsComplex, Dataset_AddBand, 
    Dataset_BeginAsyncReader, Dataset_BuildOverviews, Dataset_CreateMaskBand, 
    Dataset_EndAsyncReader, Dataset_FlushCache, Dataset_GetDriver, 
    Dataset_GetFileList, Dataset_GetGCPCount, Dataset_GetGCPProjection, 
    Dataset_GetGCPs, Dataset_GetGeoTransform, Dataset_GetProjection, 
    Dataset_GetProjectionRef, Dataset_GetRasterBand, Dataset_RasterCount_get, 
    Dataset_RasterXSize_get, Dataset_RasterYSize_get, Dataset_ReadRaster1, 
    Dataset_SetGCPs, Dataset_SetGeoTransform, Dataset_SetProjection, 
    Dataset_WriteRaster, Dataset_swigregister, Debug, DecToDMS, 
    DecToPackedDMS, DitherRGB2PCT, DontUseExceptions, Driver_CopyFiles, 
    Driver_Create, Driver_CreateCopy, Driver_Delete, Driver_Deregister, 
    Driver_HelpTopic_get, Driver_LongName_get, Driver_Register, Driver_Rename, 
    Driver_ShortName_get, Driver_swigregister, Error, ErrorReset, 
    EscapeString, FileFromMemBuffer, FillNodata, FindFile, FinderClean, 
    GCP_GCPLine_get, GCP_GCPLine_set, GCP_GCPPixel_get, GCP_GCPPixel_set, 
    GCP_GCPX_get, GCP_GCPX_set, GCP_GCPY_get, GCP_GCPY_set, GCP_GCPZ_get, 
    GCP_GCPZ_set, GCP_Id_get, GCP_Id_set, GCP_Info_get, GCP_Info_set, 
    GCP_swigregister, GCPsToGeoTransform, GDALDestroyDriverManager, 
    GDAL_GCP_GCPLine_get, GDAL_GCP_GCPLine_set, GDAL_GCP_GCPPixel_get, 
    GDAL_GCP_GCPPixel_set, GDAL_GCP_GCPX_get, GDAL_GCP_GCPX_set, 
    GDAL_GCP_GCPY_get, GDAL_GCP_GCPY_set, GDAL_GCP_GCPZ_get, 
    GDAL_GCP_GCPZ_set, GDAL_GCP_Id_get, GDAL_GCP_Id_set, GDAL_GCP_Info_get, 
    GDAL_GCP_Info_set, GDAL_GCP_get_GCPLine, GDAL_GCP_get_GCPPixel, 
    GDAL_GCP_get_GCPX, GDAL_GCP_get_GCPY, GDAL_GCP_get_GCPZ, GDAL_GCP_get_Id, 
    GDAL_GCP_get_Info, GDAL_GCP_set_GCPLine, GDAL_GCP_set_GCPPixel, 
    GDAL_GCP_set_GCPX, GDAL_GCP_set_GCPY, GDAL_GCP_set_GCPZ, GDAL_GCP_set_Id, 
    GDAL_GCP_set_Info, GeneralCmdLineProcessor, GetCacheMax, GetCacheUsed, 
    GetColorInterpretationName, GetConfigOption, GetDataTypeByName, 
    GetDataTypeName, GetDataTypeSize, GetDriver, GetDriverByName, 
    GetDriverCount, GetLastErrorMsg, GetLastErrorNo, GetLastErrorType, 
    GetPaletteInterpretationName, GetUseExceptions, HasThreadSupport, 
    IdentifyDriver, InvGeoTransform, MajorObject_GetDescription, 
    MajorObject_GetMetadataItem, MajorObject_GetMetadata_Dict, 
    MajorObject_GetMetadata_List, MajorObject_SetDescription, 
    MajorObject_SetMetadata, MajorObject_SetMetadataItem, 
    MajorObject_swigregister, Mkdir, Open, OpenShared, PackedDMSToDec, 
    ParseXMLString, Polygonize, PopErrorHandler, PopFinderLocation, 
    PushErrorHandler, PushFinderLocation, RasterAttributeTable_Clone, 
    RasterAttributeTable_CreateColumn, RasterAttributeTable_GetColOfUsage, 
    RasterAttributeTable_GetColumnCount, 
    RasterAttributeTable_GetLinearBinning, RasterAttributeTable_GetNameOfCol, 
    RasterAttributeTable_GetRowCount, RasterAttributeTable_GetRowOfValue, 
    RasterAttributeTable_GetTypeOfCol, RasterAttributeTable_GetUsageOfCol, 
    RasterAttributeTable_GetValueAsDouble, RasterAttributeTable_GetValueAsInt, 
    RasterAttributeTable_GetValueAsString, 
    RasterAttributeTable_SetLinearBinning, RasterAttributeTable_SetRowCount, 
    RasterAttributeTable_SetValueAsDouble, RasterAttributeTable_SetValueAsInt, 
    RasterAttributeTable_SetValueAsString, RasterAttributeTable_swigregister, 
    RasterizeLayer, ReadDir, RegenerateOverview, RegenerateOverviews, Rename, 
    ReprojectImage, Rmdir, SWIG_PyInstanceMethod_New, SerializeXMLTree, 
    SetCacheMax, SetConfigOption, SieveFilter, StatBuf_IsDirectory, 
    StatBuf_mode_get, StatBuf_mtime_get, StatBuf_size_get, 
    StatBuf_swigregister, TermProgress_nocb, Transformer_TransformPoint, 
    Transformer_TransformPoints, Transformer_swigregister, Unlink, 
    UseExceptions, VSIFCloseL, VSIFOpenL, VSIFReadL, VSIFSeekL, VSIFTellL, 
    VSIFTruncateL, VSIFWriteL, VSIStatL, VersionInfo, delete_AsyncReader, 
    delete_ColorEntry, delete_ColorTable, delete_Dataset, delete_GCP, 
    delete_RasterAttributeTable, delete_StatBuf, delete_Transformer, 
    new_ColorEntry, new_ColorTable, new_GCP, new_RasterAttributeTable, 
    new_StatBuf, new_Transformer)


# Variables with simple values

VSI_STAT_EXISTS_FLAG = 1

VSI_STAT_NATURE_FLAG = 2

VSI_STAT_SIZE_FLAG = 4

# no functions
# no classes
# variables with complex values

TermProgress = None # (!) real value is ''

