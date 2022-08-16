Search Schema
------------------------------------------

This section covers the logic and schema related to search. The search process
begins when the user clicks 'Search' on the main application toolbar. They have
the option then of performing a simple search or an advanced search. Regardless
of which search type they use, the outcome is the same - the catalogue
application internally creates a collection of unserialised **SearchRecord**
objects. These objects are simple mappings between a search and the products
that match the criteria of that search.

The matching search records are shown to the user as a paginated table of
entries, each entry corresponding to one product. If a user chooses to add that
product to their basket, the SearchRecord is then serialised (saved
persistently in the database). By definition, the basket can be defined as
//"all serialised **SearchRecords** for a given user which have **no** Order
associated with them"//. In the ordering section we describe the order process
in more detail.



Simple search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simple search is the default search interface.
The use can enter the following search criteria:

 + date ranges (multiple, required)
 + digitized area of interest (optional)

A new search record is created when the user submits a valid form.

Advanced search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the user press "Advanced search", many more fields appear and a complex
interface allows to specify almost all other search criteria, which can
be different according to the selected product type.

For sensor-based products, the sensor criteria is always mandatory and an Ajax
powered method, keeps available choices consistent in the sensor-related
criteria (i.e. when the user selects a certain mission, only the sensors available
in that mission are shown in the sensor box).


A new search record is created when the user submits a valid form.

**Note**: this Ajax U is similar but not identical to what happens in the Product ID
search interface: in advanced search, the Ajax call takes only care of drilling
down the mission-sensor hierarchy without issuing a new search query on every change.


Product ID search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This search view is only available for optical search products because
other types have no Product ID implementation.

The aim of this function is to facilitate search results narrowing of
an existing advanced search results set, through a UI based on the product ID.

A link to the search view is available from the search results window only
if the search is an advanced search for optical products.

**Note**: every search submit will not create a new search but modifiy the original one.
This is not identical to the behaviour of the modify search view which always creates
a new search object.


Ajax search implementation details
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Ajax product id search has a JS handler which issues an Ajax post call
on every option select change.

The Ajax call is received by `catalogue.views.search.ProductIdSearch` which
takes care of:

  + updating the Search object with the new parameters
  + calls catalogue.views.searcher.Searcher.describeQuery, that
    return a JSON object containing
      + the query description (to update the "Search summary" box)
      + the query SQL (if settings.DEBUG is set)
      + a dictionary of values for the select options (e.g.: sensor_type,
        acquisition:mode etc.)
      +

The JS code responsible for this is in the view template catalogue/templates/ProductIdSearch.html
and updates the select options hiding/showing the available values

**Note:** in order to avoid a narrow/one-way only search, all options must be
  nullable, this means that also sensors multiple select was changed to be not
  mandatory.

**Note:** catalogue.views.searcher.Searcher.describeQuery accepts an optional
  parameter (unset_only=False) that if activated, returns only values for
  parameter that are not set in current Search, this allows for a pivot-like
  way of obtaining the values: "tell me all the possible values for
  the parameters that are not set", this can be useful if the UI do not use
 '*' or other similar mechanisms to delete a parameter from the filter.


