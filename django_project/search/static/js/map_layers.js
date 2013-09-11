var WMS_SERVER = 'maps.sansa.org.za';

WEB_LAYERS = {}
// Streets and boundaries for SA base map with an
// underlay of spot 2010 2m mosaic
//
// Uses the degraded 2.5m product in a tile cache
//
// and under that blue marble. Its rendered as a single
// layer for best quality.
WEB_LAYERS.zaSpot2mMosaic2010TC = new OpenLayers.Layer.WMS(
  '2m Mosaic 2010 TC', 'http://'+ WMS_SERVER + '/cgi-bin/tilecache.cgi?',
{
 VERSION: '1.1.1',
 EXCEPTIONS: 'application/vnd.ogc.se_inimage',
 width: '800',
 layers: 'spot5mosaic2m2010',
 maxResolution: '156543.0339',
 srs: 'EPSG:900913',
 height: '525',
 format: 'image/jpeg',
 transparent: 'false',
 antialiasing: 'true'
},
{isBaseLayer: true});

// Streets and boundaries for SA base map with an underlay
// of spot 2009 2m mosaic
//
// Uses the degraded 2.5m product in a tile cache
//
// and under that blue marble. Its rendered as a single layer
// for best quality.
WEB_LAYERS.zaSpot2mMosaic2009TC = new OpenLayers.Layer.WMS(
    '2m Mosaic 2009 TC', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
{
   VERSION: '1.1.1',
   EXCEPTIONS: 'application/vnd.ogc.se_inimage',
   width: '800',
   //layers: 'Roads',
   layers: 'spot5mosaic2m2009',
   maxResolution: '156543.0339',
   srs: 'EPSG:900913',
   height: '525',
   format: 'image/jpeg',
   transparent: 'false',
   antialiasing: 'true'
 },
 {isBaseLayer: true});

// Streets and boundaries for SA base map with an underlay
// of spot 2008 mosaic. Uses the degraded 2m product in a tile cache
// and under that blue marble. Its rendered as a single layer for
// best quality.
WEB_LAYERS.zaSpot2mMosaic2008TC = new OpenLayers.Layer.WMS(
    '2m Mosaic 2008 TC', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
{
   VERSION: '1.1.1',
   EXCEPTIONS: 'application/vnd.ogc.se_inimage',
   width: '800',
   layers: 'spot5mosaic2m2008',
   maxResolution: '156543.0339',
   srs: 'EPSG:900913',
   height: '525',
   format: 'image/jpeg',
   transparent: 'false',
   antialiasing: 'true'
 },
 {isBaseLayer: true});

// Streets and boundaries for SA base map with an underlay of spot
// 2007 mosaic. Uses the degraded 2m product in a tile cache
// and under that blue marble. Its rendered as a single layer
// for best quality.
WEB_LAYERS.zaSpot2mMosaic2007TC = new OpenLayers.Layer.WMS(
  '2m Mosaic 2007 TC', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
{
   VERSION: '1.1.1',
   EXCEPTIONS: 'application/vnd.ogc.se_inimage',
   width: '800',
   layers: 'spot5mosaic2m2007',
   srs: 'EPSG:900913',
   maxResolution: '156543.0339',
   height: '525',
   format: 'image/jpeg',
   transparent: 'false',
   antialiasing: 'true'
 },
 {isBaseLayer: true});

// Streets and boundaries for SA base map with an underlay of spot
// 2010 mosaic and under that blue marble. Its rendered as a single
// layer for best quality.
WEB_LAYERS.zaSpot2mMosaic2010 = new OpenLayers.Layer.WMS(
    '2m Mosaic 2010', 'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=ZA_SPOT2010',
{
   VERSION: '1.1.1',
   EXCEPTIONS: 'application/vnd.ogc.se_inimage',
   width: '800',
   layers: 'Roads',
   srs: 'EPSG:900913',
   maxResolution: '156543.0339',
   height: '525',
   format: 'image/jpeg',
   transparent: 'false',
   antialiasing: 'true'
 },
 {isBaseLayer: true});

 // Streets and boundaries for SA base map with an underlay of
 // spot 2009 mosaic and under that blue marble. Its rendered as a
 // single layer for best quality.
 WEB_LAYERS.zaSpot2mMosaic2009 = new OpenLayers.Layer.WMS(
     '2m Mosaic 2009', 'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=ZA_SPOT2009',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'Roads',
  srs: 'EPSG:900913',
  maxResolution: '156543.0339',
  height: '525',
  format: 'image/jpeg',
  transparent: 'false',
  antialiasing: 'true'
},
{isBaseLayer: true});

// Streets and boundaries for SA base map with an underlay of spot
// 2008 mosaic and under that blue marble. Its rendered as a single
// layer for best quality.
WEB_LAYERS.zaSpot2mMosaic2008 = new OpenLayers.Layer.WMS(
    '2m Mosaic 2008', 'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=ZA_SPOT2008',
{
   width: '800',
   layers: 'Roads',
   srs: 'EPSG:900913',
   maxResolution: '156543.0339',
   VERSION: '1.1.1',
   EXCEPTIONS: 'application/vnd.ogc.se_inimage',
   height: '525',
   format: 'image/jpeg',
   transparent: 'false',
   antialiasing: 'true'
 },
 {isBaseLayer: true});

// Streets and boundaries for SA base map with an underlay of spot
// 2007 mosaic and under that blue marble. Its rendered as a single
// layer for best quality.
WEB_LAYERS.zaSpot2mMosaic2007 = new OpenLayers.Layer.WMS(
   '2m Mosaic 2007', 'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=ZA_SPOT2007',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'Roads',
  srs: 'EPSG:900913',
  maxResolution: '156543.0339',
  height: '525',
  format: 'image/jpeg',
  transparent: 'false',
  antialiasing: 'true'
},
{isBaseLayer: true});

 // Streets and boundaries for SA base map with an underlay of
 // spot 2010 mosaic. Uses the degraded 10m product in a tile cache
 // and under that blue marble. Its rendered as a single layer for
 // best quality.
WEB_LAYERS.zaSpot10mMosaic2010 = new OpenLayers.Layer.WMS(
   '10m Mosaic 2010 TC', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'spot5mosaic10m2010',
  maxResolution: '156543.0339',
  srs: 'EPSG:900913',
  height: '525',
  format: 'image/jpeg',
  transparent: 'false',
  antialiasing: 'true'
},
{isBaseLayer: true});

 // Streets and boundaries for SA base map with an underlay of spot
 // 2009 mosaic. Uses the degraded 10m product in a tile cache
 //
 // and under that blue marble. Its rendered as a single layer for
 // best quality.
WEB_LAYERS.zaSpot10mMosaic2009 = new OpenLayers.Layer.WMS(
   '10m Mosaic 2009 TC', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'spot5mosaic10m2009',
  maxResolution: '156543.0339',
  srs: 'EPSG:900913',
  height: '525',
  format: 'image/jpeg',
  transparent: 'false',
  antialiasing: 'true'
},
{isBaseLayer: true});

 // Streets and boundaries for SA base map with an underlay of
 // spot 2008 mosaic
 //
 // Uses the degraded 10 product in a tile cache
 //
 // and under that blue marble. Its rendered as a single layer for
 // best quality.
WEB_LAYERS.zaSpot10mMosaic2008 = new OpenLayers.Layer.WMS(
   '10m Mosaic 2008 TC', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'spot5mosaic10m2008',
  maxResolution: '156543.0339',
  srs: 'EPSG:900913',
  height: '525',
  format: 'image/jpeg',
  transparent: 'false',
  antialiasing: 'true'
},
{isBaseLayer: true});

 // Streets and boundaries for SA base map with an underlay of spot
 // 2007 mosaic
 //
 // Uses the degraded 10 product in a tile cache
 //
 // and under that blue marble. Its rendered as a single layer for
 // best quality.
WEB_LAYERS.zaSpot10mMosaic2007 = new OpenLayers.Layer.WMS(
   '10m Mosaic 2007 TC', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'spot5mosaic10m2007',
  srs: 'EPSG:900913',
  maxResolution: '156543.0339',
  height: '525',
  format: 'image/jpeg',
  transparent: 'false',
  antialiasing: 'true'
},
{isBaseLayer: true});

// Spot5 ZA 2008 10m Mosaic directly from mapserver
WEB_LAYERS.zaSpot5Mosaic2008 = new OpenLayers.Layer.WMS(
     'SPOT5 10m Mosaic 2008, ZA',
     'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=ZA_SPOT',
 {
   VERSION: '1.1.1',
   EXCEPTIONS: 'application/vnd.ogc.se_inimage',
   layers: 'Spot5_RSA_2008_10m',
   maxResolution: '156543.0339',
 });
 WEB_LAYERS.zaSpot5Mosaic2008.setVisibility(false);

//a Vector only version of the above
WEB_LAYERS.zaRoadsBoundaries = new OpenLayers.Layer.WMS(
    'SA Vector', 'http://' + WMS_SERVER + '/cgi-bin/tilecache.cgi?',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'za_vector',
  srs: 'EPSG:900913',
  maxResolution: '156543.0339',
  height: '525',
  format: 'image/jpeg',
  transparent: 'false',
  antialiasing: 'true'
},
{isBaseLayer: true});

 // Map of all search footprints that have been made.
 // Transparent: true will make a wms layer into an overlay
 WEB_LAYERS.searches = new OpenLayers.Layer.WMS(
     'Searches', 'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=SEARCHES',
          {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'searches',
  srs: 'EPSG:900913',
  maxResolution: '156543.0339',
  height: '525',
  format: 'image/png',
  transparent: 'true'
},
{isBaseLayer: false});

// Map of site visitors
// Transparent: true will make a wms layer into an overlay
WEB_LAYERS.visitors = new OpenLayers.Layer.WMS(
  'Visitors', 'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=VISITORS',
{
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  width: '800',
  layers: 'visitors',
  styles: '',
  srs: 'EPSG:900913',
  maxResolution: '156543.0339',
  height: '525',
  format: 'image/png',
  transparent: 'true'
},
{isBaseLayer: false}
       );

        // Nasa Blue marble directly from mapserver
WEB_LAYERS.BlueMarble = new OpenLayers.Layer.WMS('BlueMarble',
     'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=WORLD',
 {
  VERSION: '1.1.1',
  EXCEPTIONS: 'application/vnd.ogc.se_inimage',
  layers: 'BlueMarble',
  maxResolution: '156543.0339'
 });
 WEB_LAYERS.BlueMarble.setVisibility(false);

// //
// // Google
// //
// WEB_LAYERS.GooglePhysical = new OpenLayers.Layer.Google(
// 'Google Physical',
// {type: G_PHYSICAL_MAP}
//           );

// //
// // Google streets
// //
// WEB_LAYERS.GoogleStreets = new OpenLayers.Layer.Google(
// 'Google Streets' // the default
//           );

// //
// // Google hybrid
// //
// WEB_LAYERS.GoogleHybrid = new OpenLayers.Layer.Google(
// 'Google Hybrid',
// {type: G_HYBRID_MAP}
//           );

// //
// // Google Satellite
// //
// WEB_LAYERS.GoogleSatellite = new OpenLayers.Layer.Google(
// 'Google Satellite',
// {type: G_SATELLITE_MAP}
//           );

//
// Heatmap - all
//
WEB_LAYERS.Heatmap_total = new OpenLayers.Layer.Image(
     'Heatmap total',
     '/media/heatmaps/heatmap-total.png',
     new OpenLayers.Bounds(-20037508.343,
     -16222639.241,
     20019734.329,
     16213801.068),
     new OpenLayers.Size(1252,1013),
     {isBaseLayer: true,
     maxResolution: 156543.0339
     }
);

//
// Heatmap - last3month
//
WEB_LAYERS.Heatmap_last3month = new OpenLayers.Layer.Image(
     'Heatmap last 3 months',
     '/media/heatmaps/heatmap-last3month.png',
     new OpenLayers.Bounds(-20037508.343,
     -16222639.241,
     20019734.329,
     16213801.068),
     new OpenLayers.Size(1252,1013),
     {isBaseLayer: true,
     maxResolution: 156543.0339
     }
);

//
// Heatmap - last month
//
 WEB_LAYERS.Heatmap_lastmonth = new OpenLayers.Layer.Image(
     'Heatmap last month',
     '/media/heatmaps/heatmap-lastmonth.png',
     new OpenLayers.Bounds(-20037508.343,
     -16222639.241,
     20019734.329,
     16213801.068),
     new OpenLayers.Size(1252,1013),
     {isBaseLayer: true,
     maxResolution: 156543.0339
     }
);

//
// Heatmap - last week
//
WEB_LAYERS.Heatmap_lastweek = new OpenLayers.Layer.Image(
     'Heatmap last week',
     '/media/heatmaps/heatmap-lastweek.png',
     new OpenLayers.Bounds(-20037508.343,
     -16222639.241,
     20019734.329,
     16213801.068),
     new OpenLayers.Size(1252,1013),
     {isBaseLayer: true,
     maxResolution: 156543.0339
     }
);

// Note for this layer to be used you need to regex replace
// USERNAME with theRequest.user.username
// WEB_LAYERS.CartLayer = new OpenLayers.Layer.WMS('Cart', 'http://' +
//  WMS_SERVER + '/cgi-bin/mapserv?map=' +
//  settings.CART_LAYER + '&user=USERNAME',
//           {
//   version: '1.1.1',
//   width: '800',
//   layers: 'Cart',
//   srs: 'EPSG:4326',
//   height: '525',
//   format: 'image/png',
//   transparent: 'true'
// },
// {isBaseLayer: false});