var map = new OpenLayers.Map( 'map', {controls: []});
var SearchPanelState = true;
var CartPanelState = false;
var ResultPanelState = false;

function initMap() {
    var layer = new OpenLayers.Layer.OSM( "Simple OSM Map");
    map.addLayer(layer);
    map.setCenter(
        new OpenLayers.LonLat(-71.147, 42.472).transform(
            new OpenLayers.Projection("EPSG:4326"),
            map.getProjectionObject()
        ), 12
    );
}

function toggleSearchPanel() {
    if (SearchPanelState) {
        $("#search-panel").animate({left: -300}, 300 );
        SearchPanelState = false;
        $("#cart-panel-toggle").animate({top: 145}, 200 );
    } else {
        if (CartPanelState) {
            closeCartPanel();
        }
        $("#search-panel").animate({left: 10}, 300 );
        SearchPanelState = true;
        $("#cart-panel-toggle").animate({top: 515}, 200 );
    }
}

function closeSearchPanel() {
    $("#search-panel").animate({left: -300}, 300 );
    SearchPanelState = false;
    $("#cart-panel-toggle").animate({top: 145}, 200 );
}

function toggleCartPanel() {
    if (CartPanelState) {
        $("#cart-panel").animate({left: -300}, 300 );
        CartPanelState = false;
        $("#cart-panel-toggle").animate({top: 145}, 200 );
        $("#search-panel-toggle").animate({top: 25}, 200 );
    } else {
        if (SearchPanelState) {
            closeSearchPanel();
        }
        $("#cart-panel").animate({left: 10}, 300 );
        CartPanelState = true;
        $("#cart-panel-toggle").animate({top: 0}, 200 );
        $("#search-panel-toggle").animate({top: 515}, 200 );
    }
}

function closeCartPanel() {
    $("#cart-panel").animate({left: -300}, 300 );
    CartPanelState = false;
    $("#search-panel-toggle").animate({top: 25}, 200 );
}

function toggleResultPanel() {
    if (ResultPanelState) {
        $("#result-panel").animate({right: -300}, 300 );
        ResultPanelState = false;
    } else {
        $("#result-panel").animate({right: 10}, 300 );
        ResultPanelState = true;
    }
}

function defaultPanelState() {
    if (SearchPanelState) {
        $("#search-panel").animate({left: 10}, 300 );
        SearchPanelState = true;
        $("#cart-panel-toggle").animate({top: 515}, 200 );
    } else if (CartPanelState) {
        $("#cart-panel").animate({left: 10}, 300 );
        $("#cart-panel-toggle").animate({top: 0}, 200 );
        $("#search-panel-toggle").animate({top: 515}, 200 );
    }
    if (ResultPanelState) {
        $("#result-panel").animate({right: 10}, 300 );
    }
}