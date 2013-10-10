+function ($) {

  var OLMap = function (element, options) {
    this.$element = $(element);
    this.options = $.extend({}, OLMap.DEFAULTS, options);

    var self=this;

    this.initMap();
    // function calls
  };

  OLMap.DEFAULTS = {

  };

  OLMap.prototype.initMap = function() {

    var options = {
      projection : new OpenLayers.Projection("EPSG:900913"),
      displayProjection : new OpenLayers.Projection("EPSG:4326"),
      units : 'm',
      maxResolution: 156543.0339,
      maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,20037508.34, 20037508.34),
      numZoomLevels : 18,
      controls: [] //no controls by default we add them explicitly lower down
    };

    this.map = new OpenLayers.Map('map', options);
    var layerMapnik = new OpenLayers.Layer.OSM("Open Street Map");
    var layerSearch = new OpenLayers.Layer.Vector("Search geometry");
    var geoSearch = new OpenLayers.Layer.Vector("Polygon select");
    var myLayersList = [
          WEB_LAYERS.zaSpot2mMosaic2010TC,
          WEB_LAYERS.zaSpot2mMosaic2009TC,
          WEB_LAYERS.zaSpot2mMosaic2008TC,
          WEB_LAYERS.zaSpot2mMosaic2007TC,
          WEB_LAYERS.zaSpot10mMosaic2010,
          WEB_LAYERS.zaSpot10mMosaic2009,
          WEB_LAYERS.zaSpot10mMosaic2008,
          WEB_LAYERS.zaSpot10mMosaic2007,
          WEB_LAYERS.zaRoadsBoundaries,
          layerMapnik,
          layerSearch
      ];
      this.map.addLayers(myLayersList);
      this.map.zoomToExtent(this.transformBounds(new OpenLayers.Bounds(14.0,-35.0,34.0,-21.0)));

      var myHighlightControl = new OpenLayers.Control.SelectFeature( layerSearch , {
          hover: false,
          highlightOnly: true,
          renderIntent: "temporary",
          eventListeners: {
              beforefeaturehighlighted: null,
              featurehighlighted: featureSelected,
              featureunhighlighted: null
          }
      });
      this.map.addControl(myHighlightControl);
      myHighlightControl.activate();
      layerSearch.selectFeatureControl = myHighlightControl;
      this.map.addLayer(geoSearch);
      geoSearch.events.on({"featuremodified" : modifyWKT});
      geoSearch.events.on({"featureadded" : addWKT});
      geoSearch.events.on({"featureremoved": removeWKT});
      mNavigationPanel = new OpenLayers.Control.Panel({div : OpenLayers.Util.getElement('map-navigation')});
      this.map.addControl(mNavigationPanel);
      var myZoomInControl = new OpenLayers.Control.ZoomBox({
          title: "Zoom In Box: draw a box on the map, to see the area at a larger scale.",
          displayClass:'right icon-zoom-in icon-2x icon-border olControlZoomBoxIn',
          div : OpenLayers.Util.getElement('map-navigation'),
          out: false
        });
    //mMap.addControl(myZoomInControl);

    var myZoomOutControl = new OpenLayers.Control.ZoomBox({
          title: "Zoom Out Box: draw a box on the map, to see the area at a smaller scale.",
          displayClass:'right icon-zoom-out icon-2x icon-border olControlZoomBoxOut',
          div : OpenLayers.Util.getElement('map-navigation'),
          out: true
        });
    //mMap.addControl(myZoomOutControl);

      var myNavigationControl = new OpenLayers.Control.Navigation({
      title : "Pan map: click and drag map to move the map in the direction of the mouse.",
      zoomWheelEnabled: false,
      displayClass:'right icon-move icon-2x icon-border olControlNavigation',
      div : OpenLayers.Util.getElement('map-navigation'),
      }
    );
    //mMap.addControl(myNavigationControl);

      var myHistoryControl = new OpenLayers.Control.NavigationHistory({
    nextOptions: {
        title : "Next view: quickly jump to the next map view, works only with prevoius view.",
        displayClass:'right icon-chevron-right icon-2x icon-border olControlNavigationHistoryNext',
        div : OpenLayers.Util.getElement('map-navigation'),
      },
    previousOptions: {
        title : "Previous view: quickly jump to the prevoius map view.",
        displayClass:'right icon-chevron-left icon-2x icon-border olControlNavigationHistoryPrevious',
        div : OpenLayers.Util.getElement('map-navigation'),
      }
    });
    mNavigationPanel.addControls([myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.previous, myHistoryControl.next]);

    var myDrawingControl = new OpenLayers.Control.DrawFeature(geoSearch,
        OpenLayers.Handler.Polygon, {
      'displayClass': 'right icon-check-empty icon-2x icon-border olControlDrawFeaturePolygon',
      'title': 'Capture polygon: left click to add points, double click to finish capturing',
        div : OpenLayers.Util.getElement('map-navigation'),
        });
    var myModifyFeatureControl = new OpenLayers.Control.ModifyFeature(geoSearch, {
        'displayClass': 'right icon-edit icon-2x icon-border olControlModifyFeature',
        'title': 'Modify polygon: left click to move/add points, hover and press <i>delete</i> to delete points',
        div : OpenLayers.Util.getElement('map-navigation'),
    });
    var myDestroyFeaturesControl = new DestroyFeatures({
        'displayClass': 'right icon-remove icon-2x icon-border destroyFeature',
        'title':'Delete polygon: deletes polygon',
        'layer': geoSearch,
        div : OpenLayers.Util.getElement('map-navigation'),
        }
      );
    mNavigationPanel.addControls([myDrawingControl, myModifyFeatureControl, myDestroyFeaturesControl]);

    this.populateLayerSwitcher();

    this.map.addControl(new OpenLayers.Control.MousePosition({'div': document.getElementById("map-control-position")}));
    this.map.addControl(new OpenLayers.Control.ScaleBar({
        align: "left",
        minWidth: 150,
        maxWidth: 200,
        div: document.getElementById("map-control-scalebar")
      }));
  };

  OLMap.prototype.transformBounds = function (theBounds)
  {
    var myBounds = theBounds.clone();
    var myCRS = new OpenLayers.Projection("EPSG:4326");
    var toCRS = this.map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
    myBounds.transform(myCRS, toCRS);
    return myBounds;
  };

  OLMap.prototype.transformGeometry = function(theGeometry)
  {
    var myGeometry = theGeometry.clone();
    var myCRS = new OpenLayers.Projection("EPSG:4326");
    var toCRS = this.map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
    myGeometry.transform(myCRS,toCRS);
    return myGeometry;
  };

  OLMap.prototype.reverseTransformGeometry = function(theGeometry)
  {
    var myGeometry = theGeometry.clone();
    var myCRS = new OpenLayers.Projection("EPSG:4326");
    myGeometry.transform(this.map.getProjectionObject(),myCRS);
    return myGeometry;
  };

  OLMap.prototype.switchBaseLayer = function (name, el) {
    this.map.setBaseLayer(this.map.getLayersByName(name)[0]);
    $('#map-layerswitcher .visible').removeClass('visible');
    $(el).addClass('visible');
  };

  OLMap.prototype.switchVectorLayer = function(name, el) {
    var layer = this.map.getLayersByName(name)[0];
    if (layer.visibility) {
        layer.setVisibility(false);
        $(el).removeClass('visible_layer');
    } else {
        layer.setVisibility(true);
        $(el).addClass('visible_layer');
    }
  };

  OLMap.prototype.populateLayerSwitcher = function() {
    var div = $('#map-layerswitcher');
    var layerHTML;
    var visible;
    var js_layer_switch;
    _.each(this.map.layers, function(val) {
      if (val.visibility && val.isBaseLayer) {
          visible = 'visible';
      } else if (val.visibility)
          visible = 'visible_layer';
      else {
          visible = '';
      }

      if (val.isBaseLayer) {
          js_layer_switch = ' onclick="switchBaseLayer(\''+val.name+'\', this);" ';
      } else {
          js_layer_switch = ' onclick="switchVectorLayer(\''+val.name+'\', this);" ';
      }
      layerHTML = '<div class="layer-control '+ visible +'" '+js_layer_switch+'><img src="/static/images/'+WEB_LAYERS_IMAGE[val.name]+'" /><p>'+val.name+'</p></div>';
      div.append(layerHTML);
    });
  };

  $.fn.sansaMap = function (option) {
    return this.each(function () {
      var $this = $(this);

      var options = typeof option == 'object' && option;
      this.widget = new OLMap(this, options);

    });
  };

  $.fn.sansaMap.Constructor = OLMap;

}(window.jQuery);