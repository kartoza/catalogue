define([
    'backbone',
    'underscore',
    'shared',
    'views/map_control_panel',
    'views/side_panel',
    'ol',
    'jquery',
    'layerSwitcher',
    'views/olmap_basemap',
    'collections/paginated',
    'views/olmap_layers',
    'views/search',
    'views/result_grid',
    'models/result_item',
    'htmlToCanvas'
], function (Backbone, _, Shared, MapControlPanelView, SidePanelView,
             ol, $, LayerSwitcher, Basemap, ResultItemCollection, Layers, SearchView, ResultGridView) {
    return Backbone.View.extend({
        template: _.template($('#map-template').html()),
        className: 'map-wrapper',
        id: 'wrapper',
        map: null,
        polygonDraw: null,
        layerSearchSource: null,
        sidePanelView: null,
        searchView: null,
        // attributes
        mapInteractionEnabled: false,
        previousZoom: 0,
        initZoom: 8,
        numInFlightTiles: 0,
        scaleLineControl: null,
        mapIsReady: false,
        polygonDrawn: false,
        initCenter: [22.948492328125, -31.12543669218031],
        events: {
            'click .zoom-in': 'zoomInMap',
            'click .zoom-out': 'zoomOutMap',
            'click .layer-control': 'layerControlClicked',
            'click .print-map-control': 'downloadMap',
            'click .polygonal-lasso-tool': 'drawPolygon',
            'click .close-matadata': 'hideMetadata',
            'click .permalink-control': 'toggleSearchShare',
            'click .delete-polygon': 'deletePolygon',
            'click .sidebarToggle' : 'toggleChange'

        },

        initialize: function () {
            // Ensure methods keep the `this` references to the view itself
            _.bindAll(this, 'render');
            this.layers = new Layers({parent: this});
            this.createPolygonInteraction();
            Shared.CurrentState.FETCH_CLUSTERS = true;
            Shared.Dispatcher.on('layers:addSearch', this.addFeatures, this);
            Shared.Dispatcher.on('layer:focusFeature', this.focusFeature, this);
            Shared.Dispatcher.on('layer:removeFocusFeature', this.removeFocusFeature, this);
            Shared.Dispatcher.on('map:zoomToCoordinates', this.zoomToCoordinates, this);
            Shared.Dispatcher.on('map:drawPoint', this.drawPoint, this);
            Shared.Dispatcher.on('map:clearPoint', this.clearPoint, this);
            Shared.Dispatcher.on('map:zoomToExtent', this.zoomToExtent, this);
            Shared.Dispatcher.on('map:reloadXHR', this.reloadXHR, this);
            Shared.Dispatcher.on('map:addLayer', this.addLayer, this);
            Shared.Dispatcher.on('map:removeLayer', this.removeLayer, this);
            Shared.Dispatcher.on('map:downloadMap', this.downloadMap, this);
            Shared.Dispatcher.on('map:toggleMapInteraction', this.toggleMapInteraction, this);
            Shared.Dispatcher.on('map:setPolygonDrawn', this.setPolygonDrawn, this);

            new ResultGridView({
                'collection': new ResultItemCollection()
            });

            this.render();
            this.pointVectorSource = new ol.source.Vector({});
            this.pointLayer = new ol.layer.Vector({
                source: this.pointVectorSource,
                style: [
                    new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'blue',
                            width: 3
                        }),
                        fill: new ol.style.Fill({
                            color: 'rgba(0, 0, 255, 0.1)'
                        })
                    })]
            });
            this.layerSearchSource = new ol.source.Vector({})
            this.pointLayer.setZIndex(1000);
            this.map.addLayer(this.pointLayer);

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
                ext = ol.proj.transformExtent(coordinates, ol.proj.get('EPSG:4326'), ol.proj.get('EPSG:3857'));
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

        showFeature: function (features, lon, lat, siteExist = false) {
            let featuresClickedResponseData = [];
            const self = this;
            // Point of interest flag
            let poiFound = false;
            let featuresData = '';
            if (features) {
                $.each(features, function (index, feature) {
                    const geometry = feature.getGeometry();
                    const geometryType = geometry.getType();

                    if (geometryType === 'Point') {
                        featuresClickedResponseData = self.featureClicked(
                            feature, self.uploadDataState);
                        poiFound = featuresClickedResponseData[0];
                        featuresData = featuresClickedResponseData[1];
                        self.zoomToCoordinates(geometry.getCoordinates());
                        // increase zoom level if it is clusters
                        if (feature.getProperties()['count'] &&
                            feature.getProperties()['count'] > 1) {
                            self.map.getView().setZoom(self.getCurrentZoom() + 1);
                            poiFound = true;
                        }
                        if (feature.getProperties().hasOwnProperty('features')) {
                            if (feature.getProperties()['features'].length > 0) {
                                poiFound = true;
                            }
                        }
                    }
                });
            }
            if (self.uploadDataState && !poiFound) {
                // Show modal upload if in upload mode
                self.mapControlPanel.showUploadDataModal(lon, lat, featuresData);
            } else if (!self.uploadDataState && !poiFound) {
                // Show feature info
                Shared.Dispatcher.trigger('third_party_layers:showFeatureInfo', lon, lat, siteExist, featuresData);
                Shared.Dispatcher.trigger('layers:showFeatureInfo', lon, lat, siteExist);
            }
        },
        featureClicked: function (feature, uploadDataState) {
            var properties = feature.getProperties();
            if (properties.hasOwnProperty('station')) {
                return [false, feature];
            }

            if (properties.hasOwnProperty('features')) {
                if (properties['features'].length > 1) {

                    this.zoomToCoordinates(
                        feature.getGeometry().getCoordinates(),
                        this.getCurrentZoom() + 2
                    );
                } else {
                    var _properties = properties['features'][0].getProperties();
                    Shared.Dispatcher.trigger('locationSite-' + _properties.id + ':clicked');
                }
            }

            if (!properties.hasOwnProperty('record_type')) {
                return [false, ''];
            }

            if (uploadDataState) {
                return [false, feature];
            }

            if (properties['record_type'] === 'site') {
                Shared.Dispatcher.trigger('locationSite-' + properties.id + ':clicked');
            } else {
                Shared.Dispatcher.trigger('cluster-biology' + properties.id + ':clicked');
            }
            this.layers.highlightVectorSource.clear();
            if (this.layers.layerStyle.isIndividialCluster(feature)) {
                this.addHighlightFeature(feature);
            }
            return [true, properties];
        },
        focusFeature: function( theRecordId ) {
            const self = this
            const highlightStyle = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#3399CC',
                    width: 3,
              }),
            });
            const featureId = this.getFeatureIndexByRecordId( theRecordId );
            const feature = self.layerSearchSource.getFeatureById(featureId);
            feature.setStyle(highlightStyle);

        },

        getFeatureIndexByRecordId: function( theRecordId ) {
            const self = this
            const features = self.layerSearchSource.getFeatures();
            for(let i=0; i < features.length; ++i)
            {
              if(features[i].getProperties()['original_product_id'] == theRecordId)
              {
                return features[i].getId();
              }
            }
        },

        removeFocusFeature: function (theRecordId){
            const self = this
            const featureId = this.getFeatureIndexByRecordId( theRecordId );
            const feature = self.layerSearchSource.getFeatureById(featureId);
            feature.setStyle(new ol.style.Style({
                        stroke: new ol.style.Stroke({ color: '#FFA500' }),
                        fillOpacity: '0'
                    }));
        },

        hidePopup: function () {
            this.popup.setPosition(undefined);
        },
        showPopup: function (coordinates, html) {
            $('#popup').html(html);
            this.popup.setPosition(coordinates);
        },
        layerControlClicked: function (e) {
        },

        getCurrentZoom: function () {
            return this.map.getView().getZoom();
        },
        getCurrentBbox: function () {
            var ext = this.map.getView().calculateExtent(this.map.getSize());
            return ol.proj.transformExtent(ext, ol.proj.get('EPSG:3857'), ol.proj.get('EPSG:4326'));
        },
        createPolygonInteraction: function () {
            let self = this;
            this.source = new ol.source.Vector({wrapX: false});
            this.layer = new ol.layer.Vector({
                source: self.source
            });
            this.polygonDraw = new ol.interaction.Draw({
                source: self.source,
                type: 'Polygon'
            });
            this.polygonDraw.on('drawend', function (evt) {

                // Zoom to extent
                let polygonExtent = evt.feature.getGeometry().getExtent();
                let transformedCoordinates = [];
                let coordinates = evt.feature.getGeometry().getCoordinates()[0];
                for (let i=0; i<coordinates.length; i++) {
                    let newCoord = ol.proj.transform(coordinates[i], ol.proj.get('EPSG:3857'), ol.proj.get('EPSG:4326'));
                    transformedCoordinates.push(newCoord);
                }
                self.polygonCoordinates = transformedCoordinates;
                self.polygonExist = true;
                // Shared.Dispatcher.trigger('map:zoomToExtent', polygonExtent, false, false);
                Shared.Dispatcher.trigger('map:setPolygonDrawn', polygonExtent);

                // show delete polygon
                $('.polygonal-lasso-tool').hide();
                $('.delete-polygon').removeClass('hide-delete-polygon');
            });
            this.polygonDraw.on('drawstart', function () {
                self.source.clear();
            });
        },
        render: function () {
            var self = this;
            this.$el.html(this.template());
            $('#map-container').append(this.$el);

            this.loadMap();

            this.map.on('click', function (e) {
                // self.mapClicked(e);
            });
            this.searchView = new SearchView({
                    parent: this,
            });
            this.sidePanelView = new SidePanelView();
            this.mapControlPanel = new MapControlPanelView({
                parent: this
            });
            $('#layoutSidenav_nav').append(this.searchView.render().$el);
            this.$el.append(this.mapControlPanel.render().$el);
            $('#layoutRightSide').append(this.sidePanelView.render().$el);


            // add layer switcher
            var layerSwitcher = new LayerSwitcher();
            this.map.addControl(layerSwitcher);
            $(layerSwitcher.element).addClass('layer-switcher-custom');
            $(layerSwitcher.element).attr('data-toggle', 'popover');
            $(layerSwitcher.element).attr('data-placement', 'right');
            $(layerSwitcher.element).attr('data-trigger', 'hover');
            $(layerSwitcher.element).attr('data-content', 'Change Basemap');
            $(layerSwitcher.element).removeClass('ol-control');
            $('.layer-switcher-custom').click(function () {
                $(this).popover('hide');
            });
            $('.layer-switcher-custom .panel').mouseenter(function () {
                $('.layer-switcher-custom').popover('disable');
            }).mouseleave(function () {
                $('.layer-switcher-custom').popover('enable');
            });
            this.mapControlPanel.addPanel($(layerSwitcher.element));

            this.map.getLayers().forEach(function (layer) {
                try {
                    var source = layer.getSource();
                    if (source instanceof ol.source.TileImage) {
                        source.on('tileloadstart', function () {
                            ++self.numInFlightTiles
                        });
                        source.on('tileloadend', function () {
                            --self.numInFlightTiles
                        });
                    }
                } catch (err) {
                }
            });

            this.map.on('postrender', function (evt) {
                if (!evt.frameState)
                    return;

                var numHeldTiles = 0;
                var wanted = evt.frameState.wantedTiles;
                for (var layer in wanted)
                    if (wanted.hasOwnProperty(layer))
                        numHeldTiles += Object.keys(wanted[layer]).length;

                var ready = self.numInFlightTiles === 0 && numHeldTiles === 0;
                if (self.mapIsReady !== ready)
                    self.mapIsReady = ready;
            });

            return this;
        },

        loadMap: function () {
            var self = this;
            var mousePositionControl = new ol.control.MousePosition({
                projection: 'EPSG:4326',
                target: document.getElementById('mouse-position-wrapper'),
                coordinateFormat: function (coordinate) {
                    return ol.coordinate.format(coordinate, '{y},{x}', 4);
                }
            });
            var basemap = new Basemap();

            var center = this.initCenter;
            // Add scaleline control
            let scalelineControl = new ol.control.ScaleLine({
                units: 'metric',
                bar: true,
                steps: 4,
                text: true,
                minWidth: 140
            })

            let extent = ['5.207535937500003','-37.72038269917067','47.3950359375','-18.54426493227018'];
            let newExtent = [];
            for (let e=0; e < extent.length; e++) {
                newExtent.push(parseFloat(extent[e]));
            }
            extent = ol.proj.transformExtent(newExtent, 'EPSG:4326', 'EPSG:3857');

            this.map = new ol.Map({
                target: 'map',
                layers: basemap.getBaseMaps(),
                view: new ol.View({
                    center: ol.proj.fromLonLat(center),
                    zoom: this.initZoom,
                    minZoom: 1,
                    maxZoom: 19, // prevent zooming past 50m
                }),
                controls: ol.control.defaults({
                    zoom: false
                }).extend(
                    [
                        mousePositionControl,
                        scalelineControl
                    ])
            });

            this.map.getView().fit(extent);

            // Create a popup overlay which will be used to dispgitlay feature info
            this.popup = new ol.Overlay({
                element: document.getElementById('popup'),
                positioning: 'bottom-center',
                offset: [0, -10]
            });
            this.map.addOverlay(this.popup);
            // this.layers.addLayersToMap(this.map);
            this.initExtent = this.getCurrentBbox();
        },
        removeLayer: function (layer) {
            this.map.removeLayer(layer);
        },
        addLayer: function (layer) {
            this.map.addLayer(layer);
        },
        reloadXHR: function () {
            this.previousZoom = -1;
            this.clusterCollection.administrative = null;
            this.fetchingRecords();
            $('#fetching-error .call-administrator').show();
        },

        switchHighlight: function (features, ignoreZoom) {
            var self = this;
            this.closeHighlight();
            $.each(features, function (index, feature) {
                self.addHighlightFeature(feature);
            });
            if (!ignoreZoom) {
                var extent = this.layers.highlightVectorSource.getExtent();
                this.map.getView().fit(extent, {
                    size: this.map.getSize(), padding: [
                        0, $('.right-panel').width(), 0, 250
                    ]
                });
                if (this.getCurrentZoom() > 8) {
                    this.map.getView().setZoom(8);
                }
            }
        },

        addFeatures: function(features){
            const self = this
            self.layerSearchSource.clear();
            _.each(features, function (feature) {
                const format = new ol.format.WKT();
                const feat = format.readFeature(feature.attributes['spatial_coverage'], {
                    dataProjection: 'EPSG:4326',
                    featureProjection: 'EPSG:3857',
                });
                feat.setProperties(feature.attributes)
                feat.setId(feature.attributes['id'])
                const exist = new ResultItemCollection().filter(function (item) {
                    return item.get("product").id == feature.attributes.id;
                });

                //if item is in cart, color green else orange
                if (exist.length > 0) {
                  feat.setStyle(new ol.style.Style({
                        stroke: new ol.style.Stroke({ color: '#5bb75b' }),
                        fillOpacity: '0.5'
                    })
                  );
                } else {
                    feat.setStyle(new ol.style.Style({
                        stroke: new ol.style.Stroke({ color: '#FFA500' }),
                        fillOpacity: '0'
                    }));
                }

                self.layerSearchSource.addFeatures([feat]);

              });
            const layerSearchVector = new ol.layer.Vector({
                className: 'search-result',
                source: self.layerSearchSource,
                style: function (feature) {
                    const geom = feature.getGeometry();
                    return self.layerStyle.getPinnedHighlightStyle(geom.getType());
                    }
            });
            this.map.addLayer(layerSearchVector)
        },

        downloadMap: function () {
            var that = this;
            var downloadMap = true;
            that.map.once('rendercomplete', function () {
                const mapCanvas = document.createElement('canvas');
                const size = that.map.getSize();
                mapCanvas.width = size[0];
                mapCanvas.height = size[1];
                const mapContext = mapCanvas.getContext('2d');
                Array.prototype.forEach.call(
                    that.map.getViewport().querySelectorAll('.ol-layer canvas, .search-result canvas'),
                    function (canvas) {
                        if (canvas.width > 0) {
                            const opacity = canvas.parentNode.style.opacity || canvas.style.opacity;
                            mapContext.globalAlpha = opacity === '' ? 1 : Number(opacity);
                            const backgroundColor = canvas.parentNode.style.backgroundColor;
                            if (backgroundColor) {
                                mapContext.fillStyle = backgroundColor;
                                mapContext.fillRect(0, 0, canvas.width, canvas.height);
                            }
                            let matrix;
                            const transform = canvas.style.transform;
                            if (transform) {
                                // Get the transform parameters from the style's transform matrix
                                matrix = transform.match(/^matrix\(([^\(]*)\)$/)[1].split(',').map(Number);
                            } else {
                                matrix = [
                                    parseFloat(canvas.style.width) / canvas.width, 0, 0,
                                    parseFloat(canvas.style.height) / canvas.height,
                                    0,
                                    0,
                                ];
                            }
                            // Apply the transform to the export map context
                            CanvasRenderingContext2D.prototype.setTransform.apply(
                                mapContext,
                                matrix
                            );
                            mapContext.drawImage(canvas, 0, 0);
                        }
                    }
                    );
                mapContext.globalAlpha = 1;
                if (navigator.msSaveBlob) {
                  // link download attribute does not work on MS browsers
                  navigator.msSaveBlob(mapCanvas.msToBlob(), 'map.png');
                } else {
                  const link = document.getElementById('image-download');
                  link.href = mapCanvas.toDataURL();
                  link.click();
                                        
                }
              });
                that.map.renderSync();

        },
        drawPolygon: function () {

            this.map.removeLayer(this.layer);
            this.map.addLayer(this.layer);
            this.map.addInteraction(this.polygonDraw);
            Shared.Dispatcher.trigger('map:toggleMapInteraction', true);
        },
        stopDrawing: function () {

            this.map.removeInteraction(this.polygonDraw);
            Shared.Dispatcher.trigger('map:toggleMapInteraction', false);
        },
        hideMetadata: function (event){
            $("#product-metadata").hide()

        },

        toggleSearchShare: function() {

            const permalink =  $('#permalink-control');
            if (permalink.hasClass('permalink-disabled')) {
                return;
            }
            const textArea = document.createElement("textarea");
            textArea.value = window.location.origin +'/search/'+ guid + '/';
            document.body.insertBefore(textArea, document.body.firstChild);
            textArea.focus();
            textArea.select();

            try {
                const successful = document.execCommand('copy');
                permalink.attr('data-bs-content', 'Permalink copied to your clipboard');
            } catch (err) {
                permalink.attr('data-bs-content', 'Unable to copy');
            }
            permalink.popover('show');
            document.body.removeChild(textArea);

        },

        deletePolygon: function (){
            this.map.removeLayer(this.layer);
            this.source.clear();
            $('.polygonal-lasso-tool').show();
                $('.delete-polygon').addClass('hide-delete-polygon');
            this.stopDrawing();
            Shared.Dispatcher.trigger('map:setPolygonDrawn', null);
        },

        toggleChange: function (){
           const sidebar = $('#sidebarToggle');
           const sidenav = $('#layoutSidenav_nav');
           if (sidebar.attr('data-bs-content')=="Hide parameters"){
               sidebar.attr('data-bs-content', 'Show parameters');
               sidenav.css('margin','0');
               sidebar.children('i').removeClass('fa-compress');
               sidebar.children('i').addClass('fa-expand');
           }
           else{
               sidebar.attr('data-bs-content', 'Hide parameters');
               sidenav.css('margin','0.5rem');
               sidebar.children('i').removeClass('fa-expand');
               sidebar.children('i').addClass('fa-compress');
           }
        }
    })
});
