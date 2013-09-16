var map;
var SearchPanelState = true;
var CartPanelState = false;
var ResultPanelState = false;
var ResultDownloadOptionsState = false;
var CartDownloadOptionsState = false;
var LastSelectedResultItem = "0";

if (typeof APP == 'undefined') {
    APP = {};
    $APP = $(APP);
}

/* Transform an openlayers bounds object such that
 * it matches the CRS of the map
 * @param a bounds object (assumed to be in EPSG:4326)
 * @return a new bounds object projected into the map CRS
 */
function transformBounds(theBounds)
{
  var myBounds = theBounds.clone();
  var myCRS = new OpenLayers.Projection("EPSG:4326");
  var toCRS = map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
  myBounds.transform(myCRS, toCRS);
  return myBounds;
}

function transformGeometry(theGeometry)
{
  var myGeometry = theGeometry.clone();
  var myCRS = new OpenLayers.Projection("EPSG:4326");
  var toCRS = map.getProjectionObject() || new OpenLayers.Projection("EPSG:900913");
  myGeometry.transform(myCRS,toCRS);
  return myGeometry;
}

function initMap() {

    var options = {
        projection : new OpenLayers.Projection("EPSG:900913"),
        displayProjection : new OpenLayers.Projection("EPSG:4326"),
        units : 'm',
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,20037508.34, 20037508.34),
        numZoomLevels : 18,
        controls: [] //no controls by default we add them explicitly lower down
      };
    map = new OpenLayers.Map('map', options);
    var layerMapnik = new OpenLayers.Layer.OSM("Open Street Map");
    layerSearch = new OpenLayers.Layer.Vector("search_geometry");
    myLayersList = [
        WEB_LAYERS.zaSpot2mMosaic2010TC,
        WEB_LAYERS.zaSpot2mMosaic2009TC,
        WEB_LAYERS.zaSpot2mMosaic2008TC,
        WEB_LAYERS.zaSpot2mMosaic2007TC,
        WEB_LAYERS.zaSpot10mMosaic2010,
        WEB_LAYERS.zaSpot10mMosaic2009,
        WEB_LAYERS.zaSpot10mMosaic2008,
        WEB_LAYERS.zaSpot10mMosaic2007,
        WEB_LAYERS.zaRoadsBoundaries,
        layerMapnik,
        layerSearch
    ];
    map.addLayers(myLayersList);
    map.zoomToExtent( transformBounds(new OpenLayers.Bounds(14.0,-35.0,34.0,-21.0)));

    var myHighlightControl = new OpenLayers.Control.SelectFeature( layerSearch , {
        hover: false,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
            beforefeaturehighlighted: null,
            featurehighlighted: featureSelected,
            featureunhighlighted: null
        }
    });
    map.addControl(myHighlightControl);
    myHighlightControl.activate();
    layerSearch.selectFeatureControl = myHighlightControl;

    mNavigationPanel = new OpenLayers.Control.Panel({div : OpenLayers.Util.getElement('map-navigation')});
  map.addControl(mNavigationPanel);
  var myZoomInControl = new OpenLayers.Control.ZoomBox({
        title: "Zoom In Box: draw a box on the map, to see the area at a larger scale.",
        displayClass:'right icon-zoom-in icon-2x icon-border olControlZoomBoxIn',
        div : OpenLayers.Util.getElement('map-navigation'),
        out: false
      });
  //mMap.addControl(myZoomInControl);

  var myZoomOutControl = new OpenLayers.Control.ZoomBox({
        title: "Zoom Out Box: draw a box on the map, to see the area at a smaller scale.",
        displayClass:'right icon-zoom-out icon-2x icon-border olControlZoomBoxOut',
        div : OpenLayers.Util.getElement('map-navigation'),
        out: true
      });
  //mMap.addControl(myZoomOutControl);

    var myNavigationControl = new OpenLayers.Control.Navigation({
    title : "Pan map: click and drag map to move the map in the direction of the mouse.",
    zoomWheelEnabled: false,
    displayClass:'right icon-move icon-2x icon-border olControlNavigation',
    div : OpenLayers.Util.getElement('map-navigation'),
    }
  );
  //mMap.addControl(myNavigationControl);

    var myHistoryControl = new OpenLayers.Control.NavigationHistory({
  nextOptions: {
      title : "Next view: quickly jump to the next map view, works only with prevoius view.",
      displayClass:'right icon-chevron-right icon-2x icon-border olControlNavigationHistoryNext',
      div : OpenLayers.Util.getElement('map-navigation'),
    },
  previousOptions: {
      title : "Previous view: quickly jump to the prevoius map view.",
      displayClass:'right icon-chevron-left icon-2x icon-border olControlNavigationHistoryPrevious',
      div : OpenLayers.Util.getElement('map-navigation'),
    }
  });
  mNavigationPanel.addControls([myZoomInControl,myZoomOutControl, myNavigationControl, myHistoryControl.previous, myHistoryControl.next]);
}

function resetSceneZIndices() {
    var myFeatures = layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i) {
        myFeatures[i].attributes.zIndex=0;
        myFeatures[i].selected = "no";
    }
}

function getFeatureIndexByRecordId( theRecordId ) {
    var myFeatures = layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      if(myFeatures[i].attributes.unique_product_id == theRecordId)
      {
        return i;
      }
    }
}

function featureSelected(theEvent) {
    blockResultPanel();
    hightlightRecord(theEvent.feature.attributes.unique_product_id, false);
    unblockResultPanel();
}

function hightlightRecord( theRecordId, theZoomFlag )
{
  var myIndex = getFeatureIndexByRecordId( theRecordId );
  layerSearch.features[myIndex].attributes.zIndex=1;
  layerSearch.features[myIndex].selected = "yes";
  if ( LastSelectedResultItem != "0")
  {
    $("#result_item_"+ LastSelectedResultItem).css("background-color", "#ffffff");
  }
  LastSelectedResultItem = theRecordId;
  $("#result_item_"+ theRecordId).css("background-color", "#BAD696");
  resetSceneZIndices();
  if (theZoomFlag)
  {
    map.zoomToExtent(layerSearch.features[myIndex].geometry.bounds);
  }
  layerSearch.redraw();
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

function openResultPanel() {
    if (!ResultPanelState) {
        $("#result-panel").animate({right: 10}, 300 );
        ResultPanelState = true;
        showResultPanelButtons();
    }
}

function defaultPanelState() {
    hideResultDownloadOptions();
    hideCartDownloadOptions();
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

function hideResultDownloadOptions() {
    $(".downloadoptions").hide();
}

function showResultDownloadOptions() {
    $(".downloadoptions").show();
}

function hideCartDownloadOptions() {
    $(".downloadcartoptions").hide();
}

function showCartDownloadOptions() {
    $(".downloadcartoptions").show();
}

function showResultPanelButtons() {
    $("#result-panel-download-button").show();
}

function blockResultPanel() {
    $('body').block({
        message: 'Please wait <i class="icon-refresh icon-spin"></i>',
        css: {
            border: '1px solid #000',
            background: '#FFF',
            width: '350px',
            height:'200px',
            'line-height': '200px',
            'font-size': '24px'
        }
    });
}

function unblockResultPanel() {
    $('body').unblock();
}

function toggleResultDownloadButton() {
    if (ResultDownloadOptionsState) {
        hideResultDownloadOptions();
        $("#result-panel-download-button").animate({top: 500}, 200 );
        ResultDownloadOptionsState = false;
    } else {
        $("#result-panel-download-button").animate({top: 300}, 200 );
        setTimeout(showResultDownloadOptions,210);
        ResultDownloadOptionsState = true;
    }
}

function toggleCartDownloadButton() {
    if (CartDownloadOptionsState) {
        hideCartDownloadOptions();
        $("#cart-panel-download-button").animate({top: 370}, 200 );
        CartDownloadOptionsState = false;
    } else {
        $("#cart-panel-download-button").animate({top: 170}, 200 );
        setTimeout(showCartDownloadOptions,210);
        CartDownloadOptionsState = true;
    }
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
    // if (typeof(search_data['Collections']) == 'undefined')  {
    //     $('#sattelite_inline').html('You have to select at least 1 sensor!').addClass('form-error');
    //     $('#tab-1').prop('checked',true);
    //     form_ok = false;
    // } else {
    //     $('#sattelite_inline').html('');
    // }

    search_data['Dates'] = [];
    _.each($('.date_range_row'), function(row) {
        var dr = new Object();
        dr.date_from = $(row).children(".date_from").html().split('/');
        dr.date_to = $(row).children(".date_to").html().split('/');
        dr.date_from = dr.date_from[2]+'-'+dr.date_from[0]+'-'+dr.date_from[1];
        dr.date_to = dr.date_to[2]+'-'+dr.date_to[0]+'-'+dr.date_to[1];
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
        $.ajax({
            type: "POST",
            url: "/submitsearch/",
            data: search_data ,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                APP.guid = data.guid;
                $APP.trigger('collectionSearch', {
                    offset: 0
                });
                openResultPanel();
                toggleSearchPanel();
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }
}

var data = null;
$.ajax({
    'async':false,
    'url': '/getselectoptions/',
    'dataType': 'json'
}).done(function (response) {
    // update global var... we must refactor this
    data = response;
})

// backbone models/collections/views

APP.$modal = $('#ajax-modal');
APP.guid = '';

APP.ResultItem = Backbone.Model.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e64c/'
});

APP.ResultItemCollection = PaginatedCollection.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e64c/',
    urlRoot: function() {
        return '/api/v1/searchresults/'+ APP.guid + '/';
    },
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
        blockResultPanel();
        this.collection.previousPage();
        return false;
    },

    next: function() {
        blockResultPanel();
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
        //this.collection.fetch({reset: true});
        this.cont = $("#results-container");
        $APP.on('collectionSearch', $.proxy(this.collectionSearch, this));
    },

    collectionSearch: function (evt, options) {
        blockResultPanel();
        _.extend(this.collection, options);
        this.collection.fetch({
            reset: true
        });
    },
    render: function() {
        layerSearch.removeFeatures(layerSearch.features);
        this.cont.empty();
        var self=this;
        _(this.collection.models).each(function(item){
            self.renderItem(item);
        },this);
        this._update_pagination_info();
        this._updateResultsInfo();
        map.zoomToExtent(layerSearch.getDataExtent());
        unblockResultPanel();
        return this;
    },
    renderItem: function(item) {
        var feat = new OpenLayers.Feature.Vector(transformGeometry(OpenLayers.Geometry.fromWKT(item.attributes.spatial_coverage)),item.attributes);
        layerSearch.addFeatures([feat]);
        var myItem = new APP.ResultGridViewItem({
            model:item,
            collection:this.collection
        });
        this.cont.append(myItem.render().el);
    },
    _update_pagination_info:function() {
        var cur_pag_el = this.$el.find('#resultsPosition');
        var page_info = this.collection.pageInfo();
        var text = 'Page ' + page_info.current_page + ' of ' + page_info.pages + '('+page_info.total+' records)'
        cur_pag_el.html(text);
    },
    _updateResultsInfo:function() {
        var text = '<b>Summary</b>:<br />'+this.collection.total+' record found for<br />Note:The SPOT Imagery provided in this backdrop has been degraded to 10m';
        var pag_el = this.$el.find('#resultsSummary');
        pag_el.html(text);
    }
});

APP.ResultGridViewItem = Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata',
        'click span.cart-button': 'addToCart',
        'click img.result-img': 'highlightResultItem'
    },
    initialize: function() {
        $APP.on('highlightResultItem', $.proxy(this.highlightResultItem, this));
    },
    highlightResultItem: function() {
        hightlightRecord(this.model.get('unique_product_id'), true);
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
    addToCart: function() {
        if (UserLoged) {
            var id = this.model.get('id');

            APP.Cart.create({'product': {'id':id}},{wait: true});
            alert('Product added to cart');
        } else {
            alert('You need to log in first!');
        }
    },
    render: function() {
       $(this.el).html(_.template(template, {model:this.model}));
        return this;
    },
});

var template = [
            '<div class="result-item" id="result_item_<%= model.get("unique_product_id") %>">',
            '<img class="result-img" src="/thumbnail/<%= model.get("id") %>/medium/" />',
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


APP.CartItem = Backbone.Model.extend({
    urlRoot: '/api/v1/searchrecords/',
    idAttribute: 'id',
    url: function () {
        var urlRoot;
        if (_.isFunction(this.urlRoot)) { urlRoot = this.urlRoot(); } else { urlRoot = this.urlRoot; }
        var id;
        if (typeof this.id === 'undefined') {
            id = '';
        } else {
            id = this.id + '/';
        }
        return urlRoot+id;
    }
});

APP.CartItemCollection = Backbone.Collection.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e64c/',
    urlRoot: '/api/v1/searchrecords/',
    model: APP.CartItem,
    limit: 100
});

APP.Cart = new APP.CartItemCollection();

APP.CartGridView = Backbone.View.extend({
    el: $("#cart-container"),

    initialize: function() {
        this.collection.bind('reset', this.render, this);
        this.collection.bind('add', this.render, this);
        this.collection.bind('destroy', this.render, this);
        this.collection.fetch({reset: true});
    },
    render: function() {
        // house keeping
        this.$el.empty();
        var self=this;
        _(this.collection.models).each(function(item){
            self.renderItem(item);
        },this);
        $('#cart-container').perfectScrollbar('update');
        return this;
    },
    renderItem: function(item) {
        var myItem = new APP.CartGridViewItem({
            model:item,
            collection:this.collection
        });
        this.$el.append(myItem.render().el);
    }
});

APP.CartGridViewItem = Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata',
        'click span.delete-button': 'delete'
    },

    showMetadata: function() {
        $('body').modalmanager('loading');
        var id = this.model.get('product').id;
        setTimeout(function(){
            APP.$modal.load('/metadata/'+id, '', function(){
            APP.$modal.modal();
        });
      }, 1000);
    },
    delete: function() {
        var del = confirm('Are you sure?');
        if (del) {
            this.model.destroy({wait: true});
        }
    },
    render: function() {
       $(this.el).html(_.template(templateCart, {model:this.model}));
        return this;
    },
});


var templateCart = [
        '<div class="cart-item">',
          '<img src="/thumbnail/<%= model.get("product").id %>/large/" />',
          '<div class="cart-item-info">',
            '<p><%= model.get("product").unique_product_id %></p>',
            '<p><%= model.get("product").product_date %></p>',
            '<div class="buttons">',
              '<span class="button metadata-button"><i class="icon-list-alt"></i> Metadata</span>',
              '<span class="button icon-2x delete-button"><i class="icon-trash"></i></span>',
            '</div>',
          '</div>',
          '<div class="cloud-cover">',
            '<img src="/static/images/cloud-icon.png" />',
            '<p><%= model.get("product").cloud_cover %></p>',
          '</div>',
        '</div>'
        ].join('');

var CartgridViewHtml = new APP.CartGridView({
        'collection': APP.Cart});