+function () {

  "use strict"; // jshint ;_;

  APP.GeoSearchLayer = function (map_object, options) {
      this.options = options || {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.GeoSearchLayer.prototype = {

    _initialize: function() {
      this.geoSearch = new OpenLayers.Layer.Vector("Polygon select", {'displayInLayerSwitcher': false});

      this.mWKTFormat = new OpenLayers.Format.WKT();

      this.map_object.map.addLayer(this.geoSearch);

      this.geoSearch.events.on({"featuremodified" : $.proxy(this.modifyWKT, this)});
      this.geoSearch.events.on({"featureadded" : $.proxy(this.addWKT, this)});
      this.geoSearch.events.on({"featureremoved": this.removeWKT});

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

    var DestroyFeatures = OpenLayers.Class(OpenLayers.Control, {
      type: OpenLayers.Control.TYPE_BUTTON,
      trigger: function() {
        this.layer.destroyFeatures();
      }
    });

    var myDestroyFeaturesControl = new DestroyFeatures({
      'displayClass': 'right icon-remove icon-2x icon-border destroyFeature',
      'title':'Delete polygon: deletes polygon',
      'layer': this.geoSearch,
      div : OpenLayers.Util.getElement('map-navigation'),
    });

    // add controls to the panel
    this.map_object.mNavigationPanel.addControls(
      [myDrawingControl, myModifyFeatureControl, myDestroyFeaturesControl]);
  },
  /* ------------------------------------------------------
 * OpenLayers WKT manipulators
 * -------------------------------------------------------- */
  readWKT: function (wkt) {
    // OpenLayers cannot handle EWKT -- we make sure to strip it out.
    // EWKT is only exposed to OL if there's a validation error in the admin.
    var myRegularExpression = new RegExp("^SRID=\\d+;(.+)", "i");
    var myMatch = myRegularExpression.exec(wkt);
    if (myMatch)
    {
      wkt = myMatch[1];
    }
    var feature = this.mWKTFormat.read(wkt);
    if (feature) {
      return feature.geometry;
    }
  },

  writeWKT: function(geometry) {
    var myGeometry = geometry.clone();
    var myUnprojectedGeometry = this.map_object.reverseTransformGeometry(myGeometry);
    document.getElementById('id_geometry').value =
     'SRID=4326;' + this.mWKTFormat.write(new OpenLayers.Feature.Vector(myUnprojectedGeometry));
  },

  addWKT: function(event) {
    // This function will sync the contents of the `vector` layer with the
    // WKT in the text field.
    // Make sure to remove any previously added features.
    if (this.geoSearch.features.length > 1){
      var myOldFeatures = [this.geoSearch.features[0]];
      this.geoSearch.removeFeatures(myOldFeatures);
      this.geoSearch.destroyFeatures(myOldFeatures);
    }
    this.writeWKT(event.feature.geometry);
  },

  modifyWKT: function(event) {
    this.writeWKT(event.feature.geometry);
  },

  removeWKT: function(event) {
    document.getElementById('id_geometry').value = '';
  }

}; // prototype

}(); // anonfunc