+function () {

  "use strict"; // jshint ;_;

  APP.CartLayer = function (map_object, options) {
      this.options = options || {};
      this.features = {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.CartLayer.prototype = {

    _initialize: function() {

      this.layerCart = new OpenLayers.Layer.Vector("Cart", {'displayInLayerSwitcher': false});
      this.map_object.add_layer(this.layerCart);
      var feat = [];
      for(var index in this.options.wkt) {
        var featData = this.options.wkt[index].wkt;
        this.features[index] = new OpenLayers.Feature.Vector(this.map_object.transformGeometry(OpenLayers.Geometry.fromWKT(featData)));
        this.features[index].attributes = { 'id': index, 'original_product_id': this.options.wkt[index].id };
        feat.push(this.features[index]);
      }
      this.layerCart.addFeatures(feat);

      this.highlightCtrl = new OpenLayers.Control.SelectFeature(this.layerCart, {
        hover: true,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
          featurehighlighted: $.proxy(this.featureHighlighted, this),
          featureunhighlighted: $.proxy(this.featureUnhighlighted, this)
        }
      });
      this.map_object.add_control(this.highlightCtrl);
      this.highlightCtrl.activate();
      this.zoomToAllFeatures();
  },

  featureHighlighted: function(evt) {
    var data = evt.feature.attributes;
    var point = evt.feature.geometry.getCentroid();
    var lonlat = new OpenLayers.LonLat(point.x, point.y);

    var html = '<span class="loud white">' + data.productName + '</span>';
    html = html + '<img src="/thumbnail/'+ data.id +'/large/" />';

    this.popup = new OpenLayers.Popup.Anchored(
        'myPopup',
        lonlat,
        new OpenLayers.Size(250, 268),
        html,
        {size: {w: 14, h: 14}, offset: {x: -7, y: -7}},
        false
    );
    this.popup.setBackgroundColor('#000');
    this.popup.setOpacity(1);
    this.map_object.add_popup(this.popup);
  },

  featureUnhighlighted: function(evt) {
    this.map_object.remove_popup(this.popup);
  },

  removeFeature: function(featID) {
    var feat = this.features[featID];
    this.layerCart.removeFeatures([feat]);
    delete this.features[featID];
    this.zoomToAllFeatures();
  },

  zoomToAllFeatures: function() {
    this.map_object.map.zoomToExtent(this.layerCart.getDataExtent());
  }

}; // prototype

}(); // anonfunc