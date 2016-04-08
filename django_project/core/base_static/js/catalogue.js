// ==ClosureCompiler==
// @compilation_level SIMPLE_OPTIMIZATIONS
// @output_file_name catalogue.js
// ==/ClosureCompiler==

/* Compress this file to catalogue.js using google's closure compiler at
  http://closure-compiler.appspot.com/home */


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

/* ------------------------------------------------------
 *  Global variables
 *  ------------------------------------------------------ */

/* Setup the style for our scene footprints layer and enable
 * zIndexing so that we can raise the selected on above the others
 * see http://openlayers.org/dev/examples/ordering.html */

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
var mLastSelectedRecordId = null;

/*--------------------------------------------------------
 * Things to run on any page first load that uses this lib
 -------------------------------------------------------- */
$(document).ready(function()
{
  //block the user interface when an ajax request is sent
  //$(".blocking-link").live('click',block);
  //check for messages every 60 s
  setInterval(checkForMessages, 60000);
  $(".btn-group").click(function() {
    item = $(this).parent().parent().parent();
    item.animate({scrollTop: item[0].scrollHeight});
  });''
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
  $.blockUI({ message: '<h2><img src="/static/images/ajax-loader.gif" /> Loading...</h2>',
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
function removeWKT(event) {
  document.getElementById('id_geometry').value = '';
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
//helper: enable map Navigation
function enableNavigation()
{
  mMap.getControlsByClass('OpenLayers.Control.Navigation')[0].activate();
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
        'displayClass': 'btn btn-info btn-large right icon-check-empty olControlDrawFeaturePolygon',
        'title': 'Capture polygon: left click to add points, double click to finish capturing',
        'button': OpenLayers.Util.getElement('map-navigation')
      });
  var myModifyFeatureControl = new OpenLayers.Control.ModifyFeature(theLayer, {
      'displayClass': 'right icon-edit icon-2x olControlModifyFeature',
      'title': 'Modify polygon: left click to move/add points, hover and press <i>delete</i> to delete points'
  });
  var myDestroyFeaturesControl = new DestroyFeatures({
      'displayClass': 'right icon-remove icon-2x destroyFeature',
      'title':'Delete polygon: deletes polygon',
      'layer': theLayer
      }
    );
  //mMapControls = [myDrawingControl, myModifyFeatureControl, myDestroyFeaturesControl];
  mNavigationPanel.addControls([myDrawingControl, myModifyFeatureControl, myDestroyFeaturesControl]);
  //dirty hack to hide icons on map
  $(".olControlNoSelect").hide();
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
  //$("#accordion").accordion({ autoHeight: false });
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
  //$("#collapseOne").collapse('hide');
  //$("#collapseThree").collapse('hide');
  $("#collapseTwo").collapse('show');
  $("#collapseTwo").collapse({parent:'#accordion', toggle:true});
  //$("#accordion").accordion("activate", 1);
  /*
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
*/
}

function showMiniCart(request)
{
  /*
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
  */
  // refresh the cart table
  $("#cart_tab").load("/showminicartcontents/");

  /*
  if ( myShowAccordionFlag )
  {
    $("#accordion").accordion("activate", 2);
  }
  */
  $.pnotify({
    title: 'Success',
    text: 'Item ' + request.Item + ' successfully added to your cart!',
    type: 'success'
  });
  unblock();
}

function showErrorAddToCart(request) {
  $.pnotify({
    title: 'Error',
    text: request.responseText,
    type: 'error'
  });
  unblock();
}

function addToCart( theId )
{
  // Show a wait image before we hit our ajax call
  block();
  //$.get("/addtocart/" + theId + "/?xhr");
  $.ajax({
    url: "/addtocart/" + theId + "/?xhr",
    dataType: "json",
    success: showMiniCart,
    error: showErrorAddToCart
  });
  //showMiniCart();
  $('#myTab a[href="#cart_tab"]').tab('show');
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
  return false;
}
function removeFromCart(theId, theObject)
{
  //check if this product has delivery details form
  var myOrderForm_refs = $('#add_form #id_ref_id');
    if (myOrderForm_refs.length >0){
  var current_refs=myOrderForm_refs.val();
  //check if current_refs are empty, and convert to array
  if (current_refs.length){
      current_refs=current_refs.split(',');
  } else {
      current_refs=[];
  }
  //get removed ref_id
  var ref_id=theObject.parent().parent().find('a.show_form').attr('ref_id')
  var index = current_refs.indexOf(ref_id);
  if (index>-1){
      current_refs.splice(index,1);
      myOrderForm_refs.val(current_refs.join(','));
  }
    }
  $.get("/removefromcart/" + theId + "/?xhr","",layerRemoved);
  theObject.parent().parent().remove();
  //-1 for the header row
  var myRowCount = $("#cart-contents-table tr").length - 1;
  $("#cart_title").html( 'Cart (' + myRowCount + ')');
  $("#cart-item-count").html( myRowCount );
  if ((myRowCount < 1) && ($("#id_processing_level").length != 0))
  {
    //second clause above to prevent this action when minicart is being interacted with
    window.location.replace("/emptyCartHelp/");
  }
  unblock();
  return false;
}
function removeFromMiniCart(theId, theObject)
{
  //theObject is the remove icon - we use it to find its parent row and remove that
  block();
  removeFromCart( theId, theObject );
}
function showCart()
{
  $("#cart").load("/showcartcontents/","", zebraTables);
  unblock();
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
  unblock();
}

function loadSearchResults( theNumber, theSearchGuid )
{
  block();
  $('#search-results').show();
  $("#search-results-container").load("/rendersearchresultspage/" + theSearchGuid + "/?page=" + theNumber,"",unblock);
}

function loadPage( theNumber, theSearchGuid )
{
  block();
  // Show a wait image before we hit our ajax call
  $("#page").load("/searchpage/" + theSearchGuid + "/?page=" + theNumber,"",revealTable);
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
  $( "#results" ).height( myTableHeight );
}

// Get feature info implementation for openlayer
// see http://trac.openlayers.org/wiki/GetFeatureInfo
function showFeatureInfo(event)
{
  block();
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
  unblock();
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

/*
Create a custom map control to show map help dialog
*/
// this is a global variable which is intialized by setupMapHelpDialog()
var myMapHelpDialog = null;
var map_help_button = new OpenLayers.Control.Button({
        displayClass: 'right icon-question-sign icon-2x olControlMapHelp',
        trigger: function () {
          //show maphelp dialog
          $('#modalContainer').load("/mapHelp/");
          $('#myModal').modal('show');
      }
    });

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
  mNavigationPanel = new OpenLayers.Control.Panel({div : OpenLayers.Util.getElement('map-navigation-panel')});
  mMap.addControl(mNavigationPanel);
  var myZoomInControl = new OpenLayers.Control.ZoomBox({
        title: "Zoom In Box: draw a box on the map, to see the area at a larger scale.",
        displayClass:'right icon-zoom-in icon-2x olControlZoomBoxIn',
        div : OpenLayers.Util.getElement('map-navigation-panel'),
        out: false
      });
  //mMap.addControl(myZoomInControl);

  var myZoomOutControl = new OpenLayers.Control.ZoomBox({
        title: "Zoom Out Box: draw a box on the map, to see the area at a smaller scale.",
        displayClass:'right icon-zoom-out icon-2x olControlZoomBoxOut',
        out: true
      });
  //mMap.addControl(myZoomOutControl);

    var myNavigationControl = new OpenLayers.Control.Navigation({
    title : "Pan map: click and drag map to move the map in the direction of the mouse.",
    zoomWheelEnabled: false,
    displayClass:'right icon-move icon-2x olControlNavigation',
    }
  );
  //mMap.addControl(myNavigationControl);

    var myHistoryControl = new OpenLayers.Control.NavigationHistory({
  nextOptions: {
      title : "Next view: quickly jump to the next map view, works only with previous view.",
      displayClass:'right icon-chevron-right icon-2x olControlNavigationHistoryNext',
    },
  previousOptions: {
      title : "Previous view: quickly jump to the previous map view.",
      displayClass:'right icon-chevron-left icon-2x olControlNavigationHistoryPrevious',
    }
  });
  //mMap.addControl(myHistoryControl);
  // add map help button
  //mMap.addControl(myZoomInControl);
  // now add these controls all to our toolbar / panel
  mNavigationPanel.addControls([map_help_button, myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.previous, myHistoryControl.next]);
  //mNavigationPanel.addControls([map_help_button]);
  mMap.addControl(new OpenLayers.Control.ScaleBar({
      align: "left",
      minWidth: 150,
      maxWidth: 200,
      div: document.getElementById("map-scale")
    }));

  //show cursor location
  mMap.addControl(new OpenLayers.Control.MousePosition({'div': document.getElementById("map-location")}));
  mMap.addControl(new OpenLayers.Control.LayerSwitcher());
}

/*
 * @param theLayers and array of layers that should be added to the map
 */
function setupSearchMap( theLayers )
{

  mWKTFormat = new OpenLayers.Format.WKT();
  setupBaseMap();
  mVectorLayer = new OpenLayers.Layer.Vector("search_geometry");
  setupEditingPanel(mVectorLayer);
  mMap.addLayer(mVectorLayer);
  // Add geometry specific panel of toolbar controls
  mMap.addLayers( theLayers );
  addSelectControl();
  // Read WKT from the text field.

  //var myWKT = document.getElementById('id_geometry').value;
  var myWKT = $('#id_geometry').val();
  //var myWKT = false;
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
  mVectorLayer.events.on({"featureremoved": removeWKT});
  // Then add optional behavior controls

  /*
  // disable editing or drawing by default on searchMap
  if (myWKT){
    enableEditing();
  } else {
    enableDrawing();
  }*/

  //activate Navigation/DragPan by default for searchMap
  enableNavigation();

}

/*
 * @param theLayers an array of layers that should be added to the map
 */
function setupTaskingMap( theLayers )
{
  mWKTFormat = new OpenLayers.Format.WKT();
  mVectorLayer = new OpenLayers.Layer.Vector("task_geometry");
  mMap.addLayer(mVectorLayer);
  // Add geometry specific panel of toolbar controls
  setupEditingPanel(mVectorLayer);
  // Here we use a predefined layer that will be kept up to date with URL changes
  layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Open Street Map");
  //theLayers.unshift(layerMapnik); // add to start of array
  theLayers.push(layerMapnik); // add to end of array
  mMap.addLayers( theLayers );
  addSelectControl();
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
  mVectorLayer.events.on({"featureremoved": removeWKT});
  // Then add optional behavior controls

  if (myWKT){
    enableEditing();
  } else {
    enableDrawing();
  }
}

/*--------------------------
 * Functions relating to clicking on scenes in the map to
 * highlight them.
 * -------------------------- */

function featureSelected( theEvent )
{
  block();
  $(".mapquery").html(theEvent.feature.product_id);
  hightlightRecord(theEvent.feature.id, false);
  unblock();
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

  $('#scene-id-help').click (function () {
    mySceneIdHelpDialog.dialog('open');
    return false;
  });
}

function setupMapHelpDialog()
{
  myMapHelpDialog = $('<div></div>').load("/mapHelp/").dialog({
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
}

/* Show a pop up dialog with metadata.
 * @see setupMetadataDialog
 * @note also used from withing image preview panel */
function showMetadata( theRecordId )
{
    //console.log('FIX ME!');
    $('#modalContainer').load("/metadata/" + theRecordId + "/");
    $('#myModal').modal('show');
}

function setupMetadataDialog( )
{
  $('#main-content').on('click','.metadata-icon', function () {
    var myRecordId = $(this).attr('longdesc');
    showMetadata(myRecordId);
  });
}

function setupPreviewDialogCart( )
{
  $('#main-content').on('click','.mini-icon', function () {
    var myRecordId = $(this).attr('longdesc');
    $('#modalContainer').load("/thumbnailpage/" + myRecordId + "/");
    $('#myModal').modal('show');
  });
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
  //unset the last selected rec table row to not be bold
  //then set the new selection to bold...
  if ( mLastSelectedRecordId )
  {
    $("#record-"+ mLastSelectedRecordId + " td" ).css("font-weight", "normal");
  }
  mLastSelectedRecordId = theRecordId;
  $("#record-"+ theRecordId + " td" ).css("font-weight", "bold");
  // use ajax to load the thumb preview and then call the prepareFancy callback
  //$("#preview-accordion-div").load("/showpreview/" + theRecordId + "/medium/","",prepareFancy);
  $("#preview_tab").load("/showpreview/" + theRecordId + "/medium/");
  $('#modalContainer').load("/thumbnailpage/" + theRecordId + "/");
  $('#myTab a[href="#preview_tab"]').tab('show');
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
  $('#main-content').on('click', '.mini-icon', function () {
    //$(this).css("border", "1px").css("border-color","red");
    var myRecordId = $(this).attr('longdesc');
    hightlightRecord(myRecordId, true);
  });
}

/* Setup a callback so that when a search result table row is
 * clicked, the corresponding scene is highlighted on the map
 * and loaded in the preview accordion panel. */
function setupRowClickCallback()
{
  $('#search-results-container').delegate('.result-row', 'click', (function () {
    var myRecordId = $(this).attr('id').replace("record-","");
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

/** Load some content into the #content div.
 * Uses ajax to load it and blocks the ui while loading
 */
function loadContent( theUrl )
{
  block();
  $("#content").load( theUrl ,"",unblock);
}

function loadSummaryTable(theId)
{
  block();
  $("#content").load("/sensorSummaryTable/" + theId + "/","",unblock);
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

/** This function will pop up a form to let admins send messages to users.
 * @param theAllFlag - whether the message should go to all users
 * (c) Linfiniti
 **/
function sendMessage( theAllFlag )
{
  var myMessageDialog = $('#message-dialog').dialog({
    autoOpen: true,
    title: 'Send Message',
    closeOnEscape: true,
    dialogClass: 'scrollable',
    position: 'center',
    width: 480,
    modal: true,
    buttons:
    [
      {
        text: "Send",
        click : function( ) { postMessage ( theAllFlag ); }
      },
      {
        text: "Close",
        click : function() {
          $(this).dialog("close");
        }
      }
    ],
    open: function() {
      if ( theAllFlag )
      {
        $("#message-dialog").load("/sendMessageToAllUsers/", function() {
          $('#message-dialog').dialog('option', 'position', 'center');
        });
      }
      else
      {
        $("#message-dialog").load("/sendMessageToUser/", function() {
          $('#message-dialog').dialog('option', 'position', 'center');
        });
      }

    }
  });
}

/** Posts edited message to server for dissemination.
 * (c) Linfiniti
 **/
function postMessage( theAllFlag )
{
  var myUrl = "/sendMessageToUser/";
  if ( theAllFlag )
  {
    myUrl = "/sendMessageToAllUsers/";
  }
  $.post( myUrl, $("#message-form" ).serialize(), function(data) {
    $("#message-dialog").empty();
    $("#message-dialog").append(data);
  });
}

/** Check for messages on the server and display any returned messages
 * in a popup.
 * (c) Linfiniti
 */
function checkForMessages()
{
  $.get("/getUserMessages/" , function(data) {
    if ( data !== "\n" && data.length !== 0)
    {
      $.each(data, function(key, val) {
        console.log(val);
        $.pnotify({
          title: 'New message',
          text: val.message,
          type: 'info',
          hide: false
        });
      });
    }
  });
}

function displaySearchFormErrors() {
  var errors = '';
  $("[id^='error']").each(function() {
    //console.log($(this).parent().parent().parent().parent());
    //errors = errors + '<p onclick="$(\'#' +$(this).attr('id')+'\').parent().parent().parent().parent().collapse(\'show\');">' + $(this).text() + '</p>';
    errors = errors + '<a data-toggle="collapse" data-parent="#accordion-search2" href="#' + $(this).parent().parent().parent().parent().attr('id') + '" ><i class="icon-edit"></i> ' + $(this).text() + '</a><br />';
  });
  if (errors != '') {
    $.pnotify({
      title: 'Error on search form',
      text: errors,
      type: 'error',
    });
  }
}

