var map = new OpenLayers.Map( 'map', {controls: []});
var SearchPanelState = false;
var CartPanelState = false;
var ResultPanelState = true;


if (typeof APP == 'undefined') {
    APP = {};
    $APP = $(APP);
}

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

// backbone models/collections/views

APP.$modal = $('#ajax-modal');

APP.ResultItem = Backbone.Model.extend({
    urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e64c/'
});

APP.ResultItemCollection = PaginatedCollection.extend({
    urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e64c/',
    model: APP.ResultItem,
    limit: 15
});

APP.Results = new APP.ResultItemCollection();

APP.ResultGridView = Backbone.View.extend({
    el: $("#result-panel"),

    events: {
        'click div.searchPrev': 'previous',
        'click div.searchNext': 'next'
    },

    previous: function() {
        this.collection.previousPage();
        return false;
    },

    next: function() {
        this.collection.nextPage();
        return false;
    },

    first: function() {
        this.collection.firstPage();
        return false;
    },

    last: function() {
        this.collection.lastPage();
        return false;
    },

    initialize: function() {
        this.collection.bind('reset', this.render, this);
        this.collection.fetch({reset: true});
        this.cont = $("#results-container");
    },

    collectionSearch: function (evt, options) {
        _.extend(this.collection, options);
        this.collection.fetch({
            reset: true
        });
    },
    render: function() {
        // house keeping
        this.cont.empty();
        var self=this;
        _(this.collection.models).each(function(item){
            self.renderItem(item);
        },this);
        this._update_pagination_info();
        return this;
    },
    renderItem: function(item) {
        var myItem = new APP.ResultGridViewItem({
            model:item,
            collection:this.collection
        });
        this.cont.append(myItem.render().el);
    },
    _update_pagination_info:function() {
        var cur_pag_el = this.$el.find('.cur_pag_page');
        var tot_pag_el = this.$el.find('.tot_pag_page');
        var total_rec_el = this.$el.find('.total_pag_records');
        var page_info = this.collection.pageInfo();
        cur_pag_el.html(page_info.current_page);
        tot_pag_el.html(page_info.pages);
        total_rec_el.html(page_info.total);
    }
});

APP.ResultGridViewItem = Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata'
    },

    showMetadata: function() {
        $('body').modalmanager('loading');
        var id = this.model.get('id');
        setTimeout(function(){
            APP.$modal.load('/metadata/'+id, '', function(){
            APP.$modal.modal();
        });
      }, 1000);
    },
    render: function() {
       $(this.el).html(_.template(template, {model:this.model}));
        return this;
    },
});

var template = [
            '<div class="result-item">',
            '<img src="/thumbnail/<%= model.get("id") %>/medium/" />',
            '<div class="result-item-info">',
              '<p><%= model.get("unique_product_id") %></p>',
              '<p><%= model.get("product_date") %></p>',
            '</div>',
            '<div class="cloud-cover">',
              '<img src="/static/images/cloud-icon.png" />',
              '<p>',
              '<% if(model.get("cloud_cover") != -1) { %><%= model.get("cloud_cover") %>',
              '<% } else { %>UNK',
              '<% } %>',
              '</p>',
            '</div>',
            '<span class="button metadata-button"><i class="icon-list-alt icon-2x"></i></span>',
            '<span class="button cart-button"><i class="icon-shopping-cart icon-2x"></i></span>',
          '</div>'
          ].join('');

var ResultgridViewHtml = new APP.ResultGridView({
        'collection': APP.Results});