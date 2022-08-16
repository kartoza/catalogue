

% ----------------------------------------------

= Searching for data on the Catalogue =

There are two ways that a user can carry out a search on the catalogue:
+ Basic search - for novice / casual users this is the easiest since it
requires very little domain knowledge.
+ Advanced search - for power users and remote sensing professinals. Requires
moderate to in-depth domain knowledge.
+

These two search environments are described in the sections that follow.

In addition to the advanced search, there is also the option for the user to
refine searches using a 'product id refinement'. In this process, the user can
further filter their search results and view the updated result set in real
time.

== Basic Search ==

Basic search requires only the specification of a date range and optionally the
digitisation of a search area on a map. A wireframe illustrating this is
provided below.


[img/simple-search.png]

At any time, the user can switch to the advanced search dialog (as described in
the next sections) by using the 'Toggle Advanced Search' button.

The map area of the search window (which remains when the search is toggled to
advanced mode) is provided above the search form. A button on the search form
will launch a dialog that shows useful information on using the map. This is
illustrated below.


[img/sac02.png]

The map itself can be customised by selecting the 'Layers' tab to the right and
switching it to use a different backdrop layer. The layers listed may vary
based on the user rights of the person currently logged in. Users that have
been assigned 'partner' status will see higher resolution SPOT5 mosaics (which
are not shown to general users due to licensing restrictions).

The toolbar below the map has a number of tools which can be used to interact
with the map. These allow the activities of:

- zooming in
- zooming out
- panning (shifting the map extents north, south, east or west)
- stepping back in the history of areas of extents places you have panned or zoomed to)
- stepping forward in the history of areas of extents (places you have panned or zoomed to)
- digitising an area of interest for your search
- editing the digitised area of interest
- deleting the digitised area of interest
-

In addition, to the bottom right of the map area, two icons are present. These allow you to:
- restore the map size to default
- grow the size of the map such that if occupies the entire browser window area
-

It should be noted that for the latter item, the search form and related
buttons are shifted down to 'below the fold' (i.e. below the bottom edge of the
window), requiring the user to scroll the window down to once again see the
other input controls on the form.

Below the map are two additional elements:
- the current position of the cursor in decimal degrees
- a scale bar with units in kilometers
-

**Technical note:** The backdrop layers shown in the map areas are in the
'Google Mercator' coordinate reference system (EPSG:90013)

In the image below, the various map elements described above are shown. The map
is shown in 'maximised state'.


[img/sac03.png]



== Advanced Search ==

For casual users, the simple search functionality may be sufficient, but there
is a class of users that demand more control over the search criteria. These
users include SAC staff members, remote sensing specialists and other
professional users. To cater to the needs of this demographic, we have
implemented the advanced search functionality.

=== Optical Products ===

[img/advanced-search-optical.png]

An advanced search for optical products allows the user to create a refined
subset of OpticalProduct records based on various properties.
The options selected in the advanced search form are cumulative.

In the wireframe above, you can see the options available in advanced search.


==== Sensor Details ====

The sensor details area of the form allows the user to define which products
should be found based on the sensors that acquired them.

- When selecting one or more missions, the sensors, modes, types and bands
  entries will be filtered to show only those items permissible for the given
  missions.
- When selecting one or more sensors, the modes, types and bands entries will
  be filtered to show only those items permissible for the given sensors.
- When selecting one or more types, the mode and band entries will be filtered
  to show only those items permissible for the given types.
- When selecting one or more modes, the band entries will be filtered to show
  only those items permissible for the given modes.
- The Mission, Mission Sensor, Type and Mode selectors are constrained to show
  only non-radar products (based on MissionSensor::is_radar property).
-

==== Image Details ====

The image details area of the form allows the user to define which products
should be found based on the product / image properties.

**Cloud cover** can optionally be used to filter products that have been determined
to have less than a given amount of cloud cover. Images with NULL cloud_cover
will be assumed to have 100% cloud cover for purposes of filtering. If the
checkbox next to the cloud cover slider is unchecked, cloud cover will be
ignored when filtering.

The **acquisition angle** is used to limit search results to products that were
acquired with the sensor orientated between a range of viewing angles. Images
with NULL sensor_viewing_angle will be assumed to be excluded when filtering by
sensor viewing angle. If either the min or max value is unpopulated, this will
be ignored in the search.

**Spatial resolution** is used to filter products based on image pixel size. On a
technical note, the pixel size is determined by checking the
GenericImageryProduct::spatial_resolution (which is an inherited property of
optical product). The reason this is used rather than the
AcquisitionMode::spatial_resolution is that the product may have been
resampled during processing so (with the exception of level 1A products), the
resolution may not correspond to the acquisition mode any more. For ease of
use, spatial resolution is grouped as shown in the table below, and the user
may select a single entry from this list.

|| Class | Value Range |
| < 1m | 0 - 1m |
| 1m - 7m | 1 - 7m |
| 7m - 25m | 7 - 250m |
| 25m - 70m | 25 - 70m |
| 70m - 1km | 70 - 1000m |
| > 1km | 1000m + |

**Bands** is used to identify the spectral resolution of the products being
searched for. A user friendly grouping is listed in a select box allowing the
user to select a single band range. These are:

|| Name | Notes |
| Panchromatic | Single band imagery |
| Truecolour RGB (3) | Three bands representing red green blue |
| Multispectral (4-8) | 4 to 8 bands |
| Superspectral (9-40) | 9 to 40 bands |
| Hyperspectral (>40) | more than 40 bands |

Technical note: As with spatial resolution, the number of bands used for filtering is taken
from  GenericImageryProduct::band_count rather than AcquisitionMode::band_count.


==== Row / Path Ranges ====

The specification of row and path ranges can be one in one of three ways:
+ A range e.g. [0,15] means include all rows/paths inclusively from 0 to 15.
+ A list e.g. 1,5,3 means include specifically row or paths numbered 1, 5 and 3.
+ A single item e.g. 10 means include only that row/path
+

The sematics of what constitutes a row and path (in a geospatial sense) varies
from sensor to sensor. The search algorithm makes no special allowance for this
so it should be noted that a row/path search of 30,50 for two different sensors
my return imagery covering disparate areas.

**Note:** Although the normal expectation is that both a row and a path are
provided, this is a soft requirement, and a user may enter one or the other (or
neither) if they desire.

==== Processing levels ====

The products can be filtered according to their processing level. The list of
processing level list is not dynamic (i.e. it does not ajust its entries based
on mission, sensor etc. selections) as it would be prohibitively CPU intensive
to do so. As such there is no guarantee of being at least one product for each
of the listed processing levels.

One or more processing levels can be selected. If none are selected, it is
assumed that products at all levels should be queried when searching.

==== Geometry ====

A geometry can be defined for a search in one of four ways:
+ Digitising an area on the map directly
+ Uploading a shapefile or kml demarcating the area of interest
+ Specifying point and radius geometry in an input box
+ Specifying a bounding box in an input box
+

[img/sac01.png]

For digitising, the user should select the 'capture polygon' tool on the map.

For the geometry upload functions, only the first feature in the uploaded
shapefile / kml will be used. The shapefile should have a polygon geometry type
and have a Coordinate Reference System of EPSG:4326 (Geographic WGS84).

The input box for geometry can be used to create a circular geometry by
entering the coordinate of the center point and a radius in kilometers. For example:

```
20.5,-32.3,100
```

The values should be entered as easting (use negative number to indicate west),
northing (use negative number to indicate south), radius (in km). The
easting/northing values are specified in decimal degrees.

Finally, the bounding box can also be entered in the form:

```
xmin,ymin,xmax,ymax
```

For example:

```
20,-34,22,-32
```

==== Date Ranges ====

When conducting a search with the advanced search tool, the user can specify
one or more date ranges. The start date for any date range will be restricted
to be no earlier **1 January 1972**. The end date will be restricted to be no
later than the current date. No facility is made for including time in the date
range.

The process of defining date ranges consists of:
- Selecting a start date in the 'start' calendar
- Selecting an end date in the 'end' calendar
- Clicking the 'add' icon to add the date range to the range list
-

The user can remove a range from the list by selecting it and clicking the
'remove' icon.


==== Executing the search ====

Once the user has completed the search definition process, pressing the
'search' button will cause the search request to be posted to the server. If
there are any validation errors, the user will be returned to the search form
and the validation errors will be indicated. Assuming there were no errors, the
user is redirected to the search results page.

== Radar Search ==

[img/advanced-search-radar.png]

Radar products share many properties in common with Optical products, so you
should read the description of the Advanced Search for Optical Products above
first. There are five principle differences in the Radar Search dialog:
+ There is no option to choose a cloud cover rating.
+ There is an option added for polarisation mode.
+ Acquisition angle is replaced with incidence angle (RadarProduct::incidence_angle).
+ The Mission, Mission Sensor, Type and Mode selectors are constrained to show
  only radar products (based on MissionSensor::is_radar property).
+ There is no option to choose a number of bands.
+

It should be noted that radar products will often not have row/path data. In
this situation the row/path and offsets should have been defined using the
product centroid system as illustrated below. For this reason the row/path inputs
remain.

[img/centroid_based_row_path.png]

The centroid based the row/path schema uses N/S/E/W suffixes to indicate
hemisphere, however the row/path range definition expects numeric entries. As
such negative values in the row box will indicate west and negative values in
the path will indicate south.

== Generic Imagery Search ==

The purpose of the generic imagery search is to allow the user to locate
GenericImageryProducts and their class heirarchy descendents (currently Optical
and Radar products). The generic imagery search uses a reduced set of options
in order to cater for the range of different imagery types.

[img/advanced-search-generic.png]

In particular:

- There are no options related to the selection of a mission,
sensor, sensor type or acquisition mode.
- There are no options related to acquisition angle or incidence angle.
- There are no options relating to polarisation mode.
- There are no options relating to Row / Path.
-


Because of the diverse results that may be returned apon completing a generic
imagery search, there is no post search product id filtering catered for.
However the user may refine the search from the search results screen where
they will be returned to a pre-populated instance of the original search form.

== GeospatialProduct Search ==

[img/advanced-search-geospatial.png]

