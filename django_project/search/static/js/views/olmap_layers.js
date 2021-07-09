define(['shared', 'backbone', 'underscore', 'jquery', 'jqueryUi', 'jqueryTouch', 'ol', 'views/layer_style'], function (Shared, Backbone, _, $, jqueryUI, jqueryTouch, ol, LayerStyle) {
    return Backbone.View.extend({
        // source of layers
        locationSiteCluster: null,
        locationSiteClusterLayer: null,
        locationSiteClusterSource: null,
        highlightVectorSource: null,
        highlightVector: null,
        highlightPinnedVectorSource: null,
        highlightPinnedVector: null,
        administrativeLayerGroup: null,
        layers: {},
        initialLoadBiodiversityLayersToMap: false,
        orders: {},
        layerSelector: null,
        initialize: function () {
            this.layerStyle = new LayerStyle();
            Shared.Dispatcher.on('layers:showFeatureInfo', this.showFeatureInfo, this);
            Shared.Dispatcher.on('layers:renderLegend', this.renderLegend, this);
            var administrativeVisibility = Shared.StorageUtil.getItemDict('Administrative', 'transparency');
            if (administrativeVisibility !== null) {
                this.administrativeTransparency = administrativeVisibility;
            }
        },
        isBiodiversityLayerLoaded: function () {
            return true;
        },
        isAdministrativeLayerSelected: function () {
            var $checkbox = $('.layer-selector-input[value="Administrative"]');
            if ($checkbox.length === 0) {
                return true
            }
            return $checkbox.is(':checked');
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
            if (layerName.indexOf(this.administrativeKeyword) >= 0) {
                layerType = layerName;
            }
            if (layerName === 'Sites') {
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
        // addBiodiveristyLayersToMap: function (map) {
        //     var self = this;
        //     // ---------------------------------
        //     // HIGHLIGHT PINNED LAYER
        //     // ---------------------------------
        //     self.highlightPinnedVectorSource = new ol.source.Vector({});
        //     self.highlightPinnedVector = new ol.layer.Vector({
        //         source: self.highlightPinnedVectorSource,
        //         style: function (feature) {
        //             var geom = feature.getGeometry();
        //             return self.layerStyle.getPinnedHighlightStyle(geom.getType());
        //         }
        //     });
        //     map.addLayer(self.highlightPinnedVector);
        //
        //     // ---------------------------------
        //     // HIGHLIGHT LAYER -- MARKER
        //     // ---------------------------------
        //     self.highlightVectorSource = new ol.source.Vector();
        //     self.highlightVector = new ol.layer.Vector({
        //         source: self.highlightVectorSource,
        //         style: function (feature) {
        //             var geom = feature.getGeometry();
        //             return self.layerStyle.getHighlightStyle(geom.getType());
        //         }
        //     });
        //     map.addLayer(self.highlightVector);
        //
        //     // ---------------------------------
        //     // BIODIVERSITY LAYERS
        //     // ---------------------------------
        //
        //     // self.biodiversitySource = new ol.source.ImageWMS(biodiversityLayersOptions);
        //     // self.biodiversityTileLayer = new ol.layer.Image({
        //     //     source: self.biodiversitySource
        //     // });
        //     self.initLayer(
        //         self.biodiversityTileLayer,
        //         'Sites',
        //         true,
        //     );
        //
        //     if (!self.initialLoadBiodiversityLayersToMap) {
        //         self.initialLoadBiodiversityLayersToMap = true;
        //     }
        // },

        addLayersToMap: function (map) {
            var self = this;
            this.map = map;

            var biodiversityOrder = Shared.StorageUtil.getItemDict('Sites', 'order');
            if (biodiversityOrder === null) {
                biodiversityOrder = 0;
            }
            self.orders[0] = 'Sites';
            // self.addBiodiveristyLayersToMap(map);
            self.renderLayers(false);
        },
        
        changeLayerVisibility: function (layerName, visible) {
            if (Object.keys(this.layers).length === 0) {
                return false;
            }
            this.layers[layerName]['layer'].setVisible(visible);
        },
        changeLayerTransparency: function (layername, opacity) {
            if (Object.keys(this.layers).length === 0) {
                return false;
            }
            this.layers[layername]['layer'].setOpacity(opacity);
        },
        selectorChanged: function (layerName, selected) {
            Shared.StorageUtil.setItemDict(layerName, 'selected', selected);
            this.changeLayerVisibility(layerName, selected);
            var needToReloadXHR = true;
            this.toggleLegend(layerName, selected, needToReloadXHR);
        },
        toggleLegend: function (layerName, selected, reloadXHR) {
            // show/hide legend
            var $legendElement = this.getLegendElement(layerName);
            if (layerName === 'Sites' && this.isBiodiversityLayerLoaded()) {
                if (reloadXHR) {
                    Shared.Dispatcher.trigger('map:reloadXHR');
                }
                if (selected) {
                    Shared.Dispatcher.trigger('biodiversityLegend:show');
                } else {
                    Shared.Dispatcher.trigger('biodiversityLegend:hide');
                }
            }

            if (selected) {
                if ($legendElement.length > 0) {
                    $legendElement.show();
                    let legendDisplayed = Shared.StorageUtil.getItem('legendsDisplayed');
                    if (legendDisplayed !== false || typeof legendDisplayed === 'undefined') {
                        Shared.Dispatcher.trigger('map:showMapLegends');
                    }
                }
            } else {
                $legendElement.hide();
            }
        },
        ol3_checkLayer: function (layer) {
            var res = false;
            for (var i = 0; i < this.map.getLayers().getLength(); i++) {
                //check if layer exists
                if (this.map.getLayers().getArray()[i] === layer) {
                    //if exists, return true
                    res = true;
                }
            }
            return res;
        },
        moveLayerToTop: function (layer) {
            if (layer) {
                if (this.ol3_checkLayer(layer)) {
                    this.map.removeLayer(layer);
                    this.map.getLayers().insertAt(this.map.getLayers().getLength(), layer);
                } else {
                    console.log('not found')
                }
            }
        },
        moveLegendToTop: function (layerName) {
            this.getLegendElement(layerName).detach().prependTo('#map-legend');
        },
        getLegendElement: function (layerName) {
            return $(".control-drop-shadow").find(
                "[data-name='" + layerName + "']");
        },

        renderTransparencySlider: function () {
            var self = this;
            var layerDivs = $('#layers-selector').find('.layer-transparency');
            $.each(layerDivs, function (key, layerDiv) {
                $(layerDiv).slider({
                    range: 'max',
                    min: 1,
                    max: 100,
                    value: $(layerDiv).data('value'),
                    slide: function (event, ui) {
                        var $label = $(event.target).closest('li').find('.layer-selector-input');
                        var layername = 'Sites';
                        if ($label.length > 0) {
                            layername = $label.val();
                        }
                        self.changeLayerTransparency(layername, ui.value / 100);
                    },
                    stop: function (event, ui) {
                        var $label = $(event.target).closest('li').find('.layer-selector-input');
                        var layername = 'Sites';
                        if ($label.length > 0) {
                            layername = $label.val();
                        }
                        Shared.StorageUtil.setItemDict(layername, 'transparency', ui.value / 100);
                        if (layername.indexOf(self.administrativeKeyword) >= 0) {
                            self.administrativeTransparency = ui.value / 100;
                        }
                    }
                });
            });
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

                if (layerName.indexOf(self.administrativeKeyword) >= 0) {
                    var administrativeVisibility = Shared.StorageUtil.getItem('Administrative');
                    if (administrativeVisibility === null) {
                        administrativeVisibility = true;
                    } else {
                        if (administrativeVisibility.hasOwnProperty('selected')) {
                            administrativeVisibility = administrativeVisibility['selected'];
                        }
                    }
                    defaultVisibility = administrativeVisibility;
                    source = 'Base';
                }

                self.renderLayersSelector(key, layerName, defaultVisibility, currentLayerTransparency, category, source, isFirstTime);
            });

            // RENDER LAYERS
            $.each(self.layers, function (key, value) {
                let _layer = value['layer'];
                if (!_layer.get('added')) {
                    _layer.set('added', true);
                    self.map.addLayer(_layer);
                }
            });
            self.renderTransparencySlider();

            $('.layer-selector-input').change(function (e) {
                self.selectorChanged($(e.target).val(), $(e.target).is(':checked'))
            });
            if (isFirstTime) {
                self.initializeLayerSelector();
            }
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
                if (layerName.indexOf(that.administrativeKeyword) >= 0) {
                    layerName = that.administrativeKeyword;
                    key_feature = 'administrative';
                }
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
        showLayerSource: function (layerKey) {
            if (Object.keys(this.layers).length === 0) {
                return false;
            } else if (layerKey !== this.administrativeKeyword) {
                this.getLayerAbstract(layerKey);
            }
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
        initializeLayerSelector: function () {
            let self = this;
            this.layerSelector = $('#layers-selector');
            this.layerSelector.sortable({cancel: '.layer-abstract'});
            this.layerSelector.on('sortupdate', function () {
                let $layerSelectorInput = $('.layer-selector-input');
                $($layerSelectorInput.get().reverse()).each(function (index, value) {
                    let layerName = $(value).val();
                    self.moveLayerToTop(self.layers[layerName]['layer']);
                    self.moveLegendToTop(layerName);
                });
                self.moveLayerToTop(self.highlightPinnedVector);
                self.moveLayerToTop(self.highlightVector);

                // Update saved order
                $($layerSelectorInput.get()).each(function (index, value) {
                    let layerName = $(value).val();
                    Shared.StorageUtil.setItemDict(layerName, 'order', parseInt(index));
                });
            });
        },
        changeLayerOder: function (layerName, order) {
            let $layerElm = $('.layer-selector-input[value="' + layerName + '"]').parent().parent();
            let $layerSelectorList = $('#layers-selector li');
            if (order > $layerSelectorList.length - 1) {
                order = $layerSelectorList.length - 1;
            }
            if (order <= 0) {
                $layerElm.insertBefore($layerSelectorList.get(0));
            } else {
                $layerElm.insertAfter($layerSelectorList.get(order - 1));
            }
        },
        refreshLayerOrders: function () {
            let self = this;
            let $layerSelectorInput = $('.layer-selector-input');
            $($layerSelectorInput.get()).each(function (index, value) {
                let layerName = $(value).val();
                let order = Shared.StorageUtil.getItemDict(layerName, 'order');
                if (order != null) {
                    self.changeLayerOder(layerName, order);
                }
            });
            self.layerSelector.trigger('sortupdate');
        }
    })
});