+function () {

  "use strict"; // jshint ;_;

  APP.SansaMap = function (map_id) {
      this.map_element = map_id;
      this._initialize();

      // return the object
      return this;
  };

  APP.SansaMap.prototype = {
    default_options: {
      projection : new OpenLayers.Projection("EPSG:900913"),
      displayProjection : new OpenLayers.Projection("EPSG:4326"),
      units : 'm',
      maxResolution: 156543.0339,
      maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,20037508.34, 20037508.34),
      numZoomLevels : 18,
      controls: []
    },

    initLayers: function() {
      var layerMapnik = new OpenLayers.Layer.OSM("Open Street Map");

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
            layerMapnik
        ];
        this.map.addLayers(myLayersList);
    },

    _initialize: function() {
      var self = this;

      this.map = new OpenLayers.Map(this.map_element, this.default_options);

      this.initLayers();

    // special vector layers

    this.geoSearch = new OpenLayers.Layer.Vector("Polygon select", {'displayInLayerSwitcher': false});

    this.map.zoomToExtent(this.transformBounds(new OpenLayers.Bounds(14.0,-35.0,34.0,-21.0)));

    this.map.addLayer(this.geoSearch);
    this.geoSearch.events.on({"featuremodified" : modifyWKT});
    this.geoSearch.events.on({"featureadded" : addWKT});
    this.geoSearch.events.on({"featureremoved": removeWKT});

    var mNavigationPanel = new OpenLayers.Control.Panel({div : OpenLayers.Util.getElement('map-navigation')});
    this.map.addControl(mNavigationPanel);

    var myZoomInControl = new OpenLayers.Control.ZoomBox({
      title: "Zoom In Box: draw a box on the map, to see the area at a larger scale.",
      displayClass:'right icon-zoom-in icon-2x icon-border olControlZoomBoxIn',
      div : OpenLayers.Util.getElement('map-navigation'),
      out: false
    });

    var myZoomOutControl = new OpenLayers.Control.ZoomBox({
          title: "Zoom Out Box: draw a box on the map, to see the area at a smaller scale.",
          displayClass:'right icon-zoom-out icon-2x icon-border olControlZoomBoxOut',
          div : OpenLayers.Util.getElement('map-navigation'),
          out: true
        });

    var myNavigationControl = new OpenLayers.Control.Navigation({
      title : "Pan map: click and drag map to move the map in the direction of the mouse.",
      zoomWheelEnabled: false,
      displayClass:'right icon-move icon-2x icon-border olControlNavigation',
      div : OpenLayers.Util.getElement('map-navigation'),
    });

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

    mNavigationPanel.addControls(
      [myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.previous, myHistoryControl.next]
    );

    var myDrawingControl = new OpenLayers.Control.DrawFeature(this.geoSearch, OpenLayers.Handler.Polygon, {
      'displayClass': 'right icon-check-empty icon-2x icon-border olControlDrawFeaturePolygon',
      'title': 'Capture polygon: left click to add points, double click to finish capturing',
      div : OpenLayers.Util.getElement('map-navigation'),
    });

    var myModifyFeatureControl = new OpenLayers.Control.ModifyFeature(this.geoSearch, {
      'displayClass': 'right icon-edit icon-2x icon-border olControlModifyFeature',
      'title': 'Modify polygon: left click to move/add points, hover and press <i>delete</i> to delete points',
      div : OpenLayers.Util.getElement('map-navigation'),
    });

    var myDestroyFeaturesControl = new DestroyFeatures({
      'displayClass': 'right icon-remove icon-2x icon-border destroyFeature',
      'title':'Delete polygon: deletes polygon',
      'layer': this.geoSearch,
      div : OpenLayers.Util.getElement('map-navigation'),
    });

    mNavigationPanel.addControls([myDrawingControl, myModifyFeatureControl, myDestroyFeaturesControl]);

    this.refreshLayerSwitcher();

    this.map.addControl(new OpenLayers.Control.MousePosition({'div': document.getElementById("map-control-position")}));
    this.map.addControl(new OpenLayers.Control.ScaleBar({
        align: "left",
        minWidth: 150,
        maxWidth: 200,
        div: document.getElementById("map-control-scalebar")
      }));

    $('#map-layerswitcher').on('click', '.layer-control', function(evt,data){
      var myLayer = $(evt.currentTarget).text();
      self.switchLayer(myLayer,$(evt.currentTarget));
    });
  },

  add_layer: function (theLayer) {
    this.map.addLayers([theLayer]);
    // refresh the layer switcher layers
    this.refreshLayerSwitcher();
  },

  transformBounds: function (theBounds)
  {
    var myBounds = theBounds.clone();
    var myCRS = new OpenLayers.Projection("EPSG:4326");
    var toCRS = this.map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
    myBounds.transform(myCRS, toCRS);
    return myBounds;
  },

  transformGeometry: function(theGeometry)
  {
    var myGeometry = theGeometry.clone();
    var myCRS = new OpenLayers.Projection("EPSG:4326");
    var toCRS = this.map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
    myGeometry.transform(myCRS,toCRS);
    return myGeometry;
  },

  reverseTransformGeometry: function(theGeometry)
  {
    var myGeometry = theGeometry.clone();
    var myCRS = new OpenLayers.Projection("EPSG:4326");
    myGeometry.transform(this.map.getProjectionObject(),myCRS);
    return myGeometry;
  },

  switchLayer: function(name, el) {
    var layer = this.map.getLayersByName(name)[0];
    if (layer.isBaseLayer === true) {
      this.map.setBaseLayer(layer);
      // clear classes on previously selected layers
      $('#map-layerswitcher .base').removeClass('visible');
      $(el).addClass('visible');
    } else {
      if (layer.visibility) {
          layer.setVisibility(false);
          $(el).removeClass('visible');
      } else {
          layer.setVisibility(true);
          $(el).addClass('visible');
      }
    }
  },

  refreshLayerSwitcher: function() {
    var div = $('#map-layerswitcher');
    //clear out elements
    div.empty();

    var visible, base;

    _.each(this.map.layers, function(val) {
      if (val.displayInLayerSwitcher === true) {
        if (val.isBaseLayer === true) {
          base = 'base';
        } else {
          base = '';
        };
        if (val.visibility) {
            visible = 'visible';
        } else {
            visible = '';
        }

        var layerHTML = '<div class="layer-control '+ visible +' '+base+'"><img src="/static/images/'+WEB_LAYERS_IMAGE[val.name]+'" /><p>'+val.name+'</p></div>';
        div.append(layerHTML);
      }
    });
  }
}; // prototype

}(); // anon function
