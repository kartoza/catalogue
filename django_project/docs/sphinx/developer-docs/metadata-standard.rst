Metadata
------------------------------------------

Metadata created for products in the SAC Catalogue adheres to the ISO19115
specification. The aforementioned specification defines many different
attributes that can be used to describe a product, which can result in somewhat
complicated metadata documents with the majority of attributes unpopulated do
to lack of sufficient information.

The standard also specifies a core set of attributes that should be present
for any given metadata document. 
  
Mandatory Core Items
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are listed in the table that follows:

+ **Dataset title (M)**
 - This is the SAC product identifier for this dataset
 - MD_Metadata > MD_DataIdentification.citation >
   MD_Metadata > CI_Citation.title
 - **Note:** Wolfgang in DIMS packages the ID is e.g. SPOT5.HRG.L1A but we
   should rather use SAC product ID here I think.
+ **Dataset reference date (M)**
 - Date on which product was acquired or created. For imagery products it
   should refer to the acquisition data where feasible. 
 - MD_Metadata > MD_DataIdentification.citation > CI_Citation.date
 -
+ **Dataset topic category (M)**
 -
 - MD_Metadata > MD_DataIdentification.topicCategory
 -
+ **Abstract describing the dataset (M)** 
 -
 - MD_Metadata > MD_DataIdentification.abstract
 -
+ **Dataset language (M)**
 - This will be set to English always for any product. There is currently no
   provision for storing language of products in the catalogue data models.
 - MD_Metadata > MD_DataIdentification.language
 -
+ **Metadata point of contact (M)** 
 - 
 - MD_Metadata.contact > CI_ResponsibleParty
 -
+ **Metadata date stamp (M)**
 - This maps to the GenericProduct::product_date field
 - MD_Metadata.dateStamp
 -
+


Above listing taken from section 6.5 'Core metadata for geographic subsets' of
the ISO 19115:2003 specification. Items marked (M) are mandatory, (O) Optional
and (C) Conditionally required.

Optional Core Items
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+ **Spatial representation type (O)** 
 - A geographic dataset should be represented as one of the following type codes:
  - vector
  - grid
  - textTable
  - tin
  - stereoModel
  - video
  -
 - MD_DataIdentification.spatialRepresentationType
 - 
+ **Reference system (O)**
 - The standard allows the reference system to be described either by means of 
   provision of projection, ellipsoid, datum, or by means of an identifier. In
   all cases we will use the MD_ReferenceSystem.referenceSystemIdentifier
   rather which should be specified in the form of an EPSG code.
 - MD_Metadata > MD_ReferenceSystem
 -
+ **Dataset responsible party (O)**
 - This is the person / institution responsible for the metadata information.
 - MD_Metadata > MD_DataIdentification.pointOfContact > CI_ResponsibleParty
 -
+ **Lineage (O)**
 - Lineage describes how the product was created and where if comes from. Two
   options for describing lineage exist (which can be used together too):
  + Using LI_Source (with properties: description(O), scaleDenominator(O),
  sourceReferenceSystem(O), sourceCitation(O), sourceExtent(O))
  + Using LI_ProcessStep (with properties: description(C), rationale(O),
  dataTime(O), processor(O)) where processor represents a contact person
  +
 - MD_Metadata > DQ_DataQuality.lineage > LI_Lineage
+ **On-line resource (O)** 
 - A permalink to an online record for this product. Any product will be
   accessible by visting a specific url based on its product ID e.g.
   ''http://catalogue.sac.co.za/showProduct/S4-_M--_M--_CAM2_0121_00_0404_00_061009_083518_L2A-_UTM34S/''
 - MD_Metadata > MD_Distribution > MD_DigitalTransferOption.onLine > CI_OnlineResource MD_DataIdentification.characterSet
 -
+ **Spatial resolution of the dataset (O)**
 - 
 - MD_Metadata > MD_DataIdentification.spatialResolution >
   MD_Resolution.equivalentScale or MD_Resolution.distance
 -
+ **Distribution format (O)**
 -
 - MD_Metadata > MD_Distribution > MD_Format.name and MD_Format.version
 -
+ **Additional extent information for the dataset (vertical and temporal) (O)**
 - 
 - MD_Metadata > MD_DataIdentification.extent > EX_Extent > EX_TemporalExtent
   or EX_VerticalExtent
 -
+ **Metadata file identifier (O)** 
 -
 - (MD_Metadata.fileIdentifier)
 -
+ **Metadata standard name (O)**
 -
 - MD_Metadata.metadataStandardName
 -
+ **Metadata standard version (O)**
 -
 - MD_Metadata.metadataStandardVersion
 -
+

Above listing taken from section 6.5 'Core metadata for geographic subsets' of
the ISO 19115:2003 specification. Items marked (M) are mandatory, (O) Optional
and (C) Conditionally required.

Conditional Core Items
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+ **Geographic location of the dataset (C) by four coordinates or by geographic identifier**
 - The footprint of the dataset in GML taken from GenericProduct::spatial_coverage
 - If this element is not present and we are examining a product package (as
   opposed to a metadata only package), geographic location will be retrieved
   directly from teh project itself, using gdal.
 - MD_Metadata > MD_DataIdentification.extent > EX_Extent > EX_GeographicExtent
   > EX_BoundingPolygon or EX_GeographicBoundingBox  or EX_GeographicDescription
 - **Note:** Wolfgang - DIMS should add the image footprint to the metadata, this
             can be achieved using EX_BoundingPolygon.
 -
+ **Dataset character set (C)** 
 -  MD_Metadata > characterSet
 -
+ **Metadata language (C)** 
 - This will be set to English always for any product. There is currently no
   provision for storing language of products in the catalogue data models.
 - MD_Metadata.language
 -
+ **Metadata character set (C)** 
 - 
 - MD_Metadata.characterSet
 -
+

Above listing taken from section 6.5 'Core metadata for geographic subsets' of
the ISO 19115:2003 specification. Items marked (M) are mandatory, (O) Optional
and (C) Conditionally required.

Schema Representation in XML
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Taking just these core elements we can realise a minimalist document structure
for raster data as listed below):

```
<?xml version="1.0" encoding="UTF-8"?>
<gmd:MD_Metadata xsi:schemaLocation="http://www.isotc211.org/2005/gmd 
     http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd" 
     xmlns:gmd="http://www.isotc211.org/2005/gmd" 
     xmlns:gco="http://www.isotc211.org/2005/gco" 
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
     xmlns:gml="http://www.opengis.net/gml" 
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <gmd:fileIdentifier>
    <gco:CharacterString></gco:CharacterString>
  </gmd:fileIdentifier>
  <gmd:language>
    <gmd:LanguageCode codeList="http://standards.iso.org/ittf/
    PubliclyAvailableStandards/ISO_19139_Schemas/resources/
    Codelist/ML_gmxCodelists.xml#LanguageCode" 
    codeListValue="eng">eng</gmd:LanguageCode>
  </gmd:language>
  <gmd:characterSet>
    <gmd:MD_CharacterSetCode codeSpace="ISOTC211/19115" 
    codeListValue="MD_CharacterSetCode_utf8" 
    codeList="http://www.isotc211.org/2005/resources/
    Codelist/gmxCodelists.xml#MD_CharacterSetCode">
    MD_CharacterSetCode_utf8</gmd:MD_CharacterSetCode>
  </gmd:characterSet>
  <gmd:hierarchyLevel>
    <gmd:MD_ScopeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/
    ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#
    MD_ScopeCode" codeListValue="dataset">dataset</gmd:MD_ScopeCode>
  </gmd:hierarchyLevel>
  <gmd:contact>
    <gmd:CI_ResponsibleParty>
      <gmd:organisationName>
        <gco:CharacterString>Test org</gco:CharacterString>
      </gmd:organisationName>
      <gmd:contactInfo>
        <gmd:CI_Contact>
          <gmd:address>
            <gmd:CI_Address>
              <gmd:electronicMailAddress>
                <gco:CharacterString>test@test.com</gco:CharacterString>
              </gmd:electronicMailAddress>
            </gmd:CI_Address>
          </gmd:address>
        </gmd:CI_Contact>
      </gmd:contactInfo>
      <gmd:role>
        <gmd:CI_RoleCode codeList="http://standards.iso.org/ittf/
           PubliclyAvailableStandards/ISO_19139_Schemas/resources/
           Codelist/ML_gmxCodelists.xml#CI_RoleCode" codeListValue="pointOfContact">
           pointOfContact</gmd:CI_RoleCode>
      </gmd:role>
    </gmd:CI_ResponsibleParty>
  </gmd:contact>
  <gmd:dateStamp>
    <gco:Date>2011-03-01</gco:Date>
  </gmd:dateStamp>
  <gmd:metadataStandardName>
    <gco:CharacterString>ISO19115</gco:CharacterString>
  </gmd:metadataStandardName>
  <gmd:metadataStandardVersion>
    <gco:CharacterString>2003/Cor.1:2006</gco:CharacterString>
  </gmd:metadataStandardVersion>
  <gmd:identificationInfo>
    <gmd:MD_DataIdentification>
      <gmd:citation>
        <gmd:CI_Citation>
          <gmd:title>
            <gco:CharacterString>Test title</gco:CharacterString>
          </gmd:title>
          <gmd:date>
            <gmd:CI_Date>
              <gmd:date>
                <gco:Date>2011-03-01</gco:Date>
              </gmd:date>
              <gmd:dateType>
                <gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/
                PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/
                ML_gmxCodelists.xml#CI_DateTypeCode" 
                codeListValue="creation">creation</gmd:CI_DateTypeCode>
              </gmd:dateType>
            </gmd:CI_Date>
          </gmd:date>
          <gmd:identifier>
            <gmd:RS_Identifier>
              <gmd:code>
                <gco:CharacterString>1</gco:CharacterString>
              </gmd:code>
              <gmd:codeSpace>
                <gco:CharacterString>1</gco:CharacterString>
              </gmd:codeSpace>
            </gmd:RS_Identifier>
          </gmd:identifier>
        </gmd:CI_Citation>
      </gmd:citation>
      <gmd:abstract>
        <gco:CharacterString>Test abstract</gco:CharacterString>
      </gmd:abstract>
      <gmd:topicCategory>
        <gmd:MD_TopicCategoryCode>environment</gmd:MD_TopicCategoryCode>
      </gmd:topicCategory>
      <!-- TO BE ADDED  
        <igmd:extent>
          <gmd:EX_Extent>
            <gmd:geographicElement>
              <gmd:EX_BoundingPolygon>
                <gmd:polygon>
                  <gml:outerBoundaryIs>
                     <gml:LinearRing>
      -->
    </gmd:MD_DataIdentification>
  </gmd:identificationInfo>
  <gmd:dataQualityInfo>
    <gmd:DQ_DataQuality>
      <gmd:scope>
        <gmd:DQ_Scope>
          <gmd:level>
            <gmd:MD_ScopeCode codeListValue="dataset"
            codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/
            ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#
            MD_ScopeCode">dataset</gmd:MD_ScopeCode>
          </gmd:level>
        </gmd:DQ_Scope>
      </gmd:scope>
    </gmd:DQ_DataQuality>
  </gmd:dataQualityInfo>
</gmd:MD_Metadata>
```

Editing Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are a few different potential sources of metadata:
- Online editors such as the [http://www.inspire-geoportal.eu/EUOSME/ EUOSME] editor
- DIMS generated packages containing metadata
- The QGIS metadata preparation tool being built to complement the online
  catalogue
- This catalogue will generate metadata for products when their metadata
  records are being exported (e.g. when a user wishes to save their search
  results as a metadata record, when their cart product descriptions are
  downloaded or when products themselves are downloaded).
-


Required modifications to the ISOMetadata.xml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This list is about the modifications that has to be done to the 
ISOMetadata.xml in order to ingest the DIMS packages.

+ We do need the spatial coverage extent for the image footprint, so 
 the extent must be specified with EX_BoundingPolygon instead of 
 EX_GeographicBoundingBox

+ 
-
