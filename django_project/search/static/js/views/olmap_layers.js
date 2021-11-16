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
        
        changeLayerVisibility: function (layerName, visible) {
            if (Object.keys(this.layers).length === 0) {
                return false;
            }
            this.layers[layerName]['layer'].setVisible(visible);
        },

        getLegendElement: function (layerName) {
            return $(".control-drop-shadow").find(
                "[data-name='" + layerName + "']");
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

        showFeatureInfo: function (lon, lat, siteExist = false) {
            // Show feature info from lon and lat
            // Lon and lat coordinates are in EPSG:3857 format

            lon = parseFloat(lon);
            lat = parseFloat(lat);
            const coordinate = ol.proj.transform([lon, lat], 'EPSG:4326', 'EPSG:3857');

            if (Shared.GetFeatureRequested) {
                Shared.GetFeatureRequested = false;
                Shared.Dispatcher.trigger('map:hidePopup');
                if (Shared.GetFeatureXHRRequest.length > 0) {
                    $.each(Shared.GetFeatureXHRRequest, function (index, request) {
                        request.abort();
                    });
                    Shared.GetFeatureXHRRequest = [];
                }
                return;
            }
            const that = this;
            const view = this.map.getView();
            let lastCoordinate = coordinate;
            let featuresInfo = {};

            Shared.GetFeatureRequested = true;
            Shared.Dispatcher.trigger('map:showPopup', coordinate,
                '<div class="info-popup popup-loading"> Fetching... </div>');
            $.each(this.layers, function (layer_key, layer) {
                if (coordinate !== lastCoordinate) {
                    return;
                }
                if (layer['layer'].getVisible()) {
                    try {
                        const queryLayer = layer['layer'].getSource().getParams()['layers'];
                        if (queryLayer.indexOf('location_site_view') > -1) {
                            return true;
                        }
                        const getFeatureFormat = layer['layer'].getSource().getParams()['getFeatureFormat'];
                        const layerName = layer['layer'].getSource().getParams()['name'];
                        let layerSource = layer['layer'].getSource().getGetFeatureInfoUrl(
                            coordinate,
                            view.getResolution(),
                            view.getProjection(),
                            {'INFO_FORMAT': getFeatureFormat}
                        );
                        layerSource += '&QUERY_LAYERS=' + queryLayer;
                        Shared.GetFeatureXHRRequest.push($.ajax({
                            type: 'POST',
                            url: '/get_feature/',
                            data: {
                                'layerSource': layerSource
                            },
                            success: function (data) {
                                // process properties
                                if (coordinate !== lastCoordinate || !data) {
                                    return;
                                }
                                let linesData = data.split("\n");
                                let properties = {};

                                // reformat plain text to be dictionary
                                // because qgis can't support info format json
                                $.each(linesData, function (index, string) {
                                    var couple = string.split(' = ');
                                    if (couple.length !== 2) {
                                        return true;
                                    } else {
                                        if (couple[0] === 'geom') {
                                            return true;
                                        }
                                        properties[couple[0]] = couple[1];
                                    }
                                });
                                if ($.isEmptyObject(properties)) {
                                    return;
                                }
                                featuresInfo[layer_key] = {
                                    'layerName': layer['layerName'],
                                    'properties': properties
                                };
                            },
                        }));
                    } catch (err) {

                    }
                }
            });
            Promise.all(Shared.GetFeatureXHRRequest).then(() => {
                if (Object.keys(featuresInfo).length > 0) {
                    that.renderFeaturesInfo(featuresInfo, coordinate);
                } else {
                    Shared.Dispatcher.trigger('map:closePopup');
                }
                Shared.GetFeatureXHRRequest = [];
            }).catch((err) => {
                if (Shared.GetFeatureXHRRequest.length > 0) {
                    Shared.Dispatcher.trigger('map:showPopup', coordinate,
                        '<div class="info-popup popup-error">Failed to fetch feature info</div>');
                    Shared.GetFeatureXHRRequest = [];
                }
            });
        },

        renderFeaturesInfo: function (featuresInfo, coordinate) {
            var that = this;
            let tabs = '<ul class="nav nav-tabs">';
            let content = '';
            $.each(featuresInfo, function (key_feature, feature) {
                var layerName = feature['layerName'];
                tabs += '<li ' +
                    'role="presentation" class="info-wrapper-tab"  ' +
                    'title="' + layerName + '" ' +
                    'data-tab="info-' + key_feature + '">' +
                    layerName + '</li>';
                content += '<div class="info-wrapper" data-tab="info-' + key_feature + '">';
                content += '<table>';
                $.each(feature['properties'], function (key, property) {
                    content += '<tr>';
                    content += '<td>' + key + '</td>';
                    content += '<td>' + property + '</td>';
                    content += '</tr>'
                });
                content += '</table>';
                content += '</div>';
            });
            tabs += '</ul>';
            Shared.Dispatcher.trigger('map:showPopup', coordinate,
                '<div class="info-popup">' + tabs + content + '</div>');
            let infoWrapperTab = $('.info-wrapper-tab');

            infoWrapperTab.click(function () {
                infoWrapperTab.removeClass('active');
                $(this).addClass('active');

                $('.info-wrapper').hide();
                $('.info-wrapper[data-tab="' + $(this).data('tab') + '"]').show();
            });
            if ($('.nav-tabs').innerHeight() > $(infoWrapperTab[0]).innerHeight()) {
                let width = $('.info-popup').width() / infoWrapperTab.length;
                infoWrapperTab.innerWidth(width);
            }
            infoWrapperTab[0].click();
        },

        getLayerAbstract: function (layerKey) {
            let layerProvider = '';
            let layerName = '';
            let layerSourceContainer = $('div.layer-source-info[value="' + layerKey + '"]');
            let fetching = layerSourceContainer.data('fetching');
            if (fetching) {
                if (layerSourceContainer.is(':visible')) {
                    layerSourceContainer.slideUp(200);
                } else {
                    layerSourceContainer.slideDown(200);
                }
                return;
            }
            layerSourceContainer.data('fetching', true);
            layerSourceContainer.html('<div style="width: 100%; height: 50px; text-align: center; padding-top:18px;">Fetching...</div>');
            layerSourceContainer.slideDown(200);

            if (layerKey.indexOf(":") > 0) {
                layerProvider = layerKey.split(":")[0];
                layerName = layerKey.split(":")[1];
            } else {
                layerProvider = layerKey;
                layerName = layerKey;
            }
            let url_provider = layerProvider;
            let url_key = layerName;
            let source = this.layers[layerKey].source
            var abstract_result = "";
        },

    })
});