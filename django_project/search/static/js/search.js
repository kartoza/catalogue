var SearchPanelState = true;
var CartPanelState = false;
var ResultPanelState = false;
var ResultDownloadOptionsState = false;
var CartDownloadOptionsState = false;
var LayerSwitcherState = false;

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

APP.blockResultPanel = function() {
    $('body').block({
        message: '<div class="wrapperloading"><div class="loading up"></div><div class="loading down"></div></div>',
        css: {
            border: '1px solid #000',
            background: 'rgba(0, 0, 0, 0.3)',
            width: '550px',
            height:'550px'
        }
    });
};

APP.unblockResultPanel= function (){
    $('body').unblock();
};

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

function toggleLayerSwitcher() {
    if (LayerSwitcherState) {
        $('#map-layerswitcher').hide();
        $('#map-layerswitcher-control').css('color','#FFFFFF');
        LayerSwitcherState = false;
    } else {
        $('#map-layerswitcher').show();
        $('#map-layerswitcher-control').css('color','green');
        LayerSwitcherState = true;
    }
}

function validate_form(){
  var form_ok = false;
  var myDateRange = $('#date_range .date_range_row');
  if (myDateRange.length === 0) {
      $('#daterange_inline').html('You have to select at least 1 date range!').addClass('form-error');
      $('#tab-2').prop('checked',true);
  } else {
    form_ok = true;
    // clear missing daterange error
    $('#daterange_inline').html('');
  }
  return form_ok;
}

function submitSearchForm() {
    $('#catalogueSearch').ajaxForm({
        type: 'POST',
        dataType: 'json',
        beforeSubmit: function(formData, jqForm, options) {
          if (validate_form()) {
            // process data if needed... before submit
            var selected_sensors = [];
            _.each($('.listTree').data('listTree').selected, function(parent) {
              _.each(parent.values, function(sensor) {
                selected_sensors.push(sensor.val);
              });
            });
            _.each(formData, function (element, index) {
              if (element.name === 'selected_sensors') {
                // update selected sensors value
                formData[index].value = selected_sensors;
              }
            });
          } else {
            // don't submit the form, there is an error in JS form validation
            return false;
          }
        },
        success: function(data){
          APP.guid = data.guid;
          $APP.trigger('collectionSearch', {
              offset: 0
          });
          openResultPanel();
          toggleSearchPanel();
        },
        error: function() {
          alert('oops!');
        }

    });
    // submit the form
    $('#catalogueSearch').submit();

}

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
        APP.blockResultPanel();
        this.collection.previousPage();
        return false;
    },

    next: function() {
        APP.blockResultPanel();
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
        $APP.on('');
    },

    collectionSearch: function (evt, options) {
        $APP.trigger('ResultGridView_fetchresults');
        APP.blockResultPanel();
        _.extend(this.collection, options);
        this.collection.fetch({
            reset: true,
            error: function() { APP.unblockResultPanel(); }
        });
    },
    render: function() {
        $APP.trigger('SearchLayer_addFeatures', {
            'data': this.collection.models
        });

        this.cont.empty();
        var self=this;
        _(this.collection.models).each(function(item){
            self.renderItem(item);
        },this);
        this._update_pagination_info();
        this._updateResultsInfo();

        APP.unblockResultPanel();

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
        var cur_pag_el = this.$el.find('#resultsPosition');
        var page_info = this.collection.pageInfo();
        var text = 'Page ' + page_info.current_page + ' of ' + page_info.pages + '('+page_info.total+' records)';
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
        $APP.trigger('highlightSearchRecord', {'unique_product_id': this.model.get('unique_product_id')});
        $("#results-container div:first-child").each(function (id, data) {
            // reset selected rows
            $(data).css("background-color", "#ffffff");
        });
        $("#result_item_"+ this.model.get('unique_product_id')).css("background-color", "#BAD696");
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