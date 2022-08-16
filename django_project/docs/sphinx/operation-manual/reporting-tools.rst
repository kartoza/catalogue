

% Leave the two blank lines above

== Catalogue Reporting tools ==

The catalogue provides numerous interactions for users and is continually being
updated with new metadata records. It is useful to produce reports that allow
SANSA staff to obtain the pulse of the system. These reports cover 4 main
areas:

+ Data holdings
+ Search activities
+ Visitor statistics
+ Order and tasking activities
+

The reports can be obtained in one of two ways:

+ Visiting the 'staff' area of the web site and selecting from the reports
  presented there
+ By direct email. Here staff can nominate which reports they wish to receive,
  and with which frequency they receive them
+

**Note:** Only 'staff' members are elegible to receive reports.

Reports sent by email will be in either rich html format, or as pdf attachments.

=== Order summaries ===

==== Order summary table ====

The order summary table is accessible from the **Staff -> Orders list** and for
individual users from **Popular Links -> My orders**. For individual users,
only their own orders will be listed. In all other respects, both tables are
the same. The table contains the following headers:

|| Id | Date | Status | Placed by | View |

When clicked, the headers will set the sort order for the table.

Above the table is a chart which displays total orders by status. For
individual users, this chart shows only their own orders.

The summary report link on the summary table will return the user an on-the-fly
created order summary report in pdf format as described below.

==== Order summary report ====

The order summary report will be sent to nominated users at chose interval of
daily, weekly or monthly. It can also be generated on-the-fly from the staff 
admin interface.

The orders summary report contains the following information:

- How many orders have been created in the reporting month
- How many orders have been closed in the reporting month
- A break down of all open orders by status (accepted etc.)
- A break down of all open orders by age
- A break down of all orders by customer
-

Format : pdf

=== PDF report generation ===

To generate on-the-fly PDF reports we use **Pisa**
http://www.xhtml2pdf.com which is an HTML/XHTML/CSS to PDF converter
written in Python and based on Reportlab Toolkit, pyPDF, TechGame
Networks CSS Library and HTML5lib. This apporach doesn't break normal
Django application development, as we can use Django Templating engine
to prepare HTML for PDF rendering.

Graphs in PDF reports are created using Google Chart API through
**pygooglechart** Python library.

== Heatmap implementation ==

Heatmap is based on a pre-calculated data which enables offline map
generation for specific periods of time, i.e. last week, last month,
last year, etc.

It's based on discovering intersections of user area of interest
geometry for each search, with quarter degree grid for the whole
world. These intersections are then summarized for each //grid cell//
per day. To create actual heatmap we are using following GDAL
utilities (//gdal_grid//, //gdaldem// and //gdalwrap//) and
ImageMagick to combine images into meaningful map.

Heatmap data and rendering is updated by a scheduled background
process, which creates required heatmaps. Heatmap visualization is
currently implemented as simple OpenLayers Image layer.


=== Heatmap configuration ===

Following steps are required to create and configure heatmap
generation functionality.

+ execute database preparation script
  - ``psql -f sql/migrations/200-heatmap-reporting.sql -d sac``
  - this script cleans existing invalid geometry data, creates tables
    //heatmap_grid// and //heatmap_values// and database procedures
    //heatmap_grid_gen//, //update_heatmap// and //heatmap//
+ execute data initilization script
  - ``psql -f sql/migrations/201-heatmap-bootstrap.sql -d sac``
  - this script first generates quarter degree grid by calling 
    ``SELECT heatmap_grid_gen(0.25);``
  - then updates data in //heatmap_values// table by calling 
    ``SELECT update_heatmap();`` without parameters


=== Heatmap creation ===

To create heatmaps we use ``generate_heatmaps.sh`` script which is in
project //scripts// folder. This script is configured to be executed
relative to //scripts// folder, however, variables which control
script behavior and output folders can be modified in script itself.

Script is preconfigured to create 4 heatmaps based on last week, last
month, last three months and full dataset. 

First we update //heatmap_values// table with new data, if new data
exists. Then for each specified heatmap we use //gdal_grid// to
extract point data from database for required date range and
apply //invdist// spatial data approximation function, and create
raster of required size. After gridding we colorize raster
using //gdaldem// by using colors specified in ``heatmap.txt``
file. In the end we transform created raster to world mercator
(EPSG:900913) projection using //gdalwrap// and overlay prepared
country borders over it, using ImageMagick.

Script runtime depends on amount of data. Currently it takes around 30
minutes to generate 4 heatmaps, with most of the time spent generating
full dataset heatmap. This script should be executed as a scheduled
background process utilizing cron scheduling daemon.


== World borders data ==

World borders data is essential for generating reports and
heatmaps. For this purpose we are using preprocessed datasat available
at http://thematicmapping.org, specifically
http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip. This
dataset is already in the repository ``resources/world_borders``
directory.


=== World borders loading ===

Process of loading world borders is done in three steps:
+ execute database preparation sql script
  - ``psql -f sql/migrations/202-report-query-by-country.sql -d sac``
  - this script creates required database table and indexes
  - **Note:** on a new installation this step is not required, because this 
    table is created on project initialization
+ importing world borders data to world borders table
  - ``./manage.py runscript load_world_borders``
+ execute data sanitizing script
  - ``psql -f sql/migrations/203-worldborders-data-sanitization.sql -d sac``
  - this script removes ``' ( )`` characters which break PISA report 
    generation functionality


**Note:** all paths are relative to project root dir


