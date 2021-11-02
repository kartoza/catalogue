define(['backbone', 'underscore', 'jquery', 'ol', 'olMapboxStyle'], function (Backbone, _, $, ol, OlMapboxStyle) {
    return Backbone.View.extend({
        getVectorTileMapBoxStyle: function (url, styleUrl, layerName, attributions) {
            let tileGrid = ol.tilegrid.createXYZ({tileSize: 512, maxZoom: 14});
            let layer = new ol.layer.VectorTile({
                source: new ol.source.VectorTile({
                    attributions: attributions,
                    format: new ol.format.MVT(),
                    tileGrid: tileGrid,
                    tilePixelRatio: 8,
                    url: url
                })
            });
            if (styleUrl) {
                fetch(styleUrl).then(function (response) {
                    response.json().then(function (glStyle) {
                        OlMapboxStyle.applyStyle(layer, glStyle, layerName).then(function () {
                        });
                    });
                });
            }
            return layer;
        },
        getOpenMapTilesTile: function (styleUrl, attributions) {
            if (!attributions) {
                attributions = '© <a href="https://openmaptiles.org/">OpenMapTiles</a> ' +
                    '© <a href="http://www.openstreetmap.org/copyright">' +
                    'OpenStreetMap contributors</a>';
            }
            return this.getVectorTileMapBoxStyle(
                '/https://api.maptiler.com/tiles/v3/{z}/{x}/{y}.pbf?key=' + mapTilerKey,
                styleUrl,
                'openmaptiles',
                attributions
            );
        },

        getBaseMaps: function () {
            var baseSourceLayers = [];
            let toposheet = new ol.layer.Tile({
                title: 'Topography',
                type: 'base',
                visible: true,
                source: new ol.source.XYZ({
                    attributions: ['Kartendaten: © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>-Mitwirkende, SRTM | Kartendarstellung: © <a href="http://opentopomap.org/">OpenTopoMap</a> ' +
                    '<a href="https://creativecommons.org/licenses/by-sa/3.0/">(CC-BY-SA)</a>'],
                    url: 'https://a.tile.opentopomap.org/{z}/{x}/{y}.png'
                })
            });

            // OSM
            let osm = new ol.layer.Tile({
                title: 'OpenStreetMap',
                source: new ol.source.OSM()
            });
            baseSourceLayers.push(osm);

            baseSourceLayers.push(toposheet);
            // baseSourceLayers.push(this.getKartozaBaseMap());

            let defaultLayer = null;
            let defaultLayerIndex = null;

            $.each(baseSourceLayers, function (index, layer) {
                let properties = layer.getProperties();
                let title = properties['title'];
                layer.set('type', 'base');
                layer.set('visible', true);
                layer.set('preload', Infinity);
                if (title === defaultBasemap) {
                    defaultLayer = layer;
                    defaultLayerIndex = index;
                }
            });

            if (defaultLayer) {
                baseSourceLayers.splice(defaultLayerIndex, 1);
                baseSourceLayers.push(defaultLayer);
            }

            let _baseMapLayers = [];
            if (_baseMapLayers.length === 0) {
                _baseMapLayers.push(
                    new ol.layer.Tile({
                        title: 'OpenStreetMap',
                        type: 'base',
                        visible: true,
                        source: new ol.source.OSM()
                    })
                )
            }
            return _baseMapLayers
        }
    })
});
