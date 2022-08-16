Catalogue Schema : Orders
------------------------------------------

**Note:** Before reading this section please read & understand the products schema notes.

The purpose of the order application logic is to allow a user to easily order one or
more products. Since each order can consist of one or more products, and each
product can be included in many orders, a 'many to many' relationship exists
between products and orders. This is realised via the **SearchRecord** model.
This SearchRecord model is also described in the Search section. As a recap,
the process of creating SearchRecords is achived by carrying out a search.
Initially when a search is carried out, SearchRecords are transient - that is,
they are not persisted in the databse. Once a user adds a SearchRecord
(representing a single product) to their basket, the SearchRecord is assigned a
User id and persisted in the database. A users basket or cart is thus the
collection of SearchRecords owned by them but that have no Order allocated to
them.

At the point of deciding to proceed with an order, the user is directed to the
Order page, a wireframe for which is shown below.

[img/order-wireframe.png]

The purpose of the order page is to allow the user to specify details relating
to their intended order and to proceed with the order initiation thereafter.
Two levels of customisation are allowed for when creating an order:

+ options that are global to the order can be defined
+ options that are specific to each product within the order can be defined
(overriding the global options where applicable)
+

The specific global and options are specified in the sections that follow. The
global versus option specification process is also illustrated in the wireframe
provided above.

**Note:** The ordering system does not (yet) implement an e-commerce system and
the processing of orders is not yet automated. When an order is placed for a
product, the notifications to operators are automatic, but the process of
fulfilling the orders remains operator controlled.

Schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The schema relating to product orders can be summarised as follows:

[img/product-orders.png]

This schema will be explained in more detail in the sections that follow.

We can express the above diagram verbally:

- Orders are instances of the Order model
- Each order has one or more SearchRecords associated with it
- Each order has a DeliveryDetail record associated with it
- Each SearchRecord //optionally// has a DeliveryDetail record associated with it
- An Order is owned by a User
- Each SearchRecord is owned by a User (which should match the Order owner)
- The DeliveryDetail record associated with an Order encapsulate the
  Projection, Datum, Processing level, Resampling Method and File Format that
  **all** the products of that order should be delivered in.
- The DeliveryDetail record associated with an Order optionally stores Order level
  AOI / clip mask used by staff to use to clip the products before shipping ordered
  products to the client
- The DeliveryDetail record associated with an SearchRecord encapsulate the
  Projection, Datum, Processing level, Resampling Method and File Format that
  the **specific product**  associated with that SearchRecord should be
  delivered in.
- Each order has a current order status and history of OrderStatus records.
- Each order has a deliver method associated with it (e.g. ftp, portable disc,
  dvd etc.)
-

Operational notes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following operation notes should be understood for the order system:

General Users
.........................................

- In order for a user to initiate an order, they must have completed the
  details of their personal profile. If this is not the case, they will first
  be redirected to their profile page where they can complete their details. On
  completion of their details, they are returned to the order page.
- The user can remove products from the order at the point of making the order.
  However if he removes the last product from the order, his basket becomes
  empty and no order should be able to be placed.
- The user cannot edit the order after it has been placed.
- The user can request an order be cancelled after it has been placed, but
  should be advised that their may be a fee payable if products have already
  been procured.
- The user can see a list of the orders they have made and their statuses.
  Clicking on a specific order will take them to a detailed view of the order
  where they can view its current status and review the products associated
  with that order, and the history of status changes made for that order.
- The list of orders visible to a user is restricted to those owned by that
  user.
- The user's address and other contact details are shown on the order form,
  with a link that will take them to their profile editor so that they can
  update their details. After updating their details they are returned to
  the order.
- The user's avatar is shown on the order so that the process feels
  personalised to them.
- For each status change to an order (including the initial placement of the
  order itself), the user will recieve an email which will be provided in both
  plain text and html format (falling back to plain text if html is not
  supported by the email client being used). The email will be visually
  consistent with the order page and include links to products that are
  available for immediate download (see below).
-

SAC Staff
.........................................

- SAC Staff can view a master list of all orders and filter / sort those orders
  by status, owner etc.
- Staff can view any order and as appropriate adjust it's status (e.g. open, in
  process, cancelled etc).
- No status change will be accepted without keeping a log of who made the
  change and what the reason was for the change.
- Each status change is timestamped so that a proper audit trail can be
  established.
- The order comments system should be the primary communication mechanism with
  the client, as it will provide a thorough audit trail.
-

Instant product delivery
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases products are available for instant download. The indicator for
this is a populated GenericProduct::local_storage_path field which points to a
valid resource on disk.

Where products originate from DIMS, an extract request will be made via the
Ordering Service for Earth Observation products (OS4EO) implemented on the DIMS
server.

In cases where instant delivery is made, download links will be included in
notification emails and in the order summary visible to operators.

In the case of DIMS OS4EO extracted products, these will be flushed after a
period of 1 week from the server file system and the user advised to this fact
when this happens.

OS4EO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Django management command, suitable to run from cron jobs, will take care of
the OS4EO order placing for GenericSensorProduct.

The followin fields in SearchRecord are involved:

  + internal_order_id
  + product_ready
  + download_path

One field in GenericSensorProduct tells us if the products is in DIMS and
can be ordered with OS4EO:

  + online_storage_medium_id

Logic is:

 + only GenericSensorProduct with online_storage_medium_id NOT NULL are DIMS products
 + if internal_order_id is not set, OS4EO order was not yet placed
 + if internal_order_id is set but download_path is NULL, the product
  OS4EO order was placed but not yet completed

Pseudo code:

 + for each pending order (i.e. GenericSensorProduct items wich are not ready from orders with status that is not 'Cancelled', 'Awaiting info from client', 'Completed')
  + if the product is ordered (internal_order_id is set) checks order status
    + if the status is 'completed' check the file availability
      + if the product is available,
        + fill download_path and save the item (this triggers product_ready = True)
        + if all other items from the same order are ready
          + change order status to 'Completed'
  + if the product is not ordered, order it:
    + call the OS4EO service to place the order, fill
      internal_order_id with the id supplied from OS4EO
    +


OS4EO configuration
.........................................

The WS endpoint is specified in global settings.py:

```
OS4EO_SERVICE_ENDPOINT = "http://196.35.94.243/os4eo"
```

OS4EO command
.........................................

**Note:** the command is not yet finished nor tested because of some problems that Werum should solve: http://redmine.linfiniti.com/issues/21

To see all available options you can call the command with `-h` or `help`
parameter:

```
$ python manage.py os4eo_order -h
Usage: manage.py os4eo_order [options]

Place orders

Options:
  -v VERBOSITY, --verbosity=VERBOSITY
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=all output
  --settings=SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath=PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Print traceback on exception
  -t, --test_only       Just test, nothing will be written into the DB.
  --version             show program's version number and exit
  -h, --help            show this help message and exit
```

OS4EO client library
.........................................

The client library is located in catalogue/os4eo_client.py, tests and
example usage are in catalogue/tests/os4eo_client_test.py.

The following methods have been implemented so far:

 + GetCapabilities
 + Submit
 + GetStatus
 + DescribeResultAccessResponse
 +


**Note:** the library development has been carried out incrementally and only the minimum
set of parameters needed to successfully place and handle an order has been implemented so far.
Additional parameters can be easily added in the future as needed.


Sample session:
```
>>> from django_project.catalogue.os4eo_client import OS4EOClient
>>> os4eo = OS4EOClient(debug=False)

>>> os4eo.GetCapabilities()
[<Element '{
set of parameters needed to successfully place and handle an order has been implemented so far.
Additional parameters can be easily added in the future as needed.


Sample session:
```
>>> from catalogue.os4eo_client import OS4EOClient
>>> os4eo = OS4EOClient(debug=False)

>>> os4eo.GetCapabilities()
[<Element '{http://www.opengis.net/ows}Operation' ...

Place single order

>>> single_id, single_submit_status = os4eo.Submit( \
  ['SPOT5.HRG.L1A:/eods_hb_pl_eods_XXXXB00000000253027605285/eods_hb_pl_eods_//SPOT5.HRG.L1A'], \
  '100001', \
)

Place multiple

>>> multiple_id, multiple_submit_status = os4eo.Submit( \
  ['SPOT5.HRG.L1A:/eods_hb_pl_eods_XXXXB00000000253027605285/eods_hb_pl_eods_//SPOT5.HRG.L1A', \
  'SPOT5.HRG.L1A:/eods_hb_pl_eods_XXXXB00000000253027605866/eods_hb_pl_eods_//SPOT5.HRG.L1A' ], \
  '100002', \
)


>>> os4eo.GetStatus(single_id)

>>> os4eo.GetStatus(multiple_id)

>>> os4eo.GetStatus(single_id, True)

>>> os4eo.GetStatus(multiple_id, True)

>>> os4eo.DescribeResultAccess(single_id)

>>> os4eo.DescribeResultAccess(multiple_id)

```

----------------------------
**Note:** elementsoap library was used to develop the webservice os4eo_client library (added in REQUIREMENTS.txt)
buta patched version was used instead of the official one , the patched version has enhanced debug
capabilities. When debug is not needed anymore, the standard library can be used, just delete the "debug"
parameter from the function calls in the main script.


Filtering of CRS's
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The projections list can be long and irrelevant for many images if the complete
list is shown. Thus the following logic applies:

- For single product properties, when listing utm zones for the projection
  combo, only the zones in which the image bounding box falls, and the two zones to
  either side of that are shown.
- For Order records, only utm zones that intersect with the image bounding box of one or
  more of the products listed in the order should be listed, along with the two
  adjacent zones on either side of each image.
- EPSG:4326 Geographic is always listed
- EPSG:900913 Google Mercator is always listed
-

Datum
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently only one datum is supported for order requests - WGS84:

 || id | name |
 |  1 | WGS84 |

Until additional datum options are available, the datum is not shown to end
users since providing a datum choice selection with only a single entry is
superfluous.

Processing Levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A user can request that a product be delivered at a different processing level
to the one recorded for the project. For example a user can request that an
image at L1A be supplied as a L3Aa product.

The processing levels are discussed in more detail in the 'dictionaries'
section of the product schema discussion.

----------------------------
**Note:** Wolfgang to supply list of rules on how processing levels may be
assigned.

File Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The user making the order can request from one of a number of different
delivery file formats. Currently these formats are defined as:

 || Id |                  Name                   |
 | 1 | GeoTiff                                   |
 | 2 | ECW - ERMapper Compressed Wavelet         |
 | 3 | JP2 - JPEG 2000                           |
 | 4 | ESRI -ShapeFile (Vector products only)    |

Packaging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


By default products should be delivered inside of standard SAC packages. The
packages will be placed in an ephemeral place in the file system (one where
files older than 7 days are flushed daily).

Staff Order Notifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The system can send notifications emails to staff based on product class or
sensor ordered. If you look in the admin ui there is already a way to allocated
users to sensors - we just need to extend that idea to include product classes
as everything is not sensor based anymore.

Product types are not aggregated. From a user perspective, staff log in and
choose which sensors and product classes they subscribe to by picking one or
more items from a select list.

---

In product id search, the user be able to put in ranges or comma
delimited lists of rows and paths too e.g.

Row: 80
Path 80

or
Row: 80-83
Path: 80-83

or
Row: 80,90,112
Path: 90, 101

Tasking Requests
------------------------------------------

The TaskingRequest model is a subclass of the Order model. Tasking requests
differ from orders in that they have no products associated with them. Instead
a tasking request has a sensor associated with it and other information
germaine to tasking a satellite to capture and image (or other remotely sensed
data) of a specific location.

Taskable Sensors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The SensorType model includes an is_taskable member which is used to
determine which sensors a user may select from when making a tasking request.
