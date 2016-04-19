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

      this.cartLayer = new OpenLayers.Layer.Vector("Cart layer", {'displayInLayerSwitcher': false, 'visibility': false});

      this.map_object.map.addLayer(this.cartLayer);

      $APP.on('SearchCartLayer_addFeatures', function(evt, payload){
        self.cartLayer.removeAllFeatures();
        _.each(payload.data, function (feature) {
          var feat = new OpenLayers.Feature.Vector(
            self.map_object.transformGeometry(OpenLayers.Geometry.fromWKT(feature.attributes.product.spatial_coverage.split(';')[1])),
            feature.attributes
          );
          self.cartLayer.addFeatures([feat]);
        });
      });

      $APP.on('SearchCartLayer_setVisibility', function(evt, visiblity){
        self.cartLayer.setVisibility(visiblity);
      });

  }

}; // prototype

}(); // anonfunc
