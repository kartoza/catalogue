+function () {

  "use strict"; // jshint ;_;

  APP.SearchLayer = function (map_object, options) {
      this.options = options || {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.SearchLayer.prototype = {

    _initialize: function() {
      this.layerSearch = new OpenLayers.Layer.Vector("Search geometry");
      this.map_object.map.addLayers([this.layerSearch]);

      var myHighlightControl = new OpenLayers.Control.SelectFeature(
      this.layerSearch , {
        hover: false,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
            beforefeaturehighlighted: null,
            featurehighlighted: this.featureSelected,
            featureunhighlighted: null
        }
      }
    );
    this.map_object.map.addControl(myHighlightControl);
    myHighlightControl.activate();
    this.layerSearch.selectFeatureControl = myHighlightControl;

    var self=this;
    $APP.on('ResultGridView_fetchresults', function (evt) {
      self.layerSearch.removeFeatures(self.layerSearch.features);
    });

    $APP.on('SearchLayer_addFeatures', function(evt, payload){
      _.each(payload.data, function (feature) {
        var feat = new OpenLayers.Feature.Vector(
          self.map_object.transformGeometry(OpenLayers.Geometry.fromWKT(feature.attributes.spatial_coverage)),
          feature.attributes
        );
        self.layerSearch.addFeatures([feat]);
      });
      // zoom to features extent
      self.map_object.map.zoomToExtent(self.layerSearch.getDataExtent());
    });

    $APP.on('highlightSearchRecord', function (evt, data) {
      self.highlightRecord(data.unique_product_id, true);
    });
  },

  featureSelected: function(theEvent) {
    APP.blockResultPanel();
    this.hightlightRecord(theEvent.feature.attributes.unique_product_id, false);
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
    this.resetSceneZIndices();
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

  resetSceneZIndices: function() {
    var myFeatures = this.layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i) {
        myFeatures[i].attributes.zIndex=0;
        myFeatures[i].selected = "no";
    }
}

}; // prototype

}(); // anonfunc