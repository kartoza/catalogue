// ==ClosureCompiler==
// @compilation_level SIMPLE_OPTIMIZATIONS
// @output_file_name catalogue.js
// ==/ClosureCompiler==

/* Compress this file to catalogue.js using google's closure compiler at
  http://closure-compiler.appspot.com/home */

/* ------------------------------------------------------
 *  Global variables
 *  ------------------------------------------------------ */

/* Setup the style for our scene footprints layer and enable
 * zIndexing so that we can raise the selected on above the others
 * see http://openlayers.org/dev/examples/ordering.html */

var DestroyFeatures = OpenLayers.Class(OpenLayers.Control, {
    type: OpenLayers.Control.TYPE_BUTTON,
    trigger: function() {
        this.layer.destroyFeatures();
    }
});
OpenLayers.Renderer.VML.prototype.supported = function() {
    return (OpenLayers.Util.getBrowserName() == "msie");
}
OpenLayers.Renderer.VML.prototype.initialize = function(containerID) {
    OpenLayers.Renderer.Elements.prototype.initialize.apply(this, arguments);
}
var mSceneStyleMap = new OpenLayers.StyleMap(
  OpenLayers.Util.applyDefaults(
  {
    fillColor: "#000000",
    fillOpacity: 0.0,
    strokeColor: "yellow",
    graphicZIndex: "${zIndex}"
  },
  OpenLayers.Feature.Vector.style["default"])
);
var mDrawingStyleLookup = {
 'yes' : {strokeColor: "red"},
 'no' : {strokeColor: "yellow"}
};
var mContext = function(feature)
{
  return feature;
};

mSceneStyleMap.addUniqueValueRules("default", "selected", mDrawingStyleLookup, mContext);
var mNavigationPanel = null;
var mMapControls = null;
var mWKTFormat = null;
var mVectorLayer = null;
var mMap = null;

/*--------------------------------------------------------
 * Things to run on any page first load that uses this lib
 -------------------------------------------------------- */
$(document).ready(function()
{
  //setup help dialog
  setupSceneIdHelpDialog();
  //block the user interface when an ajax request is sent
  $(".blocking-link").live('click',block);
});


/*--------------------------------------------------------
 * Global functions
 -------------------------------------------------------- */
/* Globally implemented wait overlays */

function unblock()
{
  $.unblockUI();
}

function block()
{
  $.blockUI({ message: '<h2><img src="/media/images/ajax-loader.gif" /> Loading...</h2>',
      css: {
        border: '1px solid #000',
        padding: '15px',
        backgroundColor: '#fff',
        '-webkit-border-radius': '10px',
        '-moz-border-radius': '10px',
        opacity: .9,
        color: '#000'
        }
      });
}

function getLayerByName( theName )
{
  if ( ! mMap )
  {
    return false;
  }
  myLayers = mMap.getLayersByName( theName );
  if ( myLayers.length > 0 )
  {
    return myLayers[0];
  }
  else
  {
    return false;
  }
}
/* ------------------------------------------------------
 * OpenLayers WKT manipulators
 * -------------------------------------------------------- */
function readWKT(wkt)
{
  // OpenLayers cannot handle EWKT -- we make sure to strip it out.
  // EWKT is only exposed to OL if there's a validation error in the admin.
  var myRegularExpression = new RegExp("^SRID=\\d+;(.+)", "i");
  var myMatch = myRegularExpression.exec(wkt);
  if (myMatch)
  {
    wkt = myMatch[1];
  }
  var feature = mWKTFormat.read(wkt);
  if (feature) {
    return feature.geometry;
  }
}
function writeWKT(geometry)
{
  myGeometry = geometry.clone();
  myUnprojectedGeometry = reverseTransformGeometry(myGeometry);
  document.getElementById('id_geometry').value =
   'SRID=4326;' + mWKTFormat.write(new OpenLayers.Feature.Vector(myUnprojectedGeometry));
}
function addWKT(event)
{
  // This function will sync the contents of the `vector` layer with the
  // WKT in the text field.
  // Make sure to remove any previously added features.
  if (mVectorLayer.features.length > 1){
    myOldFeatures = [mVectorLayer.features[0]];
    mVectorLayer.removeFeatures(myOldFeatures);
    mVectorLayer.destroyFeatures(myOldFeatures);
  }
  writeWKT(event.feature.geometry);
}
function modifyWKT(event)
{
  writeWKT(event.feature.geometry);
}

/* ------------------------------------------------------
 * Other OpenLayers Helpers
 * -------------------------------------------------------- */
// Add Select control
function addSelectControl()
{
  var select = new OpenLayers.Control.SelectFeature(mVectorLayer, {
      'toggle' : true,
      'clickout' : true
  });
  mMap.addControl(select);
  select.activate();
  mVectorLayer.selectFeatureControl = select;
}
function enableDrawing ()
{
  mMap.getControlsByClass('OpenLayers.Control.DrawFeature')[0].activate();
}
function enableEditing()
{
  mMap.getControlsByClass('OpenLayers.Control.ModifyFeature')[0].activate();
}
/*
 * Populates mMapControls with appropriate editing controls for layer type
 * @note Since we are putting the controls into a panel outside the map,
 * we need to explicitly define the styles for the icons etc.
 */
function setupEditingPanel(theLayer)
{
  var myDrawingControl = new OpenLayers.Control.DrawFeature(theLayer,
      OpenLayers.Handler.Polygon, {
	  'displayClass': 'olControlDrawFeaturePolygon',
	  'title': '<b>Capture polygon</b> left click to add points, double click to finish capturing'
      });
  var myModifyFeatureControl = new OpenLayers.Control.ModifyFeature(theLayer, {
      'displayClass': 'olControlModifyFeature',
      'title': '<b>Modify polygon</b> left click to move/add points, hover and press <i>delete</i> to delete points'
  });
  var myDestroyFeaturesControl = new DestroyFeatures({
      'displayClass': 'destroyFeature',
      'title':'<b>Delete polygon</b> deletes polygon',
      'layer': theLayer
      }
    );
  mMapControls = [myDrawingControl, myModifyFeatureControl, myDestroyFeaturesControl];
  mNavigationPanel.addControls(mMapControls);
}

//A little jquery to colour alternate table rows
//A bit of a hack, this function is used as a call back when ajax pages load
function zebraTables()
{
  $("table tr:even").addClass("even");
  $("table tr:odd").addClass("odd");
}

 /*
 * Things to do on initial page load...
 *
 */
$(function()
{
  $("#accordion").accordion({ autoHeight: false });
  zebraTables();
});

function clearSearchResults()
{
  // Remove the temporary scenes layer
  myLayer = getLayerByName("scenes");
  if (myLayer !== false)
  {
    var select = myLayer.selectFeatureControl;
    if (select) {
        select.deactivate();
        myLayer.map.removeControl(select);
    }
    myLayer.destroy();
  }
}
function prepareFancy()
{
  $("#accordion").accordion("activate", 1);
  $("a#large_preview").fancybox(
   {
     "overlayShow"           : false,
     "imageScale"            : true,
     "zoomSpeedIn"           : 600,
     "zoomSpeedOut"          : 500,
     "easingIn"              : "easeOutBack",
     "easingOut"             : "easeInBack",
     "frameWidth"            : 500,
     "frameHeight"           : 500
    });
}
function showMiniCart( )
{
  myShowAccordionFlag = true; //true unless specified otherwise by fn args
  if ( arguments.length == 1 ) //check of a flag was passed to indicate whether to activate the accordion
  {
    myShowAccordionFlag = arguments[0];
  }
  // Refresh the cart layer
  myLayer = mMap.getLayersByName("Cart")[0];
  if ( !myLayer )
  {
    return;
  }
  //Trick to trigger a refresh in an openlayers layer
  //See: http://openlayers.org/pipermail/users/2006-October/000064.html
  myLayer.mergeNewParams({'seed':Math.random()});
  myLayer.redraw();
  // refresh the cart table
  $("#cart").load("/showminicartcontents/","", zebraTables);
  if ( myShowAccordionFlag )
  {
    $("#accordion").accordion("activate", 2);
  }
  $("#working").slideUp('slow');
}
function addToCart( theId )
{
  // Show a wait image before we hit our ajax call
  $("#working").html('<p>Adding, please wait...<img src="/media/images/ajax-loader.gif"></p>');
  $("#working").slideDown('slow');
  $.get("/addtocart/" + theId + "/?xhr","", showMiniCart);
  // prevent page jumping around on empty hyperlink clicks
  return false;
}
function layerRemoved()
{
  // Callback for when a layer was removed from the cart
  // - to trigger redraw of the cart layer
  myLayer = mMap.getLayersByName("Cart")[0];
  //Trick to trigger a refresh in an openlayers layer
  //See: http://openlayers.org/pipermail/users/2006-October/000064.html
  myLayer.mergeNewParams({'version':Math.random()});
  myLayer.redraw();
  $("#working").toggle('slide');
  return false;
}
function removeFromCart(theId, theObject)
{
  $.get("/removefromcart/" + theId + "/?xhr","",layerRemoved);
  theObject.parent().parent().remove();
  //-1 for the header row
  var myRowCount = $("#cart-contents-table tr").length - 1;
  $("#cart-item-count").html( myRowCount );
  if ((myRowCount < 1) && ($("#id_processing_level").length != 0))
  {
    //second clause above to prevent this action when minicart is being interacted with
    window.location.replace("/emptyCartHelp/");
  }
  return false;
}
function removeFromMiniCart(theId, theObject)
{
  //theObject is the remove icon - we use it to find its parent row and remove that
  $("#working").html('<p>Removing, please wait...<img src="/media/images/ajax-loader.gif"></p>');
  $("#working").slideDown('slow');
  removeFromCart( theId, theObject );
}
function showCart()
{
  $("#cart").load("/showcartcontents/","", zebraTables);
  $("#working").slideUp('slow');
}

function getElement( id )
{
  if (document.getElementById)
  {
    return document.getElementById(id);
  }
  else if (document.all)
  {
    return document.all[id];
  }
  else if (document.layers)
  {
    return document.layers[id];
  }
  else
  {
    return 0;
  }
}



function getFeatureByProductId( theProductId )
{
  myLayer = getLayerByName("scenes");
  if (myLayer !== false)
  {
    var myFeatures = myLayer.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      if(myFeatures[i].product_id == theProductId)
      {
        return i;
      }
    }
  }
  return -1; //not found
}

/*
 * Load a paginated search result page into the table
 */
function revealTable()
{
  zebraTables();
  $("#working").slideUp('slow');
  $("#working").html('');
  $("#table").slideDown('slow');
}

function loadPage( theNumber, theSearchGuid )
{
  $("#table").slideUp('slow');
  // Show a wait image before we hit our ajax call
  $("#working").html('<p>Loading, please wait...<img src="/media/images/ajax-loader.gif"></p>');
  $("#working").slideDown('slow');
  $("#results-table").parent().load("/searchpage/" + theSearchGuid + "/?page=" + theNumber,"",revealTable);
}

function resizeTable()
{
  myWindowHeight = $( window ).height();
  myHeaderHeight = $( '#header' ).height();
  myMapHeight = $( '#map' ).height();
  myFooterHeight = $( '#footer' ).height();
  myPadding = 140; //cater for white space on page
  myTableHeight = myWindowHeight - ( myHeaderHeight + myFooterHeight + myMapHeight + myPadding );
  if ( myTableHeight < 200 )
  {
    myTableHeight = 200;
  }
  $( "#results-table" ).height( myTableHeight );
}

// Get feature info implementation for openlayer
// see http://trac.openlayers.org/wiki/GetFeatureInfo
function showFeatureInfo(event)
{
  $("#working").html('<p>Adding, please wait...<img src="/media/images/ajax-loader.gif"></p>');
  $("#working").slideDown('slow');
  myMousePos = mMap.getLonLatFromPixel(event.xy);
  myBoundingBox = mMap.getExtent().toBBOX();
  myPixelX = event.xy.x;
  myPixelY = event.xy.y;
  myMapWidth = mMap.size.w;
  myMapHeight = mMap.size.h;
  $("#mapquery").slideDown('slow');
  $('#hidemapquery').live('click', function() {
      $("#mapquery").slideUp('slow');
  });
  $.get("/getFeatureInfo/" + myMousePos.lon + "/" + myMousePos.lat + "/" + myBoundingBox + "/" + myPixelX +"/" + myPixelY + "/" + myMapWidth + "/" + myMapHeight +"/", function( data ) {
  $("#mapquery").html("<p><input type=button id='hidemapquery' value='Hide'></p>" + data);
  });
  Event.stop(event);
  $("#working").slideUp('slow');
}

function setHTML(response)
{
  $("#mapquery").html("<p><input type=button id='hidemapquery' value='Hide'></p>" + response.responseText);
  $("#mapquery").slideDown('slow');
  $('#hidemapquery').click(function()
  {
    $("#mapquery").slideUp('slow');
  });
}

function createLegend()
{
  //create the legend
  myLayers = mMap.layers;
  for (var i = 0; i < myLayers.length; i++)
  {
    myLayer = myLayers[i];
    myLayerName = myLayer.name;
    myVisibility = myLayer.visibility;
    myCheckedString = "";
    if ( myVisibility )
    {
      myCheckedString = "checked";
    }
    if ( myLayer.isBaseLayer )
    {
      myLegendItem = "<li class=\"ui-corner-all button ui-button ui-widget ui-button-text-only ui-state-default\"><input id=\"" + myLayerName +  "-radiobutton\" name=\"backdrop-layers\" type=\"radio\" value=\"" + myLayerName + "\" " + myCheckedString + "/><label forname=\"" + myLayerName + "-radiobutton\">" + myLayerName + "</label></li>";
      $("#base-layer-legend").append( myLegendItem );
    }
  }
  // update the current base layer when an item is clicked
  $(":radio").change(function()
  {
    myLayer = getLayerByName( this.value );
    mMap.setBaseLayer( myLayer );
  });
}
function setupCloudSlider() {
  $("#id_cloud_meanSlider").slider({
    //handle: '#id_cloud_meanSliderHandle',
    value:5,
    min: 0,
    max: 10,
    step: 1,
    start: function(e,ui){
      $('#id_cloud_meanSliderBubble').fadeIn('fast');
    },
    stop: function(e,ui){
      $('#id_cloud_meanSliderBubble').fadeOut('fast');
    },
    slide: function(e,ui){
      var myPosition = ($('#id_cloud_meanSlider').width() / 10) * ui.value;
      $("#id_cloud_meanSliderHandle").css('left', myPosition);
      $("#id_cloud_mean").val(ui.value);
      $("#id_cloud_meanSliderBubble").css('left',myPosition).text((ui.value * 10) + "%");
     }
    });
    $("#id_cloud_mean").val( $("#id_cloud_meanSlider").slider("value") );
    $("#id_cloud_meanSliderBubble").html( ($("#id_cloud_meanSlider").slider("value") * 10) + "%" );
    unblock();
}

function setupBaseMap()
{
  // The options hash, w/ zoom, resolution, and projection settings.
  var options = {
    projection : new OpenLayers.Projection("EPSG:900913"),
    displayProjection : new OpenLayers.Projection("EPSG:4326"),
    units : 'm',
    maxResolution: 156543.0339,
    maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,20037508.34, 20037508.34),
    numZoomLevels : 18,
    controls: [] //no controls by default we add them explicitly lower down
  };
  // The admin map for this geometry field.
  mMap = new OpenLayers.Map('map', options);
  // NOTE: Since we are putting the controls into a panel outside the map (in an external div),
  // we need to explicitly define the styles for the icons etc.
  mNavigationPanel = new OpenLayers.Control.Panel({'div' : document.getElementById("map-navigation-panel")});
  var myZoomInControl = new OpenLayers.Control.ZoomBox({
        title: "<b>Zoom in box</b> draw a box on the map, to see the area at a larger scale.",
        displayClass:'olControlZoomBoxIn', //so we can set its css
        out: false
      });
  mMap.addControl(myZoomInControl);
  var myZoomOutControl = new OpenLayers.Control.ZoomBox({
        title: "<b>Zoom out box</b> draw a box on the map, to see the area at a smaller scale.",
        displayClass:'olControlZoomBoxOut', //so we can set its css
        out: true
      });
  mMap.addControl(myZoomOutControl);
    var myNavigationControl = new OpenLayers.Control.Navigation({
	title : "<b>Pan map</b> click and drag map to move the map in the direction of the mouse."
    }
  );
  mMap.addControl(myNavigationControl);
    var myHistoryControl = new OpenLayers.Control.NavigationHistory({
	previousOptions: {
	    title : "<b>Previous view</b> quickly jump to the prevoius map view."
	},
	nextOptions: {
	    title : "<b>Next view</b> quickly jump to the next map view, works only with prevoius view."
	}
    });
  mMap.addControl(myHistoryControl);
  // now add these controls all to our toolbar / panel
  mNavigationPanel.addControls([myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.next, myHistoryControl.previous]);
  mMap.addControl(new OpenLayers.Control.ScaleBar({
      align: "left",
      minWidth: 150,
      maxWidth: 200,
      div: document.getElementById("map-scale")
    }));
  //show cursor location
  mMap.addControl(new OpenLayers.Control.MousePosition({'div': document.getElementById("map-location")}));
  mMap.addControl(mNavigationPanel);
}

/*
 * @param num : search_type enum value
*/
function advSearchActivate(search_type){
    if(typeof search_type == 'undefined') {
        search_type = 0;
    }
    $('.adv_search_ui .adv_fld').not('.adv_search_' + search_type).hide();
    // Check if #advancedSearch is visible
    if($('#advancedSearchDiv').is(':visible')){
        $('.adv_search_' + search_type).show('slow');
    } else {
        $('.adv_search_' + search_type).show();
        $('.adv_search_ui').show('slow');
    }
    $('#id_isAdvanced').val(true);
};

/*
 * @param theLayers and array of layers that should be added to the map
 */
function setupSearchMap( theLayers )
{

  //check if the slider exists first
  if ($("#id_cloud_mean").length > 0 )
  {
    setupCloudSlider();
  }
  mWKTFormat = new OpenLayers.Format.WKT();
  setupBaseMap();
  mVectorLayer = new OpenLayers.Layer.Vector("geometry");
  mMap.addLayer(mVectorLayer);
  // Add geometry specific panel of toolbar controls
  setupEditingPanel(mVectorLayer);
  mMap.addLayers( theLayers );
  addSelectControl();
  mMap.addControl(new OpenLayers.Control.LayerSwitcher());
  // Read WKT from the text field.
  var myWKT = document.getElementById('id_geometry').value;
  if (myWKT)
  {
    // After reading into geometry, immediately write back to
    // WKT <textarea> as EWKT (so that SRID is included).
    var mySearchGeometry = readWKT(myWKT);
    var myProjectedSearchGeometry = transformGeometry(mySearchGeometry);
    writeWKT(myProjectedSearchGeometry);
    mVectorLayer.addFeatures([new OpenLayers.Feature.Vector(myProjectedSearchGeometry)]);
    // Zooming to the bounds.
    mMap.zoomToExtent(myProjectedSearchGeometry.getBounds());
  } else {
    var bounds = new OpenLayers.Bounds(16.3477, -35.2411, 33.3984, -21.9727);
    bounds.transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
    mMap.zoomToExtent(bounds);
  }
  // This allows editing of the geographic fields -- the modified WKT is
  // written back to the content field (as EWKT, so that the ORM will know
  // to transform back to original SRID).
  mVectorLayer.events.on({"featuremodified" : modifyWKT});
  mVectorLayer.events.on({"featureadded" : addWKT});
  // Then add optional behavior controls

  if (myWKT){
    enableEditing();
  } else {
    enableDrawing();
  }
  createLegend();
}

/*
 * @param theLayers an array of layers that should be added to the map
 */
function setupTaskingMap( theLayers )
{
  mWKTFormat = new OpenLayers.Format.WKT();
  mVectorLayer = new OpenLayers.Layer.Vector("geometry");
  mMap.addLayer(mVectorLayer);
  // Add geometry specific panel of toolbar controls
  setupEditingPanel(mVectorLayer);
  // Here we use a predefined layer that will be kept up to date with URL changes
  layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Open Street Map");
  //theLayers.unshift(layerMapnik); // add to start of array
  theLayers.push(layerMapnik); // add to end of array
  mMap.addLayers( theLayers );
  addSelectControl();
  mMap.addControl(new OpenLayers.Control.LayerSwitcher());
  // Read WKT from the text field.
  var myWKT = document.getElementById('id_geometry').value;
  if (myWKT)
  {
    // After reading into geometry, immediately write back to
    // WKT <textarea> as EWKT (so that SRID is included).
    var mySearchGeometry = readWKT(myWKT);
    var myProjectedSearchGeometry = transformGeometry(mySearchGeometry);
    writeWKT(myProjectedSearchGeometry);
    mVectorLayer.addFeatures([new OpenLayers.Feature.Vector(myProjectedSearchGeometry)]);
    // Zooming to the bounds.
    mMap.zoomToExtent(myProjectedSearchGeometry.getBounds());
  } else {
    var bounds = new OpenLayers.Bounds(16.3477, -35.2411, 33.3984, -21.9727);
    bounds.transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
    mMap.zoomToExtent(bounds);
  }
  // This allows editing of the geographic fields -- the modified WKT is
  // written back to the content field (as EWKT, so that the ORM will know
  // to transform back to original SRID).
  mVectorLayer.events.on({"featuremodified" : modifyWKT});
  mVectorLayer.events.on({"featureadded" : addWKT});
  // Then add optional behavior controls

  if (myWKT){
    enableEditing();
  } else {
    enableDrawing();
  }
  createLegend();
}

/*--------------------------
 * Functions relating to clicking on scenes in the map to
 * highlight them.
 * -------------------------- */

function featureSelected( theEvent )
{
  $("#working").html(theEvent.feature.product_id);
  $("#working").slideDown('slow');
  hightlightRecord(theEvent.feature.id, false);
}

function setupSceneSelector( theLayer )
{
  var myHighlightControl = new OpenLayers.Control.SelectFeature( theLayer , {
    hover: false,
    highlightOnly: true,
    renderIntent: "temporary",
    eventListeners: {
      beforefeaturehighlighted: null,
      featurehighlighted: featureSelected,
      featureunhighlighted: null
    }
  });
  mMap.addControl(myHighlightControl);
  myHighlightControl.activate();
  theLayer.selectFeatureControl = myHighlightControl;
}


/*---------------------------------
 * General mapping functions
 * --------------------------------*/

// Function to clear vector features and purge wkt from div
function deleteFeatures()
{
  mVectorLayer.removeFeatures(mVectorLayer.features);
  mVectorLayer.destroyFeatures();
}
function clearFeatures()
{
  deleteFeatures();
  document.getElementById('id_geometry').value = '';
  mMap.setCenter(transformPoint(new OpenLayers.LonLat(0, 0)), 4);
}


function setupSearchFeatureInfo()
{
  /* Get feature info for wms queries  */
  var info = new OpenLayers.Control.WMSGetFeatureInfo(
  {
    url: 'http://196.35.94.243/cgi-bin/mapserv?map=SEARCHES',
    title: 'Identify features by clicking',
    queryVisible: true,
    vendorParams:
    {
      FEATURE_COUNT : "1000",
      INFO_FORMAT : 'text/html'
    },
    eventListeners:
    {
      getfeatureinfo: function(event)
      {
        if((event.text).length > 1)
        {
          mMap.addPopup(new OpenLayers.Popup.FramedCloud(
            "chicken",
            mMap.getLonLatFromPixel(event.xy),
            null,
            event.text,
            null,
            true
            ));
        }
        else
        {
          mMap.addPopup(new OpenLayers.Popup.FramedCloud(
            "chicken",
            mMap.getLonLatFromPixel(event.xy),
            null,
            "No result *sniff*",
            null,
            true
            ));
        }
      }
    }
  });
  mMap.addControl(info);
  info.activate();
}

function setupSqlDialog()
{
  //JQuery popup dialog for admins to see underlying search query
  $('#sql-button').live('click', function (event) {
    $('#sql').dialog({
      modal: true,
      show: 'slide',
      width: 600,
      hide: 'slide',
      autoOpen: true,
      zIndex: 9999,
      title: 'Underlying Query:',
      buttons: { "Close" : function() { $(this).dialog('close'); } }
    });
  });
}

function setupSceneIdHelpDialog()
{
  var mySceneIdHelpDialog = $('<div></div>').load("/sceneidhelp/").dialog({
    autoOpen: false,
    title: 'Scene Id Help',
    modal: true,
    show: 'slide',
    hide: 'slide',
    zIndex: 9999,
    height: $(window).height() / 2,
    width: $(window).width() / 2,
    buttons: { "Close" : function() { $(this).dialog('close'); } }
  });

  $('#scene-id-help').live('click', (function () {
    mySceneIdHelpDialog.dialog('open');
    return false;
  }));
}

function setupMapHelpDialog()
{
  var myMapHelpDialog = $('<div></div>').load("/mapHelp/").dialog({
    autoOpen: false,
    title: 'Map Help',
    modal: true,
    show: 'slide',
    hide: 'slide',
    zIndex: 9999,
    height: $(window).height() / 2,
    width: $(window).width() / 2,
    buttons: { "Close" : function() { $(this).dialog('close'); } }
  });

  $('#map-help-button').live('click', (function () {
    myMapHelpDialog.dialog('open');
    return false;
  }));
}

/* Show a pop up dialog with metadata.
 * @see setupMetadataDialog
 * @note also used from withing image preview panel */
function showMetadata( theRecordId )
{
    var myMetadataDialog = $('<div></div>').load("/metadata/" + theRecordId + "/").dialog({
      autoOpen: true,
      title: 'Metadata',
      modal: true,
      show: 'slide',
      hide: 'slide',
      zIndex: 9999,
      height: $(window).height() / 2,
      width: $(window).width() / 2,
      buttons: { "Close" : function() { $(this).dialog('close'); } }
    });
}

function setupMetadataDialog( )
{

  $('.metadata-icon').live('click', (function () {
    var myRecordId = $(this).attr('longdesc');
    showMetadata( myRecordId );
  }));
}


/* Mark all scenes as selected no and
 * give them all an equal zIndex.
 * see http://openlayers.org/dev/examples/ordering.html */
function resetSceneZIndices( )
{
  myLayer = getLayerByName("scenes");
  if (myLayer !== false)
  {
    var myFeatures = myLayer.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      myFeatures[i].attributes.zIndex=0;
      myFeatures[i].selected = "no";
    }
  }
  return -1; //not found
}

function getFeatureIndexByRecordId( theRecordId )
{
  myLayer = getLayerByName("scenes");
  if (myLayer !== false)
  {
    var myFeatures = myLayer.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      if(myFeatures[i].id == theRecordId)
      {
        return i;
      }
    }
  }
  return -1; //not found
}

/* Highlight a record on the map and load its preview in
 * the preview panel
 * @param theRecordId - id of the record to hightlight (not the product_id)
 * @param theZoomFlag - whether to zoom to the record on the map
 * */
function hightlightRecord( theRecordId, theZoomFlag )
{
  // use ajax to load the thumb preview and then call the prepareFancy callback
  $("#preview-accordion-div").load("/showpreview/" + theRecordId + "/medium/","",prepareFancy);
  resetSceneZIndices();
  var myLayer = getLayerByName("scenes");
  var myIndex = getFeatureIndexByRecordId( theRecordId );
  myLayer.features[myIndex].attributes.zIndex=1;
  myLayer.features[myIndex].selected = "yes";
  if (theZoomFlag)
  {
    mMap.zoomToExtent(myLayer.features[myIndex].geometry.bounds);
  }
  myLayer.redraw();
}

/* Setup a callback so that when a mini preview icon is
 * clicked, the corresponding scene is highlighted on teh map
 * and loaded in the preview accordion panel. */
function setupMiniIconClickCallback()
{
  $('.mini-icon').live('click', (function () {
    //$(this).css("border", "1px").css("border-color","red");
    var myRecordId = $(this).attr('longdesc');
    hightlightRecord(myRecordId, true);
  }));
}


function addOrderClicked()
{
  var myRowCount = $("#cart-contents-table tr").length;
  if ( myRowCount < 2 ) // The header row will always be there...
  {
    var myOptions =
    {
      modal: true,
      show: "blind",
      hide: "explode",
      zIndex: 99999,
      buttons:
      {
        Ok: function() {
          $(this).dialog("close");
        }
      }
    };
    $("#cart-empty-dialog").dialog( myOptions );
  }
  else
  {
    window.location.replace("/addorder/");
  }
  return false;
}

/* Transform an openlayers bounds object such that
 * it matches the CRS of the map
 * @param a bounds object (assumed to be in EPSG:4326)
 * @return a new bounds object projected into the map CRS
 */
function transformBounds(theBounds)
{
  myBounds = theBounds.clone();
  var myCRS = new OpenLayers.Projection("EPSG:4326");
  var toCRS = mMap.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
  myBounds.transform(myCRS, toCRS);
  return myBounds;
}
/* transform an openlayers geometry object such that
 * it matches the CRS of the map
 * @param a geometry object (assumed to be in EPSG:4326 CRS)
 * @return a new geometry object projected into the map CRS
 */
function transformGeometry(theGeometry)
{
  myGeometry = theGeometry.clone();
  var myCRS = new OpenLayers.Projection("EPSG:4326");
  var toCRS = mMap.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
  myGeometry.transform(myCRS,toCRS);
  return myGeometry;
}
/* Reverse transform an openlayers geometry object such that
 * it matches the CRS 4326
 * @param a geometry object (assumed to be in map CRS)
 * @return a new geometry object projected into the EPSG:4326 CRS
 */
function reverseTransformGeometry(theGeometry)
{
  myGeometry = theGeometry.clone();
  var myCRS = new OpenLayers.Projection("EPSG:4326");
  myGeometry.transform(mMap.getProjectionObject(),myCRS);
  return myGeometry;
}

/* Transform an openlayers point object such that
 * it matches the CRS of the map
 * @param a point object (assumed to be in EPSG:4326)
 * @return a new point object projected into the map CRS
 */
function transformPoint(thePoint)
{
  var myCRS = new OpenLayers.Projection("EPSG:4326");
  var myDestCRS = new OpenLayers.Projection("EPSG:900913");
  myPoint = thePoint.clone();
  myPoint = myPoint.transform(myCRS, myDestCRS);
  return myPoint;
}
/* Transform an openlayers point object such that
 * it matches the 4326 CRS
 * @param a point object (assumed to be in EPSG:900913)
 * @return a new point object projected into the 4326 CRS
 */
function reverseTransformPoint(thePoint)
{
  var myCRS = new OpenLayers.Projection("EPSG:4326");
  var mySourceCRS = new OpenLayers.Projection("EPSG:900913");
  myPoint = thePoint.clone();
  myPoint = myPoint.transform(mySourceCRS, myCRS);
  return myPoint;
}

