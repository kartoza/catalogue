define(['backbone', 'underscore', 'jquery', 'ol'], function (Backbone, _, $, ol) {
    return Backbone.View.extend({

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
                type: 'base',
                visible: true,
                source: new ol.source.OSM()
            })

            // Stamen
            let stamen = new ol.layer.Tile({
                title: 'Tone',
                type: 'base',
                visible: true,
                source: new ol.source.Stamen({
                    layer: 'toner'
                })
            })

            baseSourceLayers.push(toposheet);
            baseSourceLayers.push(stamen);
            baseSourceLayers.push(osm);

            return baseSourceLayers
        }
    })
});
