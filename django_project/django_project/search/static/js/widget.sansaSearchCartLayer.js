+function () {

  "use strict"; // jshint ;_;

  APP.SearchCartLayer = function (map_object, options) {
      this.options = options || {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.SearchCartLayer.prototype = {

    _initialize: function() {
      var self = this;

      this.cartLayer = new ol.layer.Vector("Cart layer",
          {'displayInLayerSwitcher': false, 'visibility': false});

      this.map_object.map.addLayer(this.cartLayer);

      $APP.on('SearchCartLayer_addFeatures', function(evt, payload){
        self.cartLayer.removeAllFeatures();
        _.each(payload.data, function (feature) {
          const feat = new ol.Feature(
              {
                geometry: self.map_object.transformGeometry(ol.format.WKT(feature.attributes.product.spatial_coverage.split(';')[1])),
                attribute: feature.attributes
              }
          );
          self.cartLayer.addFeatures([feat]);
        });
      });

      $APP.on('SearchCartLayer_setVisibility', function(evt, visibility){
        self.cartLayer.setVisibility(visibility);
      });

  }

}; // prototype

}(); // anonfunc
