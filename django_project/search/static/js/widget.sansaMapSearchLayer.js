+function () {

  "use strict"; // jshint ;_;

  APP.SearchLayer = function (map_object, options) {
      this.options = options || {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.SearchLayer.prototype = {

    _initialize: function() {
      var defaultStyle = new OpenLayers.Style(
        {'fillOpacity': '${getFillOpacity}', 'strokeColor' : '${getColor}', 'fillColor': '#BAD696'},
        {
          context :
            {
              getColor : function (f)
                {
                  return f.attributes.strokeColor;
                },
              getFillOpacity : function (f)
                {
                  return f.attributes.fillOpacity;
                }
            }
        }
      );

      var selectStyle = new OpenLayers.Style({'strokeColor': '#2f96b4', 'fillOpacity': 0});
      var tempStyle = new OpenLayers.Style({'strokeColor': '#9EE9FF', 'fillOpacity': 0});
      var boundsStyle = new OpenLayers.Style({'strokeColor': '#FF0000', 'fillOpacity': 0});

      var style = new OpenLayers.StyleMap({'default': defaultStyle, 'select': selectStyle, 'temporary': tempStyle});
      var styleBounds = new OpenLayers.StyleMap({'default': boundsStyle});

      this.layerSearch = new OpenLayers.Layer.Vector("Search geometry", { styleMap: style } );
      this.layerBounds = new OpenLayers.Layer.Vector("Search bounds", {'displayInLayerSwitcher': false, styleMap: styleBounds});
      this.map_object.add_layer(this.layerSearch);
      this.map_object.add_layer(this.layerBounds);

      this.myHighlightControl = new OpenLayers.Control.SelectFeature(
      this.layerSearch , {
        hover: false,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
            beforefeaturehighlighted: null,
            featurehighlighted: null,
            featureunhighlighted: null
        }
      });
      this.mySelectControl = new OpenLayers.Control.SelectFeature(
      this.layerSearch , {
        hover: false,
        onSelect: $.proxy(this.featureSelected,this),
      });
    this.map_object.map.addControl(this.myHighlightControl);
    this.map_object.map.addControl(this.mySelectControl);
    this.myHighlightControl.activate();
    this.mySelectControl.activate();
    this.layerSearch.highlightFeatureControl = this.myHighlightControl;
    this.layerSearch.selectFeatureControl = this.mySelectControl;

    var self=this;
    $APP.on('ResultGridView_fetchresults', function (evt) {
      self.layerSearch.removeFeatures(self.layerSearch.features);
    });

    $APP.on('resetZoom', function (evt) {
      self.map_object.map.zoomToExtent(self.layerSearch.getDataExtent());
      $('#resetZoom').hide();
    });

    $APP.on('SearchLayer_addFeatures', function(evt, payload){
      self.layerSearch.removeAllFeatures();
      _.each(payload.data, function (feature) {
        var feat = new OpenLayers.Feature.Vector(
          self.map_object.transformGeometry(OpenLayers.Geometry.fromWKT(feature.attributes.spatial_coverage)),
          feature.attributes
        );
        // check if item is in cart
        var exist = APP.Cart.filter(function(item) {
          return item.get("product").id == feature.attributes.id;
        });

        //if item is in cart, color green else orange
        if (exist.length > 0) {
          feat.attributes.strokeColor = '#5bb75b';
          feat.attributes.fillOpacity = '0.5';
        } else {
          feat.attributes.strokeColor = '#FFA500';
          feat.attributes.fillOpacity = '0';
        }
        self.layerSearch.addFeatures([feat]);
      });
      // zoom to features extent
      self.map_object.map.zoomToExtent(self.layerSearch.getDataExtent());
    });

    $APP.on('highlightSearchRecord', function (evt, data) {
      self.highlightRecord(data.unique_product_id, data.zoom);
    });

    $APP.on('colorCartFeature', function (evt, data) {
      self.colorCartFeature(data.unique_product_id);
    });

    $APP.on('focusFeature', function (evt, data) {
      self.focusFeature(data.unique_product_id);
    });

    $APP.on('removeFocusFeature', function (evt, data) {
      self.removeFocusFeature(data.unique_product_id);
    });

    $APP.on('removedItemFromCart', function (evt, data) {
      self.removedItemFromCart(data.unique_product_id);
    });

    $APP.on('drawCircle', function (evt, data) {
      self.drawCircle(data.x, data.y, data.r);
    });

    $APP.on('drawBox', function (evt, data) {
      self.drawBox(data.x1, data.y1, data.x2, data.y2);
    });

    $APP.on('drawWKT', function (evt, data) {
      self.drawWKT(data.wkt);
    });

    $APP.on('clearAoiBounds', function (evt, data) {
      self.layerBounds.removeAllFeatures();
    });
  },

  drawBox: function(x1,y1,x2,y2) {
    var poly = this.map_object.transformBounds(new OpenLayers.Bounds(x1,y1,x2,y2)).toGeometry();
    var featurebox = new OpenLayers.Feature.Vector(poly);
    this.layerBounds.addFeatures([featurebox]);
    APP.BoundsFeature = featurebox;
  },

  drawWKT: function(wkt) {
    var featurebox = new OpenLayers.Format.WKT().read(wkt);
    featurebox.geometry.transform(new OpenLayers.Projection("EPSG:4326"),new OpenLayers.Projection("EPSG:900913"));
    this.layerBounds.addFeatures([featurebox]);
    APP.BoundsFeature = featurebox;
  },

  drawCircle: function(x,y,r) {
    this.layerBounds.removeAllFeatures();
    var mycircle = this.map_object.transformGeometry(OpenLayers.Geometry.Polygon.createRegularPolygon
      (
          new OpenLayers.Geometry.Point(x, y),
          r/111,
          20,
          0
      ));
    var featurecircle = new OpenLayers.Feature.Vector(mycircle);
    this.layerBounds.addFeatures([featurecircle]);
    APP.BoundsFeature = featurecircle;
  },

  featureSelected: function(theEvent) {
    APP.blockResultPanel();
    var id = theEvent.attributes.unique_product_id;
    $APP.trigger('highlightResultItem', {'id': id});
    this.highlightRecord(id, false);
    APP.unblockResultPanel();
  },

  highlightRecord: function( theRecordId, theZoomFlag ) {
    var myIndex = this.getFeatureIndexByRecordId( theRecordId );
    this.layerSearch.features[myIndex].attributes.zIndex=1;
    this.layerSearch.features[myIndex].selected = "yes";
    if (theZoomFlag)
    {
      this.map_object.map.zoomToExtent(this.layerSearch.features[myIndex].geometry.bounds);
    }
    this.layerSearch.redraw();
    this.layerSearch.selectFeatureControl.highlight( this.layerSearch.features[myIndex]);
    this.resetSceneZIndices();
    APP.selectedFeatureID = theRecordId;
  },

  colorCartFeature: function( theRecordId ) {
    var myIndex = this.getFeatureIndexByRecordId( theRecordId );
    this.layerSearch.features[myIndex].attributes.strokeColor = '#5bb75b';
    this.layerSearch.features[myIndex].attributes.fillOpacity = '0.5';
    this.layerSearch.redraw();
  },

  removedItemFromCart: function( theRecordId ) {
    var myIndex = this.getFeatureIndexByRecordId( theRecordId );
    this.layerSearch.features[myIndex].attributes.strokeColor = '#FFA500';
    this.layerSearch.features[myIndex].attributes.fillOpacity = '0';
    this.layerSearch.redraw();
  },

  removeFocusFeature: function( theRecordId ) {
    var myIndex = this.getFeatureIndexByRecordId( theRecordId );
    this.layerSearch.highlightFeatureControl.unhighlight( this.layerSearch.features[myIndex]);
  },

  focusFeature: function( theRecordId ) {
    var myIndex = this.getFeatureIndexByRecordId( theRecordId );
    this.layerSearch.highlightFeatureControl.highlight( this.layerSearch.features[myIndex]);
  },

  getFeatureIndexByRecordId: function( theRecordId ) {
    var myFeatures = this.layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      if(myFeatures[i].attributes.unique_product_id == theRecordId)
      {
        return i;
      }
    }
  },

  getFeatureElementRecordId: function( theRecordId ) {
    var myFeatures = this.layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      if(myFeatures[i].attributes.unique_product_id == theRecordId)
      {
        return myFeatures[i];
      }
    }
  },

  resetSceneZIndices: function() {
    var myFeatures = this.layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i) {
        myFeatures[i].attributes.zIndex=0;
        myFeatures[i].selected = "no";
    }
}

}; // prototype

}(); // anonfunc