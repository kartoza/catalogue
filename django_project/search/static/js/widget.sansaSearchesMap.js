+function () {

  "use strict"; // jshint ;_;

  APP.SansaSearchesMap = function (map_id) {
      this.map_element = map_id;
      this._initialize();

      // return the object
      return this;
  };

  APP.SansaSearchesMap.prototype = {
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
            WEB_LAYERS.searches,
            WEB_LAYERS.BlueMarble,
            WEB_LAYERS.Heatmap_total,
            WEB_LAYERS.Heatmap_last3month,
            WEB_LAYERS.Heatmap_lastmonth,
            WEB_LAYERS.Heatmap_lastweek,
            layerMapnik
        ];
        this.map.addLayers(myLayersList);
    },

    _initialize: function() {
      var self = this;
      this.map = new OpenLayers.Map(this.map_element, this.default_options);

      this.initLayers();

    this.map.zoomToExtent(this.transformBounds(new OpenLayers.Bounds(-90.0,-45.0, 90.0, 45.0)));

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
        title : "Next view: quickly jump to the next map view, works only with previous view.",
        displayClass:'btn btn-large btn-info right icon-chevron-right olControlNavigationHistoryNext',
        div: OpenLayers.Util.getElement('map-navigation'),
        eventListeners: modifyEventListeners
      },
      previousOptions: {
        title : "Previous view: quickly jump to the previous map view.",
        displayClass:'btn btn-large btn-info right icon-chevron-left olControlNavigationHistoryPrevious',
        div: OpenLayers.Util.getElement('map-navigation'),
        eventListeners: modifyEventListeners
      }
    });

    this.mNavigationPanel.addControls(
      [myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.previous, myHistoryControl.next]
    );

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

  transformBounds: function (theBounds)
  {
    var myBounds = theBounds.clone();
    var myCRS = new OpenLayers.Projection("EPSG:4326");
    var toCRS = this.map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
    myBounds.transform(myCRS, toCRS);
    return myBounds;
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
