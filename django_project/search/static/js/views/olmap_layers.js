define([
    'shared',
    'backbone',
    'underscore',
    'jquery',
    'jqueryTouch',
    'ol',
    'views/layer_style',
    'collections/paginated'
], function (Shared, Backbone, _, $, jqueryTouch, ol, LayerStyle, ResultItemCollection) {
    return Backbone.View.extend({
        // source of layers
        layers: {},
        orders: {},
        layerSelector: null,
        layerSearchSource: null,
        initialize: function () {
            this.layerStyle = new LayerStyle();
            this.layerSearchSource = new ol.source.Vector({})
        },

        initLayer: function (layer, layerName, visibleInDefault, category, source) {
            layer.set('added', false);
            var layerType = layerName;
            var layerSource = '';
            var layerCategory = '';
            try {
                var layerOptions = layer.getSource()['i'];
                if (layerOptions) {
                    layerType = layer.getSource()['i']['layers'];
                }
            } catch (e) {
                if (e instanceof TypeError) {
                }
            }
            if (layerName === 'Search results') {
                layerType = layerName;
            }

            var savedLayerVisibility = Shared.StorageUtil.getItemDict(layerType, 'selected');

            if (savedLayerVisibility !== null) {
                visibleInDefault = savedLayerVisibility;
            }

            if (category) {
                layerCategory = category;
            }
            if (source) {
                layerSource = source;
            }

            this.layers[layerType] = {
                'layer': layer,
                'visibleInDefault': visibleInDefault,
                'layerName': layerName,
                'category': layerCategory,
                'source': layerSource
            };
            if (!visibleInDefault) {
                layer.setVisible(false);
            }
        },
        addSearchResultLayersToMap: function (map) {
            const self = this;
            self.layerSearchSource = new ol.source.Vector({});
            self.layerSearchVector = new ol.layer.Vector({
                source: self.layerSearchSource,
                style: function (feature) {
                    var geom = feature.getGeometry();
                    return self.layerStyle.getPinnedHighlightStyle(geom.getType());
                }
            });
            map.addLayer(self.layerSearchVector);

            self.initLayer(
                self.layerSearchVector,
                'Search results',
                true,
            );
        },

        addLayersToMap: function (map) {
            var self = this;
            this.map = map;
            self.orders[0] = 'Search results';
            self.addSearchResultLayersToMap(
                map
            )
            self.renderLayers(true);
        },


        renderLayers: function (isFirstTime) {
            let self = this;
            let savedOrders = $.extend({}, self.orders);

            // Reverse orders
            let reversedOrders = savedOrders;
            if (isFirstTime) {
                reversedOrders = [];
                $.each(savedOrders, function (key, value) {
                    reversedOrders.unshift(value);
                });
            }

            $.each(reversedOrders, function (index, key) {
                var value = self.layers[key];
                var layerName = '';
                var defaultVisibility = false;
                var category = '';
                var source = '';

                if (typeof value !== 'undefined') {
                    layerName = value['layerName'];
                    defaultVisibility = value['visibleInDefault'];
                    if (value.hasOwnProperty('category')) {
                        category = value['category'];
                    }
                    if (value.hasOwnProperty('source')) {
                        source = value['source'];
                    }
                } else {
                    layerName = key;
                }

                if (typeof layerName === 'undefined') {
                    return true;
                }

                var currentLayerTransparency = 100;

                // Get saved transparency data from storage
                var itemName = key;
                var layerTransparency = Shared.StorageUtil.getItemDict(itemName, 'transparency');
                if (layerTransparency !== null) {
                    currentLayerTransparency = layerTransparency * 100;
                    self.changeLayerTransparency(itemName, layerTransparency);
                } else {
                    currentLayerTransparency = 100;
                }
            });

            // RENDER LAYERS
            $.each(self.layers, function (key, value) {
                let _layer = value['layer'];
                if (!_layer.get('added')) {
                    _layer.set('added', true);
                    // self.map.addLayer(_layer);
                }
            });
        },



    })
});