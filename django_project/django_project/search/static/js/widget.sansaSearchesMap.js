+function () {

  "use strict"; // jshint ;_;

  APP.SansaSearchesMap = function (map_id) {
      this.map_element = map_id;
      this.loadMap();

      // return the object
      return this;
  };

  APP.SansaSearchesMap.prototype = {
    isBoundaryEnabled: false,
    // attributes
    mapInteractionEnabled: false,
    previousZoom: 0,
    sidePanelView: null,
    initZoom: 8,
    numInFlightTiles: 0,
    mapIsReady: false,
    polygonDrawn: false,
    initCenter: [22.948492328125, -31.12543669218031],
    scaleLineControl: null,
    defaultExtentMap: "-20037508.34, -20037508.34,20037508.34, 20037508.34",
    events: {
            'click .zoom-in': 'zoomInMap',
            'click .zoom-out': 'zoomOutMap',
            'click .layer-control': 'layerControlClicked',
            'click #map-legend-wrapper': 'mapLegendClicked',
            'click .print-map-control': 'downloadMap',
            'click #start-tutorial': 'startTutorial',
        },
    // default_options: {
    //   projection : new ol.proj.Projection("EPSG:900913"),
    //   displayProjection : new ol.proj.Projection("EPSG:4326"),
    //   units : 'm',
    //   maxResolution: 156543.0339,
    //   maxExtent: ol.extent.boundingExtent([[-20037508.34, -20037508.34],[20037508.34, 20037508.34]]),
    //   numZoomLevels : 18,
    //   controls: []
    // },

    initLayers: function() {
      var layerMapnik = new ol.source.OSM();

      var myLayersList = [
            WEB_LAYERS.searches,
            // WEB_LAYERS.BlueMarble,
            // WEB_LAYERS.Heatmap_total,
            // WEB_LAYERS.Heatmap_last3month,
            // WEB_LAYERS.Heatmap_lastmonth,
            // WEB_LAYERS.Heatmap_lastweek,
            layerMapnik
        ];
        this.map.addLayer(myLayersList);
    },

    loadMap: function() {
      var self = this;
      var mousePositionControl = new ol.control.MousePosition({
        projection: 'EPSG:4326',
        target: document.getElementById('mouse-position-wrapper'),
        coordinateFormat: function (coordinate) {
          return ol.coordinate.format(coordinate, '{y},{x}', 4);
        }
      });
      var center = this.initCenter;

      // Add scaleline control
      let scalelineControl = new ol.control.ScaleLine({
        units: 'metric',
        bar: true,
        steps: 4,
        text: true,
        minWidth: 140
      })

      let extent = this.defaultExtentMap.split(',');
      let newExtent = [];
      for (let e=0; e < extent.length; e++) {
        newExtent.push(parseFloat(extent[e]));
      }
      extent = ol.proj.transformExtent(newExtent, 'EPSG:4326', 'EPSG:900913');
      this.map = new ol.Map({
        target: 'map',
        // layers: myLayersList,
        view: new ol.View({
          center: ol.proj.fromLonLat(center),
          zoom: this.initZoom,
          minZoom: 5,
          maxZoom: 19, // prevent zooming past 50m
        }),
        controls: ol.control.defaults({
          zoom: false
        }).extend([
            mousePositionControl,
            scalelineControl
        ])
      });
      this.map.getView().fit(extent);
      this.initLayers();

    // this.map.zoomToExtent(this.transformBounds(ol.extent.boundingExtent([[-90.0,-45.0], [90.0, 45.0]])));

    // this.mNavigationPanel = new OpenLayers.Control.Panel({div : OpenLayers.Util.getElement('map-navigation'), allowDepress: true});
    // this.mNavigationPanel.allowDepress = true;
    // this.map.addControl(this.mNavigationPanel);
    //
    // var modifyEventListeners = {
    //     "activate": function() {
    //       $(this.panel_div).removeClass("btn-info");
    //       $(this.panel_div).addClass("btn-success");
    //     },
    //     "deactivate": function() {
    //       $(this.panel_div).removeClass("btn-success");
    //       $(this.panel_div).addClass("btn-info");
    //     }
    // };

    // var myZoomInControl = new OpenLayers.Control.ZoomBox({
    //   title: "Zoom In Box: draw a box on the map, to see the area at a larger scale.",
    //   displayClass:'btn btn-large btn-info right icon-zoom-in olControlZoomBoxIn',
    //   div: OpenLayers.Util.getElement('map-navigation'),
    //   out: false,
    //   eventListeners: modifyEventListeners
    // });
    //
    // var myZoomOutControl = new OpenLayers.Control.ZoomBox({
    //       title: "Zoom Out Box: draw a box on the map, to see the area at a smaller scale.",
    //       displayClass:'btn btn-large btn-info right icon-zoom-out olControlZoomBoxOut',
    //       div: OpenLayers.Util.getElement('map-navigation'),
    //       out: true,
    //       eventListeners: modifyEventListeners
    //     });
    //
    // var myNavigationControl = new OpenLayers.Control.Navigation({
    //   title : "Pan map: click and drag map to move the map in the direction of the mouse.",
    //   zoomWheelEnabled: false,
    //   displayClass:'btn btn-large btn-info right icon-move olControlNavigation',
    //   div: OpenLayers.Util.getElement('map-navigation'),
    //   eventListeners: modifyEventListeners
    // });
    //
    // var myHistoryControl = new OpenLayers.Control.NavigationHistory({
    //   nextOptions: {
    //     title : "Next view: quickly jump to the next map view, works only with previous view.",
    //     displayClass:'btn btn-large btn-info right icon-chevron-right olControlNavigationHistoryNext',
    //     div: OpenLayers.Util.getElement('map-navigation'),
    //     eventListeners: modifyEventListeners
    //   },
    //   previousOptions: {
    //     title : "Previous view: quickly jump to the previous map view.",
    //     displayClass:'btn btn-large btn-info right icon-chevron-left olControlNavigationHistoryPrevious',
    //     div: OpenLayers.Util.getElement('map-navigation'),
    //     eventListeners: modifyEventListeners
    //   }
    // });
    //
    // this.mNavigationPanel.addControls(
    //   [myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.previous, myHistoryControl.next]
    // );
    //
    // // Make the pan navigation button default selected
    // this.mNavigationPanel.activateControl(myNavigationControl);

    this.refreshLayerSwitcher();

    // this.map.addControl(new OpenLayers.Control.MousePosition({'div': document.getElementById("map-control-position")}));
    // this.map.addControl(new OpenLayers.Control.ScaleBar({
    //     align: "left",
    //     minWidth: 150,
    //     maxWidth: 200,
    //     div: document.getElementById("map-control-scalebar")
    //   }));

    $('#map-layerswitcher').on('click', '.layer-control', function(evt,data){
      var myLayer = $(evt.currentTarget).text();
      self.switchLayer(myLayer,$(evt.currentTarget));
    });
    },
    zoomInMap: function (e) {
      var view = this.map.getView();
      var zoom = view.getZoom();
      view.animate({
        zoom: zoom - 1,
        duration: 250
      })
    },
    boundaryEnabled: function (value) {
      this.isBoundaryEnabled = value;
      },
    zoomOutMap: function (e) {
      var view = this.map.getView();
      var zoom = view.getZoom();
      view.animate({
        zoom: zoom + 1,
        duration: 250
      })
    },
    zoomToCoordinates: function (coordinates, zoomLevel) {
      this.previousZoom = this.getCurrentZoom();
      this.map.getView().setCenter(coordinates);
      if (typeof zoomLevel !== 'undefined') {
        this.map.getView().setZoom(zoomLevel);
      }
      },
    zoomToExtent: function (coordinates, shouldTransform=true, updateZoom=true) {

      this.previousZoom = this.getCurrentZoom();
      let ext = coordinates;
      if (shouldTransform) {
        ext = ol.proj.transformExtent(coordinates, ol.proj.get('EPSG:4326'), ol.proj.get('EPSG:900913'));
      }
      if (this.polygonDrawn) {
        ext = this.polygonDrawn;
      }
      this.map.getView().fit(ext, {
        size: this.map.getSize(), padding: [
            0, $('.right-panel').width(), 0, 250
        ]
      });
      if (updateZoom && !this.polygonDrawn) {
        if (this.map.getView().getZoom() > 8) {
          this.map.getView().setZoom(8);
        }
      }
      },
    setPolygonDrawn: function (polygon) {
           this.polygonDrawn = polygon
    },
    getCurrentZoom: function () {
      return this.map.getView().getZoom();
      },
    removeLayer: function (layer) {
      this.map.removeLayer(layer);
      },
    addLayer: function (layer) {
      this.map.addLayer(layer);
      },
    whenMapIsReady: function (callback) {
      const self = this;
      if (this.mapIsReady)
        callback();
      else {
        setTimeout(function () {
          self.map.once('change:ready', self.whenMapIsReady.bind(null, callback));
          self.whenMapIsReady(callback);
          }, 100)
      }
      },

    downloadMap: function () {
      var that = this;
      var downloadMap = true;

      that.map.once('postcompose', function (event) {
        var canvas = event.context.canvas;
        try {
          canvas.toBlob(function (blob) {
          })
        }
        catch (error) {
          $('#error-modal').modal('show');
          downloadMap = false
        }
      });
      that.map.renderSync();

      if (downloadMap) {
        $('#ripple-loading').show();
        $('.map-control-panel').hide();
        $('.zoom-control').hide();
        $('.bug-report-wrapper').hide();
        $('.print-map-control').addClass('control-panel-selected');
        that.whenMapIsReady(function () {
          const canvas = document.getElementsByClassName('map-wrapper');
          const $mapWrapper = $('.map-wrapper');
          const divHeight = $mapWrapper.height();
          const divWidth = $mapWrapper.width();
          const ratio = divHeight / divWidth;
          html2canvas(canvas, {
            useCORS: true,
            background: '#FFFFFF',
            allowTaint: false,
            onrendered: function (canvas) {
              const link = document.createElement('a');
              link.setAttribute("type", "hidden");
              link.href = canvas.toDataURL("image/png");
              link.download = 'map.png';
              document.body.appendChild(link);
              link.click();
              link.remove();
              $('.zoom-control').show();
              $('.map-control-panel').show();
              $('#ripple-loading').hide();
              $('.bug-report-wrapper').show();
              $('.print-map-control').removeClass('control-panel-selected');
            }
          })
        });
      }
      },

  // transformBounds: function (theBounds)
  // {
  //   var myBounds = theBounds.clone();
  //   var myCRS = new OpenLayers.Projection("EPSG:4326");
  //   var toCRS = this.map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
  //   myBounds.transform(myCRS, toCRS);
  //   return myBounds;
  // },


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
