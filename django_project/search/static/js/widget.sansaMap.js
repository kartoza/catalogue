// avoid pink tiles
// OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;
// OpenLayers.Util.onImageLoadErrorColor = "transparent";

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
      var TMSOverlay = new OpenLayers.Layer.TMS(
        "2012 Mosaic", "http://maps.sansa.org.za/SPOT2012-BM/", {
            layername: '.',
            type: 'png',
            getURL: this.overlay_getTileURL,
            alpha: false,
            isBaseLayer: false,
            // layer specific variables
            // make sure we correctly transform bounds to the map projection
            TMSLayerBounds: this.transformBounds(new OpenLayers.Bounds( 16.0, -34.9999882412, 32.9999919763, -22.0)),
            TMSLayerMinZoom: 1,
            TMSLayerMaxZoom: 15
        });

      var layerMapnik = new OpenLayers.Layer.OSM("Open Street Map");

      var myLayersList = [
            TMSOverlay,
            layerMapnik
        ];
        this.map.addLayers(myLayersList);
    },

    _initialize: function() {
      var self = this;
      this.map = new OpenLayers.Map(this.map_element, this.default_options);

      this.initLayers();

    this.map.zoomToExtent(this.transformBounds(new OpenLayers.Bounds(14.0,-35.0,34.0,-21.0)));

    this.mNavigationPanel = new OpenLayers.Control.Panel({div : OpenLayers.Util.getElement('map-navigation'), allowDepress: true});
    this.mNavigationPanel.allowDepress = true;
    this.map.addControl(this.mNavigationPanel);

    var modifyEventListeners = {
        "activate": function() {
          $(this.panel_div).removeClass("btn-info");
          $(this.panel_div).addClass("btn-success");
        },
        "deactivate": function() {
          $(this.panel_div).removeClass("btn-success");
          $(this.panel_div).addClass("btn-info");
        }
    };

    var myZoomInControl = new OpenLayers.Control.ZoomBox({
      title: "Zoom In Box: draw a box on the map, to see the area at a larger scale.",
      displayClass:'btn btn-large btn-info right icon-zoom-in olControlZoomBoxIn',
      div: OpenLayers.Util.getElement('map-navigation'),
      out: false,
      eventListeners: modifyEventListeners
    });

    var myZoomOutControl = new OpenLayers.Control.ZoomBox({
          title: "Zoom Out Box: draw a box on the map, to see the area at a smaller scale.",
          displayClass:'btn btn-large btn-info right icon-zoom-out olControlZoomBoxOut',
          div: OpenLayers.Util.getElement('map-navigation'),
          out: true,
          eventListeners: modifyEventListeners
        });

    var myNavigationControl = new OpenLayers.Control.Navigation({
      title : "Pan map: click and drag map to move the map in the direction of the mouse.",
      zoomWheelEnabled: false,
      displayClass:'btn btn-large btn-info right icon-move olControlNavigation',
      div: OpenLayers.Util.getElement('map-navigation'),
      eventListeners: modifyEventListeners
    });

    var myHistoryControl = new OpenLayers.Control.NavigationHistory({
      nextOptions: {
        title : "Next view: quickly jump to the next map view, works only with prevoius view.",
        displayClass:'olnext btn btn-large btn-info disabled right icon-chevron-right olControlNavigationHistoryNext',
        div: OpenLayers.Util.getElement('map-navigation'),
        eventListeners: modifyEventListeners
      },
      previousOptions: {
        title : "Previous view: quickly jump to the prevoius map view.",
        displayClass:'olprev btn btn-large disabled btn-info right icon-chevron-left olControlNavigationHistoryPrevious',
        div: OpenLayers.Util.getElement('map-navigation')
      },
      onPreviousChange: function() {
        if (myHistoryControl.previousStack.length > 1) {
          $('.olprev').removeClass('disabled');
        } else {
          $('.olprev').addClass('disabled');
        }
      },
      onNextChange: function() {
        if (myHistoryControl.nextStack.length > 0) {
          $('.olnext').removeClass('disabled');
        } else {
          $('.olnext').addClass('disabled');
        }
      }
    });
    this.map.addControl(myHistoryControl);

    this.mNavigationPanel.addControls(
      [myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.previous, myHistoryControl.next]
    );

    // Make the pan navigation button default selected
    this.mNavigationPanel.activateControl(myNavigationControl);

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

  add_control: function(theControl) {
    this.map.addControl(theControl);
  },

  add_popup: function(popup) {
    this.map.addPopup(popup);
  },

  remove_popup: function(popup) {
    this.map.removePopup(popup);
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
      $('#map-controls3').html(WEB_LAYERS_DESC[layer.name]);
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
            if (val.isBaseLayer === true) $('#map-controls3').html(WEB_LAYERS_DESC[val.name]);
            visible = 'visible';
        } else {
            visible = '';
        }

        var layerHTML = '<div class="layer-control '+ visible +' '+base+'"><img src="/static/images/'+WEB_LAYERS_IMAGE[val.name]+'" /><p>'+val.name+'</p></div>';
        div.append(layerHTML);
      }
    });
  },
  overlay_getTileURL: function(bounds) {
    var res = this.map.getResolution();
    var x = Math.round((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
    var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));
    var z = this.map.getZoom();

    if (this.map.baseLayer.name == 'Virtual Earth Roads' || this.map.baseLayer.name == 'Virtual Earth Aerial' || this.map.baseLayer.name == 'Virtual Earth Hybrid') {
       z = z + 1;
    }
    if (this.TMSLayerBounds.intersectsBounds( bounds ) && z >= this.TMSLayerMinZoom && z <= this.TMSLayerMaxZoom ) {
       //console.log( this.url + z + "/" + x + "/" + y + "." + this.type);
       return this.url + z + "/" + x + "/" + y + "." + this.type;
    } else {
       return "http://www.maptiler.org/img/none.png";
    }
}
}; // prototype

}(); // anon function
