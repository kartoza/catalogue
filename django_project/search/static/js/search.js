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
        $("#cart-panel-toggle").animate({top: 80}, 200 );
    } else {
        if (CartPanelState) {
            closeCartPanel();
        }
        $("#search-panel").animate({left: 10}, 300 );
        showSearchPanelButtons();
        SearchPanelState = true;
        $("#cart-panel-toggle").animate({top: 535}, 200 );
    }
}

function closeSearchPanel() {
    hideSearchPanelButtons();
    $("#search-panel").animate({left: -450}, 300 );
    SearchPanelState = false;
    $("#cart-panel-toggle").animate({top: 80}, 200 );
}

function toggleCartPanel() {
    if (CartPanelState) {
        hideCartPanelButtons();
        $("#cart-panel").animate({left: -490}, 300 );
        CartPanelState = false;
        $("#cart-panel-toggle").animate({top: 80}, 200 );
        $("#search-panel-toggle").animate({top: 27}, 200 );
    } else {
        if (SearchPanelState) {
            closeSearchPanel();
        }
        $("#cart-panel").animate({left: 10}, 300 );
        showCartPanelButtons();
        CartPanelState = true;
        $("#cart-panel-toggle").animate({top: -1}, 200 );
        $("#search-panel-toggle").animate({top: 590}, 200 );
    }
}

function closeCartPanel() {
    hideCartPanelButtons();
    $("#cart-panel").animate({left: -490}, 300 );
    CartPanelState = false;
    $("#search-panel-toggle").animate({top: 27}, 200 );
}

function toggleResultPanel() {
    if (ResultPanelState) {
        hideResultPanelButtons();
        $("#result-panel").animate({right: -491}, 300 );
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
        $("#cart-panel-toggle").animate({top: 535}, 200 );
        showSearchPanelButtons();
    } else if (CartPanelState) {
        $("#cart-panel").animate({left: 10}, 300 );
        $("#cart-panel-toggle").animate({top: 0}, 200 );
        $("#search-panel-toggle").animate({top: 535}, 200 );
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
    $.blockUI({
        message: '<div class="wrapperloading"><div class="loading up"></div><div class="loading down"></div></div>',
        css: {
            border: '1px solid #000',
            background: 'rgba(0, 0, 0, 0.3)',
            width: '450px',
            height:'450px'
        }
    });
};

APP.unblockResultPanel= function (){
    $.unblockUI();
};

APP.s = Snap('#svg');


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
            resetSearchFromErrors()
            APP.guid = data.guid;
            $APP.trigger('collectionSearch', {
              offset: 0
            });
            openResultPanel();
            toggleSearchPanel();
        },
        error: function(data) {
            if (data.status == '404') {
                processSearchFormErrors(data.responseText);
            } else {
                alert('There has been an error! Probably gnomes...');
                console.log(data);
            }
        }

    });
    // submit the form
    $('#catalogueSearch').submit();

}

function processSearchFormErrors(data) {
    /* process json with errors when search submit fails
    set class error to control-group div
    add span element that holds error message afer input */
    resetSearchFromErrors();
    var errors = $.parseJSON(data);
    for (field in errors) {
        var inputDOM = $('#id_'+field);
        inputDOM.parent().parent().addClass('error');
        var helpElem = '<span class="error-block">'+ errors[field] +'</span>'
        inputDOM.parent().append(helpElem);
    }
    $('#tab-3').prop('checked',true);
}

function resetSearchFromErrors() {
    /* remove all error notifciatons on search form */
    $('.error-block').each( function() { this.remove(); })
    $('.error').each( function() { $(this).removeClass('error'); })
}

// backbone models/collections/views

APP.$modal = $('#ajax-modal');
APP.$imagemodal = null;
APP.guid = '';

APP.ResultItem = Backbone.Model.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/'
});

APP.ResultItemCollection = PaginatedCollection.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/',
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
        if (_.size(this.collection.models) != 0) {
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
        }

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
        var text = 'Page ' + page_info.current_page + ' of ' + page_info.pages + ' ('+page_info.total+' records)';
        if (page_info.current_page > 1) {
            $('#searchPrev').show();
        } else {
            $('#searchPrev').hide();
        }
        if (page_info.current_page != page_info.pages) {
            $('#searchNext').show();
        } else {
            $('#searchNext').hide();
        }
        cur_pag_el.html(text);
    },
    _updateResultsInfo:function() {
        var text = '<b>Summary</b>:<br />'+this.collection.total+' records found for<br />Note:The SPOT Imagery provided in this backdrop has been degraded to 10m';
        var pag_el = this.$el.find('#resultsSummary');
        pag_el.html(text);
    }
});

APP.ResultGridViewItem = Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata',
        'click span.cart-button': 'addToCart',
        'click span.zoom-button': 'highlightResultItem',
        'click span.showBig-button': 'openBigImage',
        'click img.result-img': 'expandResultItem',
        'mouseenter img.result-img': 'focusItem',
        'mouseleave img.result-img': 'blurItem',
        'mouseleave': 'returnToMin'
    },
    initialize: function() {
        $APP.on('highlightResultItem', $.proxy(this.highlightResultItem, this));
        this.expanded = false;
    },

    openBigImage: function() {
        // APP.$modal.load('/thumbnail/'+this.model.get('id')+'/raw/', '', function(){
        //     APP.$imagemodal.modal();
        // });
        $.loadImage('/thumbnail/'+this.model.get('id')+'/raw/')
            .done(function(image) {
              $('#imageBoximage').attr('src',image.src);
              $('#imageBox').modal();
            })
            .fail(function(image) {

            });
        //$('#imageBoximage').attr('src','/thumbnail/'+this.model.get('id')+'/raw/');
        //setTimeout(function() {$('#imageBox').modal()}, 1000);;
        //$('#imageBoximage').fullsizable();
        //APP.$imagemodal.modal();

        //$.fullsizableOpen($('#imageBoximage'));
    },

    returnToMin: function() {
        // var selectedID = this.model.get('unique_product_id');
        // var div = $("#result_item_"+ selectedID);
        // if (this.expanded) {
        //     div.animate({'height': '46px'}, 500);
        //     div.find('.result-img').animate({'height': '45px','width': '45px', 'top': '0px'});
        //     this.expanded = false;
        // }
    },

    expandResultItem: function() {
        var selectedID = this.model.get('unique_product_id');
        var div = $("#result_item_"+ selectedID);
        if (!this.expanded) {
            div.animate({'height': '410px'}, 500);
            $('#results-container').animate({scrollTop: div.position().top+$('#results-container').scrollTop()}, 500);
            div.find('.result-img').animate({'height': '370px','width': '370px', 'top': '40px'});
            div.find('.zoom-button').show(400);
            div.find('.showBig-button').show(400);
            this.expanded = true;
        } else {
            div.animate({'height': '46px'}, 500);
            div.find('.result-img').animate({'height': '45px','width': '45px', 'top': '0px'});
            div.find('.zoom-button').hide();
            div.find('.showBig-button').hide();
            this.expanded = false;
        }
    },

    focusItem: function() {
        var selectedID = this.model.get('unique_product_id');
        var pos2 = $("#result_item_"+ selectedID).offset();
        var targetFeature = searchLayer.getFeatureElementRecordId(selectedID);
        var point = targetFeature.geometry.getCentroid();
        var pos = myMap.map.getPixelFromLonLat(new OpenLayers.LonLat(point.x, point.y));
        this.line = APP.s.line(pos.x, pos.y + 35, pos2.left+2, pos2.top+25);
        this.line.animate({stroke: "#228441", strokeWidth: "2"}, 500);
    },

    blurItem: function() {
        this.line.remove();
    },

    highlightResultItem: function(event, data) {
        // if id is not set presume user has clicked in result panel on item
        // if id is set presuem user has clicked record on the map
        if (typeof data == 'undefined') {
            $APP.trigger('highlightSearchRecord', {'unique_product_id': this.model.get('unique_product_id')});
            var selectedID = this.model.get('unique_product_id');
        } else {
            var selectedID = data.id;
        }
        $("#results-container div:first-child").each(function (id, data) {
            // reset selected rows
            $(data).removeClass('focusedResultRow');
        });
        $("#result_item_"+ selectedID).addClass('focusedResultRow');
    },

    showMetadata: function() {
        var id = this.model.get('id');
        APP.$modal.load('/metadata/'+id, '', function(){
            APP.$modal.modal();
        });

    },
    addToCart: function() {
        if (UserLoged) {
            var id = this.model.get('id');
            var exist = APP.Cart.filter(function(item) {
                return item.get("product").id == id;
            });
            if (exist.length > 0) {
                alert('Product already in cart!');
            } else {
                APP.Cart.create({'product': {'id':id}},{wait: true});
                alert('Product added to cart');
            }
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
            '<img class="result-img" src="/thumbnail/<%= model.get("id") %>/large/" />',
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
            '<span class="button zoom-button"><i class="icon-screenshot icon-2x"></i></span>',
            '<span class="button showBig-button"><i class="icon-desktop icon-2x"></i></span>',
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
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/',
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
        if (UserLoged) {
            this.collection.fetch({reset: true});
        }
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
        var id = this.model.get('product').id;
        APP.$modal.load('/metadata/'+id, '', function(){
            APP.$modal.modal();
        });
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

$.loadImage = function(url) {
  // Define a "worker" function that should eventually resolve or reject the deferred object.
  var loadImage = function(deferred) {
    var image = new Image();
    // Set up event handlers to know when the image has loaded
    // or fails to load due to an error or abort.
    image.onload = loaded;
    image.onerror = errored; // URL returns 404, etc
    image.onabort = errored; // IE may call this if user clicks "Stop"

    // Setting the src property begins loading the image.
    image.src = url;

    function loaded() {
      unbindEvents();
      // Calling resolve means the image loaded sucessfully and is ready to use.
      deferred.resolve(image);
    }
    function errored() {
      unbindEvents();
      // Calling reject means we failed to load the image (e.g. 404, server offline, etc).
      deferred.reject(image);
    }
    function unbindEvents() {
      // Ensures the event callbacks only get called once.
      image.onload = null;
      image.onerror = null;
      image.onabort = null;
    }
  };

  // Create the deferred object that will contain the loaded image.
  // We don't want callers to have access to the resolve() and reject() methods,
  // so convert to "read-only" by calling `promise()`.
  return $.Deferred(loadImage).promise();
};
