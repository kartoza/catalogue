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
        var dr = '<p class="date_range_row"><span class="date_from">'+date_from+'</span><span>-</span> <span class="date_to">'+date_to+'</span> <span onclick="deleteDateRange(this);"> <i class="icon-trash"></i> </span></p>';
        $('#date_range').append(dr);
    }
}

function deleteDateRange(elem) {
    $(elem).parent().remove();
}

function submitSearchForm() {
    var search_data = new Object();
    var form_ok = true;

    _.each($('.listTree').data('listTree').selected, function(parent) {
        search_data[parent.key] = [];
        _.each(parent.values, function(sat) {
            search_data[parent.key].push(sat.val);
        });
    });

    if (typeof(search_data['Sensors']) == 'undefined')  {
        $('#sattelite_inline').html('You have to select at least 1 sensor!').addClass('form-error');
        $('#tab-1').prop('checked',true);
        form_ok = false;
    } else {
        $('#sattelite_inline').html('');
    }

    search_data['Dates'] = [];
    _.each($('.date_range_row'), function(row) {
        var dr = new Object();
        dr.date_from = $(row).children(".date_from").html();
        dr.date_to = $(row).children(".date_to").html();
        search_data['Dates'].push(dr);
    });

    if (search_data['Dates'].length == 0) {
        $('#daterange_inline').html('You have to select at least 1 date range!').addClass('form-error');
        $('#tab-2').prop('checked',true);
        form_ok = false;
    } else {
        $('#daterange_inline').html('');
    }

    if ($('#panchromatic_imagery').prop('checked')) {
        search_data['panchromatic_imagery'] = 1
    }

    if ($('#free_imagery').prop('checked')) {
        search_data['free_imagery'] = 1
    }

    if ($('#cloud_cover').val() != '') {
        search_data['cloud_cover'] = $('#cloud_cover').val();
    }

    if ($('#path').val() != '') {
        search_data['path'] = $('#path').val();
    }

    if ($('#row').val() != '') {
        search_data['row'] = $('#row').val();
    }

    if ($('#bbox').val() != '') {
        search_data['bbox'] = $('#bbox').val();
    }

    if ($('#sensor_inc_start').val() != '') {
        search_data['sensor_inc_start'] = $('#sensor_inc_start').val();
    }

    if ($('#sensor_inc_end').val() != '') {
        search_data['sensor_inc_end'] = $('#sensor_inc_end').val();
    }

    if ($('#resolution').val() != '') {
        search_data['resolution'] = $('#resolution').val();
    }

    if ($('#band_count').val() != '') {
        search_data['band_count'] = $('#band_count').val();
    }

    if (form_ok) {
        search_data = JSON.stringify(search_data);
        console.log(search_data);
    }
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