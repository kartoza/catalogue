Catalogue Schema : Products
------------------------------------------

The working unit of the catalogue is a product. A product can be any of a range
of different type of geodata:
- satellite imagery
- processed imagery
- other satellite products e.g. radar data
- derived products e.g. pan sharpened imagery
- composite products (and composite derived products) e.g. mosaics
- vector and raster data of an ordinal nature (where the data is arranged in
  discrete classes) e.g. landcover maps
- vector and raster data of a continuous nature (where the data are arranged
  within a numeric scale) e.g. rainfall monitoring points
-

The catalogue implements a model (see figure below) that caters for these
different types of product and tries to deal with them in a consistent way, and
groups them in a manner that cross cutting properties and behaviours can be
assigned to any given  product based on the family of products to which it
belongs.

[img/product-heirarchy2.png]

This is the revised schema for version 2 of the online catelogue's product model.

In this chapter we delve into the various subtypes of product and explain the
operational rules governing each type.

Generic Products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Abstract Base Class for all products.

**Concrete or Abstract:** Abstract (A product must be a subclass of Generic Product)

The generic product is the base class of all products (sensor based or derived
/ surveyed geospatial data). The purpose of the generic product is to define
common properties applicable to **any** product regardless of type. A number of
data dictionaries (as described in the next section) are used to ensure data
consistency for properties relating to a product.

Generic Product Properties
.........................................

The following properties are defined for generic products:

|| Property | Type |
|  product_date          | models.DateTimeField |
|  processing_level      | models.ForeignKey |
|  owner                 | models.ForeignKey |
|  license               | models.ForeignKey |
|  spatial_coverage      | models.PolygonField |
|  projection            | models.ForeignKey |
|  quality               | models.ForeignKey |
|  creating_software     | models.ForeignKey |
|  original_product_id   | models.CharField |
|  product_id            | models.CharField |
|  product_revision      | models.CharField |
|  local_storage_path    | models.CharField |
|  metadata              | models.TextField |
|  remote_thumbnail_url  | models.TextField |
|  concrete              | False |

**Product Date** is the generalised date for the product. This may be
equivalent to the product_acquisition_start of sensor based products, the
mid-point between  product_acquisition_start and  product_acquisition_end for
sensor based products, or an arbitrary date assigned by an operator at point of
product ingestion. Product Date is used as the basis for any date-centric
search activities in the catalogue.

**Processing Level**. All products have a descriptor indicating to what level
they have been processed. For sensor based products, this level may indicate
whether the product has been georeferenced or not. For Generic Spatial
Products, it may indicate what kind of analysis was carried out in order to
create the product. //see:// dictionaries section below.


**Local Storage Path**

```
sac=# select local_storage_path from catalogue_genericproduct where local_storage_path is not null limit 5;
local_storage_path
--------------------------------------------------------------------------------------
ZA2/1Ab/2010/5/31/ZA2_MSS_R3B_FMC4_080E_57_026N_47_100531_033947_L1Ab_ORBIT-.tif.bz2
ZA2/1Ab/2010/3/31/ZA2_MSS_R3B_FMC4_176E_47_039S_35_100331_204030_L1Ab_ORBIT-.tif.bz2
```
The path is relative to the IMAGERY_ROOT defined in settings.py and is in the form:

''mission/processing level/yyyy/m/d/product_id.<file extension>.bz2''

or

''mission/processing level/yyyy/m/d/product_id.<file extension>.tar.bz2'' (for multifile products)

Product ID Naming Scheme
.........................................

All generic products can be identified by a 'nearly unique' product id. The
product id seeks to normalise the naming conventions used by different
satellite operators such that a common naming scheme can be universally
applied.

The naming scheme used for products depends on where the product falls in the
model heirarchy. Each product type (Generic, Imagery, Sensor, Geospatial etc.)
can overload the getSacProductId method in order to apply model specific logic
as to how these product Ids should be assigned.

These will be discussed more fully in the sections that follow.

Since this is an abstract class, it has no direct naming scheme of its own.

------------------
**Note:** As per discussion with Wolfgang on 17 Feb 2011, the SAC Product Id
will apply only to sensor based products and a different, as yet undefined,
identifcation scheme will be used for GeoSpatial products.

**Note:** See CDSM naming scheme for vector products.


Dictionaries
.........................................

Generic product properties that are used repeatedly are described using foreign
key joins to various dictionary tables. These can be visualised in the
following diagram:

[img/generic-product-dictionaries.png]

These dictionaries are described in details in the sub-sections that follow.

Institution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The institution (linked to the **GenericProduct** table on the owner field)
indicates the organisation from which the product can be obtained.

As at the time of writing this document, only one record exists in this table,
and all new products are assigned to this institution:

|| ID |             Name              |   Address1    | Address2 |   Address3   | Post Code |
|  1 | Satellite Applications Centre | Hartebeeshoek | Gauteng  | South Africa | 0000       |

**Constraint:** Name must be unique.

----------------------
**Note:** Wolfgang verify that we won't be storing the original data owner
(e.g. Spot Image) here.


Processing Level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Products may have been processed by software to improve the product. For
example, a level 1a product is a 'raw' image with no georeferencing, format
conversion etc. In order for a product to be usable by mainstream users, it
generally needs to be converted into a popular image format (e.g. geotiff),
georeferenced (so that it appears in the correct place on a map),
orthorectified (to adjust the image based on distortions introduced by terrain
variance) and so on.

Processing levels are expressed as a four letter code e.g.:

```
L1Aa
```

This code can be deconstructed as:

 - **L** Abbreviation for 'level'
 - **[1-4]** A numeral representing the major level wher
  - **1** Raw imagery
  - **2** Unreferenced imagery in a common format e.g. tiff
  - **3** Rectified and imagery cleaned for atmospheric disturbance, lens irregularities etc.
  - **4** Derived products
  -
 - **[A-C]** A single upper case character representing product class (derivative,raster, vector)
 - **[a-z]** A single lower case character representing class-type (see below)
 -

**Note:** The 'L' prefix is not stored in the database tables.

Some commonly used codes include:

|| Code   | Description                                 |
| 2A/B  | (L1G)                                        |
| 3Aa   | (L1T) Orthorectified DN values               |
| 3Ab   | At sensor/TOA reflectance                    |
| 3Ac   | Atmospherically corrected/TOC reflectance    |
| 3At   | Topographic correction                       |
| 4A*   | Derivatives/products                         |
| 4B*   | Pixel-based classification                   |
| 4C*   | Vector/object classification                 |

Some common values for class type include:

|| Code | Description |
| a | Ancillary data eg. Relief shadow, hydrology |
| b | Bare or built-up indices |
| m | Maths transformation |
| s | Statistical calculations |
| t | Texture |
| v | Vegetation indices |
| w | Water/moisture indices |
| x | Time-series or metrics |
| f | Spectral Rule based Features including indices |
| r | L1 Spectral Rule based layers |
| c | L2 Spectral Rule based layers classification spectral categories |


The following processing levels are listed in the database.

 || ID | Abbreviation |   Name    |
 |  1  | 2A           | Level 2A  |
 |  2  | 1A           | Level 1A  |
 |  3  | 1Ab          | Level 1Ab |
 |  4  | 1Aa          | Level 1Aa |
 |  12 | 3Aa         | Level 3Aa |
 |  13 | 3Ab         | Level 3Ab |
 |  14 | 3Ac         | Level 3Ac |
 |  15 | 3Ad         | Level 3Ad |
 |  16 | 3Ba         | Level 3Ba |
 |  17 | 3Bb         | Level 3Bb |
 |  18 | 4           | Level 4   |

**Constraints:** Abbreviation must be unique (name can be duplicated).

---------------------------
**Note:** These should be updated to include a proper description with each in
a new description col. TS

Projection 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The projection (or more accurately the coordinate reference system (CRS)) model
contains a dictionary of CRS identifiers and human readable names. The
identifiers are expressed in the numbering system of the European Petroleum
Survey Group (EPSG). The list included is not comprehensive - at the time of
writing it contains only 84 or the //circa// 3000+ entries available in the
official EPSG CRS list.

The EPSG name is a more user friendly and easily recognisable representation of
the EPSG code. For reference, an extract of the entries is provided in the table below:

 || ID | Epsg Code |  Name |
 |  1 |     32737 | UTM37S |
 |  2 |     32733 | UTM33S |
 |  3 |     32738 | UTM38S |
 |  4 |     32734 | UTM34S |
 |  5 |     32732 | UTM32S |
 |  6 |     32735 | UTM35S |
 |  7 |     32629 | UTM29N |
 |  8 |     32731 | UTM31S |

**Constraints:** EPSG Code must be unique.

Quality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The quality is intended to provide a well defined dictionary of terms for
qualitative assessment of products. Different product vendors use different
schemes for describing product quality.

For example Spot Image describes quality in terms of an imaginary grid overlaid
(and bisecting the image into equal sized units). Each grid cell is then given
a ranking e.g. ''AABBAAAABB''.

Currently only one entry exists:

 || ID |  Name  |
 |  1 | Unknown |

This presence of a quality indicator is mandatory for GenericProduct, but the
fact that all records are currently assigned a ranking of 'Unknown' makes this
attribute largely meaningless.

-------------------------
**Note:** Wolfgang - we need to define a standard of quality description and a
strategy for populating existing and new records with an appropriate quality
indicator.

Creating Software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is useful in understanding a dataset to know which software package was used
to create it. At time of writing this document, only two software packages are
available:

 || ID |  Name   | Version |
 | 1 | Unknown | None      |
 | 2 | SARMES1 | Sarmes1   |

**Constraints:** Name must be unique.

Sarmes2 will be added to this list in the future, and other additional packages
as needed.

-------------------------
**Note:** Wolfgang - do we need to include other software here, and if so which
products should have this applied?

License
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each product should have a license associated with it. The license will detail
any restrictions on redistribution or useage that applies for the product.

The following licenses are defined and all products have been assigned one of
these licenses.

 || ID |    Name     |   Details   | Type |
 |  1 | SAC Commercial License | SAC Commercial License   |  |
 |  2 | SAC Free License | SAC Free License   |  |
 |  3 | SAC Partner License | SAC Partner License   |  |


**Constraints:** Name must be unique.

License Type Enumeration: The license type is an enumerated list (managed
directly in the model rather than in a separate dictionary via a foreign key
constraint). The reason for this is that application logic specific to the
license type is implemented (for example to determine if a product can be
freely distributed to a client).

Each license in the system is allocated a type. The following types and their
meanings are defined:

Free data, government license or commercial license or any.

|| ID | Type | Description |
|  1  | Free | Can be freely shared and redistributed without restriction |
|  2  | Government License | Applies to products that can be freely redistributed to government departments. |
|  3  | Commercial | Applies to product that can only be commercially distributed |



The license type is determined on a sensor by sensor, product by product basis. The following rules hold true:

+ SPOT data are all under SAC Partner license
+ SAC-C, Sumbandilasat and CBERS are all under SAC Free License
+ When not explicitly defined, all products should be assigned the SAC Commercial License
+

**Note:** Wolfgang to define any further rules

**Note:** The allocation of license may not always reflect the cost of the data
- where substantial processing has been requested by a user, SAC may charge a
processing fee. The system currently makes no accommodation for calculation of
such 'value added' fees.



**Note:** For the Government license type The User profile for this catalogue
includes a field  SacUserProfile::strategic_partner which is a boolean
indicating if  the users is registered as a SAC Strategic Partner employee and
thus granted unfettered access to certain products (e.g. Spot imagery). Where
the user is not a Government employee, the product license should be considered
to be commercial.

---------------------
**Note:** Wolfgang - we need to define more completely the SAC License, or
several variants of it, and add any other licenses that may apply. We would
also need rules descibing how to select products which should have which
license applied.

**Note:** Wolfgang - does it make sense to have an 'any' license?

%----------------------------------------------------------
%----------------------------------------------------------
%------------------ Generic Imagery Product  ---------------------
%----------------------------------------------------------
%----------------------------------------------------------
Generic Imagery Products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Base Class for //imagery// products.

**Concrete or Abstract:** Concrete (instances of this class can be created and stored).

**GenericImageryProduct** is the model that all sensor based products inherit
from. In addition, concrete instances of **GenericImageryProduct** are used to lodge sensor
based aggregate data. For example when an image is created that is a
combination of a 'J' and a 'T' image, we can no longer canonically state which
acquisition mode etc was used for that image. In this case the DAG (Directed
Acyclical Graph) implementation will be used to provide backpointers to the
original images used to create this record (and those backpointers will be to
Sensor based product records).

Product ID Naming Scheme
.........................................

Generic imagery products do not have an associated Mission, Sensor, Sensor Type
or Acquisition Mode, and thus the naming system differers from final (having no
ancestors) sensor based products.



------------------------
**Note:** Wolfgang to define or we must devise something. The follow section
was from Wolfgang's notes but it does not model well:
 - composite products my span multiple modes, types, sensors and even missions.
 - scenes may span long time periods and the concept of a central scene is ambiguous
 - products may span larger areas than a single QDS map and in other countries
   mapping units may differ.
 - composite products may include other imagery types eg. aerial photos.
 -

Composite files -mosaics:

``QQQQQQ_SSS_sss_ttt_mmmm_pppp_ps_rrrr_rs_yymmdd_hhmmss_LBLL_PPPPPP``

Use central scene for date and time

--------------------

Composite files - time series:
be
``MT_yymmdd_yymmdd_SSS_sss_ttt_mmmm_pppp_ps_rrrr_rs_yymmdd_hhmmss_LBLL_PPPPPP``

Use central time scene for date and time

--------------------

The following key can be used to decode the above:

|| Code            | Description                                          |
| SSS              | satellite (mission) name e.g. L5-; S5-               |
| sss              | sensor (mission sensor) e.g. TM-; ETM                |
| ttt              | type (sensor type) eg. HRF; HPN; HPM                 |
| mmmm             | bumper (acquisition) mode eg. SAM- BUF-              |
| pppp             | path (k)                                             |
| ps               | path shift                                           |
| rrrr             | row (j)                                              |
| rs               | row span                                             |
| yymmdd           | date                                                 |
| hhmmss           | time                                                 |
| LLLL             | processing Level code eg. L2A; L4Ab                  |
| PPPPPP           | Projection eg. UTM35S; LATLON; ORBIT-                |
| QQQQQQ           | 1:50000 topographic map name eg 3425CD               |
| MT_yymmdd_yymmdd | multi-temporal time span: start date to end date     |

Imagery product Properties
.........................................

A GenericImageryProduct extends the generic product model with these properties:
- spatial_resolution
- spatial_resolution_x
- spatial_resolution_y
-

Imagery Product Aggregation Rules
.........................................

In the DAG (Directed Acyclical Graph) that maps relationships between products
and their downstream constituent products, ImageryProducts can be made of:

- Generic Imagery Products
- Generic Sensor Products
- Optical Products
- Radar Products
- Geospatial Products and subclasses of Geospatial products
-

**Note:** Self referencing is not allowed. That is, a Imagery product may not
include itself in any leaf node.

**Note:** Generic Imagery Products will always be composite (derived from one
or more other products).

Dictionaries
.........................................

No additional dictionaries are introduced with this class.

Generic Sensor based products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Base Class for //Sensor// products.

**Concrete or Abstract:** Abstract (instances cannot be directly created and stored).


Generic sensor product is an Abstract Base Class that all other sensor based
products inherit from. It inherits from Generic Imagery product.

Product ID Naming Scheme
.........................................

The following scheme is used for assigning product id's for sensor based products:


Single scene file names:

``SSS_sss_ttt_mmmm_pppp_ps_rrrr_rs_yymmdd_hhmmss_LLLL_PPPPPP``

e.g. L7-_ETM_HRF_SAM-_168-_00_077-_010530_------_L3Ab_UTM36S


The following key can be used to decode the above:

|| Code            | Description                                          |
| SSS              | satellite (mission) name e.g. L5-; S5-               |
| sss              | sensor (mission sensor) e.g. TM-; ETM                |
| ttt              | type (sensor type) eg. HRF; HPN; HPM                 |
| mmmm             | bumper (acquisition) mode eg. SAM- BUF-              |
| pppp             | path (k)                                             |
| ps               | path shift                                           |
| rrrr             | row (j)                                              |
| rs               | row span                                             |
| yymmdd           | date                                                 |
| hhmmss           | time                                                 |
| LLLL             | processing Level code eg. L2A; L4Ab                  |
| PPPPPP           | Projection eg. UTM35S; LATLON; ORBIT-                |

**Note:** Elements Mission(SSS), MissionSensor(sss), SensorType(ttt) and
AcquisitionMode (mmmm) are compulsory for GenericSensorProducts. Where these
are not explicitly defined, they will be implicitly defined. That is to say, if
no Sensor has been defined for a Mission, it will cause the creation and
assignment of an implicit MissionSensor orbject named after the sensor. For
example: A new product for fictitious sensor 'FOO' is imported. No sensor type
is defined, so a default sensor type called 'FOO' is defined. This same logic
applies to SensorType and Acquisition Mode. Another example: Mission L5 exists,
Sensor MS exists, no sensor type exists so a default type of 'MS' is created
and consequently a default acquisition mode of MS os also created.
See 'placeholder' clauses in description that follow.

Where Row (rrrr) and Path (pppp) are not know for a sensor, the
word 'None' will be written out in the  product id to differentiate from 0000
which may be a valid row or path.

Where Row and Path are not applicable for a sensor (e.g. Sumbandilasat, some
Radar sensors), a centroid derived Path, Path offset, Row and Row offset will
be assigned as per the illustration below:

[img/centroid_based_row_path.png]

Generic Sensor Product Aggregation Rules
.........................................

Since this is an abstract class it may not be a node in a product aggregation tree.


Sensor Product Dictionaries
.........................................

Several domain lists are implemented for sensor based products. These can be
visualised in the following diagram:

[img/proposed-sensor-product-dictionaries.png]

These dictionaries and their interrelationships are described in more detail in
the text below.



Mission
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A mission is the name for the particular space vechicle on board of which one
or more sensors are deployed. The catalogue hosts metadata entry for a number
of different sensors - at time of writing this list looked like the table
below.

 || ID   | Abbreviation | Operator Abbreviation |    Name      |
 |  1   | S1           | SPOT-1                | Système Pour l'Observation de la Terre 1                        |
 |  2   | S5           | SPOT-5                | Système Pour l'Observation de la Terre 5                        |
 |  3   | ZA2          | ZASat-002             | Sumbandilasat                                                   |
 |  4   | C2B          | CBERS-2-B             | China-Brazil Earth Resources Satellite 2 B                      |
 |  5   | S-C          | SAC-C                 | Satélite de Aplicaciones Científicas-C                          |
 |  6   | S3           | SPOT-3                | Système Pour l'Observation de la Terre 3                        |
 |  7   | N14          | NOAA-14               | National Oceanic and Atmospheric Administration Satellite 14    |
 |  8   | N16          | NOAA-16               | National Oceanic and Atmospheric Administration Satellite 16    |
 |  9   | N11          | NOAA-11               | National Oceanic and Atmospheric Administration Satellite 11    |
 |  10  | N9           | NOAA-9                | National Oceanic and Atmospheric Administration Satellite 9     |
 |  11  | N17          | NOAA-17               | National Oceanic and Atmospheric Administration Satellite 17    |
 |  12  | N12          | NOAA-12               | National Oceanic and Atmospheric Administration Satellite 12    |
 |  13  | N15          | NOAA-15               | National Oceanic and Atmospheric Administration Satellite 15    |
 |  14  | E2           | ERS-2                 | European Remote-Sensing Satellite-2                             |
 |  15  | E1           | ERS-1                 | European Remote-Sensing Satellite-1                             |
 |  16  | L5           | LS-5                  | Landsat 5                                                       |
 |  17  | L7           | LS-7                  | Landsat 7                                                       |
 |  18  | L2           | LS-2                  | Landsat 2                                                       |
 |  19  | L3           | LS-3                  | Landsat 3                                                       |
 |  20  | L4           | LS-4                  | Landsat 4                                                       |
 |  21  | S2           | SPOT-2                | Système Pour l'Observation de la Terre 2                        |


The mission abbreviation, operator_abbreviation and name must be unique.

**Note:** Wolfgang we are using ZA2 instead of SS here.

**Note:** RE - RapidEye needs to be added to this list

**Constraints:** Name and abbreviation must be unique_together. Name must be unique.

Mission Sensors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On board each space vehicle receiving EO data will be one or more sensors.
Although the sensor may be nominally the same between two different missions
(e.g. MSS), the specific properties of these sensors will vary between
missions, and even between identical sensors on the same mission.
A sensor is basically a camera or other equipment capable of performing
distance observation of the earth.



 || ID | Abbreviation | Operator Abbreviation |       Name          |
 | 1  | AVH          | AVHRR-3               | Advanced Very High Resolution Radiometer NOAA          |
 | 2  | AMI          | AMI-1                 | Active Microwave Instrument ERS-1                      |
 | 3  | TM           | TM-4                  | Thematic Mapper Landsat 4                              |
 | 4  | TM           | TM-5                  | Thematic Mapper Landsat 5                              |
 | 5  | MSS          | MSS-1                 | Multi-Spectral-Scanner Landsat 1                       |
 | 6  | MSS          | MSS-2                 | Multi-Spectral-Scanner Landsat 2                       |
 | 7  | MSS          | MSS-3                 | Multi-Spectral-Scanner Landsat 3                       |
 | 8  | MSS          | MSS-4                 | Multi-Spectral-Scanner Landsat 4                       |
 | 9  | MSS          | MSS-5                 | Multi-Spectral-Scanner Landsat 5                       |
 | 10 | ETM          | ETM+                  | Enhanced Thematic Mapper Plus Landsat 7                |
 | 11 | HRV          | HRV-1                 | Haute Resolution Visible Spot 1                        |
 | 12 | HRV          | HRV-2                 | Haute Resolution Visible Spot 2                        |
 | 13 | HRV          | HRV-3                 | Haute Resolution Visible Spot 3                        |
 | 14 | HIR          | HRVIR-4               | High-Resolution Visible and Infrared sensor Spot 4     |
 | 15 | VMI          | Vegetation-4          | Vegetation Monitoring Instrument / Vegetation Spot 4   |
 | 16 | HRG          | HRG-5                 | High Resolution Geometric Spot 5                       |
 | 17 | HRS          | HRS-5                 | High Resolution Stereoscopic Spot 5                    |
 | 18 | VMI          | Vegetation-5          | Vegetation Monitoring Instrument / Vegetation Spot 5   |
 | 19 | AMI          | AMI-2                 | Active Microwave Instrument ERS-1                      |


The abbreviation field and the foreign key to Mission must be unique together.


**Note:** Ale, I would like to get rid of the has data field if poss. It is
used to restrict the display of sensors to users to only those with data
associated to them. Is there a cleaner way to do it? At mininimum we need to
automate updating this field as data is added to and removed from the system.
UPDATE: the sensors list in the UI is now filtered and shows only sensors with data.

Sensors
TM - Thematic Mapper
ETM - Enhanced thematic mapper
MSS Multi-spectral

**Constraints:** Name and abbreviation must be unique_together. operator_abbreviation must be unique.


**Note:** A one-to-many relationship will be created between mission sensor
entities and their related mission - as illustrated here:

```
+----------------+                +---------+
| Mission Sensor |>---------------| Mission |
+----------------+                +---------+
```


**Relationship in plain english:** Each mission can have one or more mission
sensors associated with it. Each mission sensor shall be associated to only one
mission.``

The Abbreviation will **not** be unique per sensor. Note that the 4 letter name
space does not allow for many permutations and readers of the abbreviation
should do it in context of a specific mission, sensor type etc.  (for example
by always presenting the mission abbreviation at the same time).

In some cases, no specific mission sensors will exist for a mission. In these
cases, a placeholder mission sensor should be created, named directly after the
mission e.g.

 || ID | Abbreviation | Name  | Description | Has Data | Mission |
 | 1 | ERS          | ERS |  ERS | t |  ERS |

Above assumes the pre-existance of a mission 'ERS'.


Sensor Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The sensor type describes a mission sensor. 'High end' satellites may use a
custom sensor type with its own specific properties. 'Cheaper' satellites may
use simple CCD (charge coupled device) style sensors.


 || ID | Abbreviation |  Operator Abbreviation | Name  |
 |  1  | VIT          | VisNirSwirTh           | Visual, Near Infrared, Short Wave Infrared and Thermal             |
 |  2  | STM          | STM-C                  | Strip Map C Band                                                   |
 |  3  | HRF          | HRF                    | Multispectral                                                      |
 |  4  | HTM          | HTM                    | Thermal                                                            |
 |  5  | HRF          | HRF                    | Multispectral                                                      |
 |  6  | HTM          | HTM                    | Thermal                                                            |
 |  7  | VNI          | VisNir                 | Visual, Near Infrared                                              |
 |  8  | VNI          | VisNir                 | Visual, Near Infrared                                              |



The abbreviation field and the foreign key to MissionSensor must be unique together.

ach mission sensor should have at least one sensor  type associated with it.
When a mission sensor exists with no associated sensor type, a default sensor
type matching the mission sensor abbreviation should be created e.g.

 || ID | Abbreviation |                   Name       | Mission Sensor |
 |  7 | MSS          | Multispectral - Landsat 1     | Landsat 1 MSS |
 |  8 | MSS          | Multispectral - Landsat 2     | Landsat 2 MSS |
 |  9 | MSS          | Multispectral - Landsat 3     | Landsat 3 MSS |
 |  10 | MSS          | Multispectral - Landsat 4     | Landsat 4 MSS |
 |  11 | MSS          | Multispectral - Landsat 5     | Landsat 5 MSS |

The Abbreviation will **not** be unique per sensor type. Note that the 4 letter name
space does not allow for many permutations and readers of the abbreviation
should do it in context of a specific mission-sensor, acquisition mode etc.  (for example
by always presenting the mission abbreviation at the same time).


**Note:** A one-to-many relationship will be created between mission sensor
entities and their related mission - as illustrated here:

```
+-------------+                +----------------+
| Sensor Type |>---------------| Mission Sensor |
+-------------+                +----------------+
```

**Relationship in plain english:** Each mission sensor can have one or more sensor
types associated with it. Each sensor type shall be associated to only one sensor.``


Acquisition Modes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each sensor can operate in one or more modes. Thus there the list of
acquisition modes should include at least one entry per sensor type. Where such
an entry does not exist, a default one (named after the sensor type) shall be
created. Acquisition modes table example:

 || ID   | Abbreviation | Operator Abbreviation |  Name               | Geom Resolution | Band Count |
 |  1 | MS           | MS                    | Multispectral                        |   0 |    0   |                              |
 |  2 | VV           | VV                    | Vertical Vertical Polarisation       |   0 |    0   |                              |
 |  3 | HRT          | HRT                   | Multispectral and Thermal            |   0 |    0   |                              |
 |  4 | X            | X                     | X                                    |   0 |    0   |                              |
 |  5 | I            | I                     | I                                    |   0 |    0   |                              |
 |  6 | M            | M                     | M                                    |   0 |    0   |                              |
 |  7 | P            | P                     | P                                    |   0 |    0   |                              |
 |  8 | J            | J                     | Multispectral                        |   0 |    0   |                              |
 |  9 | B            | B                     | Panchromatic                         |   0 |    0   |                              |
 | 10 | A            | A                     | Panchromatic                         |   0 |    0   |                              |
 | 11 | FMC4         | FMC4                  | Forward Motion Compensation 4        |   0 |    0   |                              |
 | 12 | 3BG          | 3BG                   | 3BG                                  |   0 |    0   |                              |
 | 13 | 5BF          | 5BF                   | 5BF                                  |   0 |    0   |                              |
 | 14 | 3BP          | 3BP                   | 3BP                                  |   0 |    0   |                              |
 | 15 | HR           | HR                    | HR                                   |   0 |    0   |                              |
 | 28 | VV           | VV                    | Vertical Vertical Polarisation       |   0 |    0   |                              |
 | 29 | HH           | HH                    | Horizontal Horizontal Polarisation   |   0 |    0   |                              |


The abbreviation field and the foreign key to SensorType must be unique together.


**Note:** Wolfgang to populate sensor type. Entries should be duplicated for
each sensor type that has that mode e.g.

 || ID   | Abbreviation |               Name               | Geom Resolution | Band Count | Sensor Type |
 |  1  | MS           | Multispectral - Landsat 1          |   0 |    0   |     Multispectral - Landsat 1  |
 |  2  | MS           | Multispectral - Landsat 2          |   0 |    0   |     Multispectral - Landsat 2  |



**Todo:** Check this list from Wolfgang is represented:

|| Mode | Description              |
| HRF  | Multi-spectral bands         |
| HPN  | Panchromatic bands           |
| HTM  | Thermal bands                |
| HPM  | Pan-sharpened multi-spectral |

**Note:** A one-to-many relationship will be created between mission sensor
entities and their related mission - as illustrated here:

```
+------------------+                +----------------+
| Acquisition Mode |>---------------|   Sensor Type  |
+------------------+                +----------------+
```

**Relationship in plain english:** Each sensor type can have one or more
acquisition mode associated with it. Each acquisition mode shall be associated
to only one sensor type.``

The Abbreviation will **not** be unique per acquisition mode. Note that the 4
letter name space does not allow for many permutations and readers of the
abbreviation should do it in context of a specific sensor type.  (for example
by always presenting the sensor type, mission type and mission abbreviations at
the same time).


--------------------------------------------
**Note:** The spatial resolution and band count columns in this table need to
be populated by Wolfgang.

**Logic Rules:** The additional columns in the acquisition mode are used to
provide implicit values for products if they are created without implicit
values. In particular:

+ The spatial resolution will be used to populate the GenericSensorProduct
  fields of spatial_resolution, spatial_resolution_x and
  spatial_resolution_y. This is implemented by first populating the
  spatial_resolution field (NULL) when assigning acquisition mode, and then
  assigning the same value to both spatial_resolution_x and
  spatial_resolution_y.
+ The band_count in acquisition mode will be assigned to the
  GenericSensorProduct.band_count (formerly called spectral_resolution) if NULL
  at the moment of assignment.
+

Mission Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The mission group model will be an addition to the schema that will allow
virtual groupings of mission sensors. In simple search and other places
designated by the client, mission groups will be used to select a family of
missions (satellites) to search on e.g. all Landsat missions.

```
+------------------+                +----------------+
| Mission          |>---------------| Mission Group  |
+------------------+                +----------------+
```

**Relationship in plain english:** Each mission group  can have one or more
missions associated with it. Each mission shall be associated to only one
mission group.``

The mission group should be populated as follows:


When a new mission is added, it should always be assigned to an existing
mission group (with the mission group being created first if needed).

Notes on the proposed schema changes
.........................................

The proposed schema change will bring about the following advantages:

 - less attributes stored on generic sensor (simplification is always good)
 - easier to understand the relationship between these entities
 - remove the risk of ambigious entries (e.g. MSS applying to multiple
   different sensors)
 - we can now effectively store resolution on acquisition table as its
    unambiguous as to which sensor & mission it applies
 - product id 'drill down searches will be more efficient
 -

**Note:** We need to get the mappings from Wolfgang for which mission sensors
are associated with each mission etc.

Because the schema changes introduce a strict heirarchy and also introduce a
requirement that acquisition mode through to mission be defined for a sensor
based product, assigning these entities to derived products will not be
meaningful. Because of this composite products (e.g. a pan sharpened SPOT
image) will not be modelled under generic sensor products but rather belong to
a sub class GenericImageryProduct.


Resolving the metadata to explicit records
.........................................

The input metadata we receive will be ambiguous for acquisition mode, sensor
type, mission sensor. It is only with the presence of a mission abbreviation
that these can be correctly resolved. For example:


``L7-_ETM_HRF_SAM-_168-_00_077-_010530_------_L3Ab_UTM36S``

``SSS_sss_ttt_mmmm_pppp_ps_rrrr_rs_yymmdd_hhmmss_LLLL_PPPPPP``

|| Code            | Description                                          |
| SSS              | satellite (mission) name e.g. L5-; S5-               |
| sss              | sensor (mission sensor) e.g. TM-; ETM                |
| ttt              | type (sensor type) eg. HRF; HPN; HPM                 |
| mmmm             | bumper (acquisition) mode eg. SAM- BUF-              |

So we can see from this example, we have the following:

|| Satellite | Mission Sensor | Sensor Type | Acquisition Mode |
| L7 | ETM | HRF | SAM |

In cases where the entries for these dictionary terms do not exist, new records should be added to the tables using the following logic:

+ Add ``L7`` to the mission table and note the PKEY of the new record
+ Add abbreviation ``ETM``, description ``ETM:Landsat 7``, mission ``PKEY from above`` to the mission sensor table and note the PKEY of the new record
+ Add abbreviation `` HRF``, description ``HRF:ETM:Landsat 7``, mission_sensor ``PKEY from above`` to the sensor type table and note the PKEY of the new record
+ Add abbreviation ``SAM``, description ``SAM:HRF:ETM:Landsat 7``, sensor_type ``PKEY from above`` to the acquisition mode table.
+





Optical products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Imagery where each pixel represents the reflectance value of
light waves reflected from a remote target within a given segment of the light
spectrum.

**Concrete or Abstract:** Concrete

Optical products are a specialisation of Generic Sensor Products. An Optical
Product is a concrete class (i.e. one that should not be treated as abstract).
The Optical Product model is used to represent any sensor originated product
that has been taken using an optical sensor. It may cover non-visible parts of
the spectrum and consist of one or more bands, each covering a different part
of the spectrum. Generally the bands (in multiple band images) are co-aligned -
meaning the cover the same geographical footprint. In some cases however, the
bands are offset from each other, creating an opportunity to super-sample the
image and improve its native resolution.

[img/optical-image-example-medium.png]

Optical products are end nodes in the product heirarchy - they do not have any
further specialisations.

Optical Product Properties
.........................................

The optical product model introduces a number of properies in addition to those
inherited from the GenericSensorProduct base class.

 - cloud_cover
 - sensor_inclination_angle
 - sensor_viewing_angle
 - gain_name
 - gain_value_per_channel
 - gain_change_per_channel
 - bias_per_channel
 - solar_zenith_angle
 - solar_azimuth_angle
 - earth_sun_distance
 -

Product ID Naming Scheme
.........................................

The naming of optical products follows the rules from its base class,
GenericSensorProduct.

Optical Product Aggregation Rules
.........................................

In the DAG (Directed Acyclical Graph) that maps relationships between products
and their downstream constituent products, **OpticalProducts** may **not**
themselves be aggregates. This is because each sensor product has an explicit
acquisition mode, sensor type etc. and such relationships are not mappable for
aggregate products. OpticalProducts can however participate in aggregations.
In the case that you have have two **OpticalProducts** forming a new image, the
new image should be modelled as a **GenericImageryProduct**.



Radar Products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Imagery where each pixel represents the reflectance value of
radio waves reflected from a remote target.

**Concrete or Abstract:** Concrete


Radar Product Aggregation Rules
.........................................

In the DAG (Directed Acyclical Graph) that maps relationships between products
and their downstream constituent products, **RadarlProducts** may **not** be
aggregates. This is because each sensor product has an explicit acquisition
mode, sensor type etc. and such relationships are not mappable for aggregate
products. In the case that you have have two **RadarlProducts** forming a new
image, the new image should be modelled as a **GenericImageryProduct**.


Product ID Naming Scheme
.........................................

Follows the same scheme as defined in OpticalProduct documentation.

Optical Product Properties
.........................................

The radar product model introduces a number of properies in addition to those
inherited from the GenericSensorProduct base class. These properties are not
shared with optical products.

 - imaging_mode
 - look_direction
 - antenna_receive_configuration
 - polarising_mode
 - polarising_list
 - slant_range_resolution
 - azimuth_range_resolution
 - orbit_direction
 - calibration
 - incidence_angle
 -

%----------------------------------------------------------
%----------------------------------------------------------
%------------------ Geospatial Product --------------------
%----------------------------------------------------------
%----------------------------------------------------------
Geospatial Products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Level 4 products derived from imagery or by direct earth
measurement (e.g. by conducting a survey with GPS).

**Concrete or Abstract:** GeoSpatial products are pure abstract (they cannot
exist on their own, only as a subclass).

Geospatial Products incorporate all level 4 products. Geospatial products are
abstract representations of features of the earths surface - as opposed to
Imagery Products which are some form of obervation of the earth service.

Geospatial Product Properties
.........................................

All geospatial products share the following properties:

 - name
 - description
 - processing_notes
 - equivalent_scale
 - data_type
 - temporal_extent_start
 - temporal_extent_end
 - place_type
 - place
 - primary_topic
 - tags
 -

Properties from GenericProduct are also inherited.

The **name** property is a descriptive name (in plain english) for the dataset e.g.
"""Landcover map of South Africa, 2010"""

The **description** property defines a generalised description of the product. It
will be incorporated into the product abstract that is autogenerated when
subclasses re-implement GenericProduct::abstract(). The description is
free-form text that describes the product and any special information relating
to it.

The **processing notes** property is a freeform text field where any specific notes
and logging information relating to the processing of the dataset can be
recorded. This data should be provided in plain text format.

In the case of geospatial products, their spatial resolution is expressed as
**equivalent scale** (after MD_Metadata > MD_DataIdentification.spatialResolution >
MD_Resolution.equivalentScale) from the ISO19115 specification. Only the
denominator is store so, for example, a value of 50000 indicates the product is
suitable for use at 1:50000 scale or smaller. A default of 1000000 (one
million) shall be assigned to any dataset where the scale is not explicitly
defined.

The **data_type** property describes what type of data is represented in the
dataset. The options for data_type are defined in a dictionary in the
GeospatialProduct model viz:

|| Abbreviation | Name |
| RA | Raster |
| VP | Vector - Points |
| VL | Vector - Lines |
| VA | Vector - Areas / Polygons |

**Note:** The ISO-19115 spec defines an MD_SpatialRepresentationTypeCode but
this is not granular to the feature type level. As such a programmatic mapping
shall be such that types VP/VL/VA are mapped to
MD_SpatialRepresentationTypeCode 'vector 001' and RA is mapped to
MD_SpatialRepresentationTypeCode 'grid'.

The **temporal extent** maps to the gmd::EX_TemporalExtent element in the ISO_19136
standard. e.g.

```
<gmd:temporalElement>
  <gmd:EX_TemporalExtent>
    <gmd:extent>
      <gml:TimePeriod gml:id=\"T1\">
        <gml:beginPosition>2008-01-01</gml:beginPosition>
        <gml:endPosition>2008-03-31</gml:endPosition>
      </gml:TimePeriod>
    </gmd:extent>
  </gmd:EX_TemporalExtent>
</gmd:temporalElement>
```

**Note:** The GenericSensorProduct includes
GenericSensorProduct::product_acquisition_start and
GenericSensorProduct::product_acquisition_end fields but their semantics are
different - they define the actual imagery acquisition period, whereas in Level
4 / GeoSpatial products the temporal_extent_start and temporal_extent_end
describe the complete date range of data represented within the dataset.
If not specified, the temporal extent **start** shall default to the
current data and time at the moment of product ingestion / creation.
If not specified, the temporal extent **end** shall default to be the same
value as the temporal extent start.

The **place** and **place_type** fields are used to define the geographic
region of interest for this dataset. When represented using ISO Metadata, the
region will be reflected in an EX_GeographicDescription element. e.g.

```
<xs:complexType name="EX_GeographicDescription_PropertyType">
  <xs:sequence minOccurs="0">
    <xs:element ref="gmd:EX_GeographicDescription"/>
  </xs:sequence>
  <xs:attributeGroup ref="gco:ObjectReference"/>
  <xs:attribute ref="gco:nilReason"/>
</xs:complexType
```

**Note:** that although the ISO19139 specification allows a sequence (i.e. multiple
geography description elements), our schema only accommodates a single
geographic place. These elements must be defined by the script performing
ingestion which is out of scope for this work package. As such the only current
way to add new geospatial products is manually through the admin panel, or by
writing a simple python tool.


**Note**: Future work package, not in spec:
```
In order to auto-assign place types 1-6 (see dictionaries section
below), the closest place of that type to the centroid of the dataset will be
used. If no region type and region are specified at point of ingestion, the
product shall use default values of 'Local area - nearest named place'
(place_type 7 as listed in the next section) for place_type and are assigned
the named place that is nearest to the centroid of the product geometry (based
on geonames dataset lodged in the **place** dictionary), unless they have been
manually assigned.
```

**Primary topic** is the main categorisation for this dataset. Additional tags can
be assigned to the dataset via the tags field (see below). The topic will be
used when assembling the SAC product id for GeoSpatial products.

**Tags** are used to provide keyword based descriptive information for the product.
Example tags might be: landcover, roads, trig beacons etc.

**Note for Alessandro:** use one of the django tagging apps for this.

Product ID Naming Scheme
.........................................

The following scheme will be used when allocating product ID's to GeoSpatial products:

|| Field | Description |
| TTT | Type, ORD for Ordinal products, CON for continuous products |
| TOPIC | 10 character abbreviation for topic, hyphen padded e.g. ROADS----- |
| TY | 2 character abbreviation e.g. RA for raster |
| PLACENAME | First 10 chars of place name with spaces/whitespace removed e.g. CAPETOWN-- |
| yymmdd           | temporal extent start date                              |
| yymmdd           | temporal extent end date                             |
| LLLL             | processing Level code eg. L4Aa; L4Ab                  |
| EPSG             | EPSG Code for coordinate reference system of dataset |

All id text elements will be converted to upper case. This a sample GeoSpatial
product ID may look like this:

```
ORD_LANDUSE---_VL_ZA--------_110101_110211_L4Ab_4326
```

The order is of the id elements is designed so that when listing products using
e.g. the unix '''ls''' command they naturally appear grouped thematically, then
by data type and then by place.


Geospatial Product Aggregation Rules
.........................................

Geospatial products may be aggregates. That is their lineage may reflect
derivation from one or more other products.

Geospatial Product Dictionaries
.........................................

The following dictionaries are implemented to support the creation of
geospatial products.

Place Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A place type can be one of:

|| ID | Type |
| 1 | Global |
| 2 | Continent e.g Africa |
| 3 | Region e.g. SADC |
| 4 | Country e.g. ZA |
| 5 | State e.g. WCAPE |
| 6 | Town or City |
| 7 | Local area - nearest named place |
| 8 | Quarter Degree Square - using ZA convention e.g 3318BC |

Administering the place types list is not an end-user activity and should be
done in consultation with developers.

Place
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For places, a dictionary based on GeoNames provides a near-exhaustive list of
local areas and towns. The geonames table will be augmented on an adhoc manner
as required via the admin panel. When the place represents an area, the centroid
of that area will be used in the geometry.

The place model looks like this:

|| ID | Type | Name | Long Name | Geometry |
| 1   | 1 | Global | Global |  |
| 2   | 2 | Africa | African Continent |  |
| 3   | 3 | SADC | Southern African Development Community | |
| 4   | 4 | ZA | South Africa | |
| 5   | 5 | GP | Gauteng Province | |
| 6   | 6 | Pretoria | Pretoria | |
| 7   | 7 | Mamelodi | Mamelodi | |

**Note:** Alessandro we need an admin ui for this

%----------------------------------------------------------
%----------------------------------------------------------
%------------------ Ordinal Product     ---------------------
%----------------------------------------------------------
%----------------------------------------------------------

Ordinal Products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Vector and Raster products where data are grouped into discrete classes.

**Concrete or Abstract:** Concrete

For ordinal products, there are three types of accuracy defined:

+ spatial
+ temporal
+ thematic
+

The first two are catered for by the GeospatialProduct abstract base class (
equivalent_scale, temporal_extent_start and temporal_extent_end). Thematic
accuracy for a product is described by adding the fields

Ordinal Product Properties
.........................................


For ordinal products we define thematic accuracy by means of the following fields:
 - class_count
 - confusion_matrix
 - kappa_score
 -


The **class count** property is a compulsory simple numeric value representing
how many classes are defined in the dataset.

The **[confusion_matrix http://en.wikipedia.org/wiki/Confusion_matrix]**
property is a collection of comma separated integers representing (in order):
+ true positive (tp)
+ false negative (fn)
+ false positive (fp)
+ true negative (tn)
+

Thus an entry of 10,5,2,8 signfies:

+ tp=10
+ fn=5
+ fp=2
+ tn=8
+

The confusion matrix entry is not mandatory.

The **[kappa score http://en.wikipedia.org/wiki/Cohen's_kappa]** is a
""statistical measure of inter-rater agreement for categorical items"".
It is represented as a single, non-compulsory real number.

Product ID Naming Scheme
.........................................

The product ID for Ordinal products is described in the GeospatialProduct model
description. Ordinal products are prefixed with the string 'ORD'.

Ordinal Product Aggregation Rules
.........................................

Ordingal products may be part of aggregations and their lineage may include
aggregations.

Ordinal Product Dictionaries
.........................................

No additional dictionaries are introduced by the ordinal product model.


Continuous Products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Synopsis:** Vector and Raster products where data are //not// grouped into
discrete classes, but rather along a continuous value range.

**Concrete or Abstract:** Concrete

Continuous Product Properties
.........................................

For Continuous data there are three additional fields:

 - range_min - floating point not null
 - range_max - floating point not null
 - unit - foreign key
 -

The **range_min** is the smallest value in the continuim of data represented in the
dataset. This value is required.

The **range_max** is the largest value in the continuim of data represented in
the dataset. This value is required.

The **unit** property is a reference to the unit dictionary and it describes
the units of measurement for the data represented in the dataset. This value is
required.


Product ID Naming Scheme
.........................................

The product ID for Ordinal products is described in the GeospatialProduct model
description. Continuous products are prefixed with the string 'CON'.

Continuous Product Aggregation Rules
.........................................

Continuous products may be part of aggregations and their lineage may include
aggregations.

Continuous Product Dictionaries
.........................................

Unit - a look up table storing measurement units:

|| Abbreviation | Name |
| m | Meters
| km | Kilometers |
| etc. ||

