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
        hideSearchPanelButtons();
        $("#search-panel").animate({left: -450}, 300 );
        SearchPanelState = false;
        $("#cart-panel-toggle").animate({top: 155}, 200 );
    } else {
        if (CartPanelState) {
            closeCartPanel();
        }
        $("#search-panel").animate({left: 10}, 300 );
        showSearchPanelButtons();
        SearchPanelState = true;
        $("#cart-panel-toggle").animate({top: 515}, 200 );
    }
}

function closeSearchPanel() {
    hideSearchPanelButtons();
    $("#search-panel").animate({left: -450}, 300 );
    SearchPanelState = false;
    $("#cart-panel-toggle").animate({top: 155}, 200 );
}

function toggleCartPanel() {
    if (CartPanelState) {
        hideCartPanelButtons();
        $("#cart-panel").animate({left: -450}, 300 );
        CartPanelState = false;
        $("#cart-panel-toggle").animate({top: 155}, 200 );
        $("#search-panel-toggle").animate({top: 35}, 200 );
    } else {
        if (SearchPanelState) {
            closeSearchPanel();
        }
        $("#cart-panel").animate({left: 10}, 300 );
        showCartPanelButtons();
        CartPanelState = true;
        $("#cart-panel-toggle").animate({top: 0}, 200 );
        $("#search-panel-toggle").animate({top: 515}, 200 );
    }
}

function closeCartPanel() {
    hideCartPanelButtons();
    $("#cart-panel").animate({left: -450}, 300 );
    CartPanelState = false;
    $("#search-panel-toggle").animate({top: 35}, 200 );
}

function toggleResultPanel() {
    if (ResultPanelState) {
        hideResultPanelButtons();
        $("#result-panel").animate({right: -450}, 300 );
        ResultPanelState = false;
    } else {
        $("#result-panel").animate({right: 10}, 300 );
        ResultPanelState = true;
        showResultPanelButtons();
    }
}

function defaultPanelState() {
    hideSearchPanelButtons();
    hideCartPanelButtons();
    hideResultPanelButtons();
    if (SearchPanelState) {
        $("#search-panel").animate({left: 10}, 300 );
        SearchPanelState = true;
        $("#cart-panel-toggle").animate({top: 515}, 200 );
        showSearchPanelButtons();
    } else if (CartPanelState) {
        $("#cart-panel").animate({left: 10}, 300 );
        $("#cart-panel-toggle").animate({top: 0}, 200 );
        $("#search-panel-toggle").animate({top: 515}, 200 );
    }
    if (ResultPanelState) {
        $("#result-panel").animate({right: 10}, 300 );
        showResultPanelButtons();
    }
}

function hideSearchPanelButtons() {
    $("#search-panel-search-button").hide();
    $("#search-panel-reset-button").hide();
}

function showSearchPanelButtons() {
    $("#search-panel-search-button").show();
    $("#search-panel-reset-button").show();
}

function hideCartPanelButtons() {
    $("#cart-panel-order-button").hide();
    $("#cart-panel-download-button").hide();
}

function showCartPanelButtons() {
    $("#cart-panel-order-button").show();
    $("#cart-panel-download-button").show();
}

function hideResultPanelButtons() {
    $("#result-panel-download-button").hide();
}

function showResultPanelButtons() {
    $("#result-panel-download-button").show();
}

function addNewDateRange() {
    var date_from = $('#date_from').val();
    var date_to = $('#date_to').val();
    if (date_from == '') {
        $('#date_from_cg').addClass('error');
        $('#date_from').focus();
    } else if (date_to == '') {
        $('#date_to_cg').addClass('error');
        $('#date_to').focus();
    } else if(date_to < date_from) {
        $('#date_to_cg').addClass('error');
        $('#date_to_inline').html('Date has to be later then date from!');
    } else {
        $('#date_to_cg').removeClass('error');
        $('#date_from_cg').removeClass('error');
        $('#date_to_inline').html('');
        var dr = '<p class="date_rage_row"><span class="date_from">'+date_from+'</span> - <span class="date_to">'+date_to+'</span> <span onclick="deleteDateRange(this);"> del </span></p>';
        $('#date_range').append(dr);
    }
}

function deleteDateRange(elem) {
    $(elem).parent().remove();
}

function submitSearchForm() {
    var search_data = new Object();
    _.each($('.listTree').data('listTree').selected, function(parent) {
        search_data[parent.key] = [];
        _.each(parent.values, function(sat) {
            search_data[parent.key].push(sat.val);
        });
    });
    search_data['Dates'] = [];
    _.each($('.date_rage_row'), function(row) {
        var dr = new Object();
        dr.date_from = $(row).children(".date_from").html();
        dr.date_to = $(row).children(".date_to").html();
        search_data['Dates'].push(dr);
    });
    console.log(search_data);
}

var data = [
    {
        "key": "Sensors",
        "val": "1",
        "values": [
            { "key": "CBERS-2B HR CCD", "val": "12" },
            { "key": "Landsat 2 MSS", "val": "13" },
            { "key": "Landsat 3 MSS", "val": "14" },
            { "key": "SPOT 2 HRV", "val": "15" },
            { "key": "SPOT 5 HRG", "val": "16" }
        ]
    },
    {
        "key": "Mission",
        "val": "2",
        "values": [
            { "key": "ZASat-002", "val": "22" },
            { "key": "LS-5", "val": "23" },
            { "key": "SPOT-4", "val": "24" }
        ]
    },
    {
        "key": "Sensor type",
        "val": "3",
        "values": [
            { "key": "HRG-5:Panchromatic B", "val": "32" },
            { "key": "HRG-5:Panchromatic A", "val": "33" },
            { "key": "HRG-5:Supersampled Panchromatic T", "val": "34" }
        ]
    },
    {
        "key": "Acquisition mode",
        "val": "4",
        "values": [
            { "key": "HRCC-2B:GRN", "val": "42" },
            { "key": "HRV-2:Camera 1", "val": "43" },
            { "key": "AMI-1:Vertical Vertical Polarisation", "val": "44" }
        ]
    }
];