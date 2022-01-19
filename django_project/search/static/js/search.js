var SearchPanelState = true;
var CartPanelState = false;
var ResultPanelState = false;
var ResultDownloadOptionsState = false;
var CartDownloadOptionsState = false;
var LayerSwitcherState = false;
var ButtonSubPanelState = false;

function toggleSearchPanel() {
    if (SearchPanelState) {
        closeSearchPanel();
    } else {
        if (CartPanelState) {
            closeCartPanel();
        }
        $("#search-panel").animate({left: 10}, 300 );
        $('#search-panel-toggle').addClass('active');
        SearchPanelState = true;
    }
}

function closeSearchPanel() {
    $('#search-panel-toggle').removeClass('active');
    $("#search-panel").animate({left: -450}, 300 );
    SearchPanelState = false;
}

function toggleCartPanel() {
    if (CartPanelState) {
        closeCartPanel();
        CartPanelState = false;
    } else {
        if (SearchPanelState) {
            closeSearchPanel();
        }
        $("#cart-panel").animate({left: 10}, 300 );
        $('#cart-panel-toggle').addClass('active');
        CartPanelState = true;
    }
}

function closeCartPanel() {
    $("#cart-panel").animate({left: -490}, 300 );
    $('#cart-panel-toggle').removeClass('active');
    CartPanelState = false;
}

function toggleResultPanel() {
    if (ResultPanelState) {
        $("#result-panel").animate({right: -491}, 300 );
        ResultPanelState = false;
    } else {
        $("#result-panel").animate({right: 10}, 300 );
        ResultPanelState = true;
    }
}

function openResultPanel() {
    if (!ResultPanelState) {
        $("#result-panel").animate({right: 10}, 300 );
        ResultPanelState = true;
    }
}

function defaultPanelState() {
    hideResultDownloadOptions();
    hideCartDownloadOptions();
    if (SearchPanelState) {
        $("#search-panel").animate({left: 10}, 300 );
        SearchPanelState = true;
    } else if (CartPanelState) {
        $("#cart-panel").animate({left: 10}, 300 );
    }
    if (ResultPanelState) {
        $("#result-panel").animate({right: 10}, 300 );
    }
}

function hideResultDownloadOptions() {
    $('#result-panel-download-button').html('<i class="icon-download-alt"></i> Download Results Data');
    $("#result-panel-btns").fadeOut('fast');
    ResultDownloadOptionsState = false;
}

function showResultDownloadOptions() {
    $('#result-panel-download-button').html('<i class="icon-remove"></i> Hide Download Options');
    $("#result-panel-btns").fadeIn('fast');
    ResultDownloadOptionsState = true;
}

function hideCartDownloadOptions() {
    $('#cart-panel-btns').fadeOut('fast');
}

function showButtonSubPanel() {
    $('#cart-show-map').fadeIn('fast');
    $('#place_order').fadeIn('fast');
    $('#cart-panel-download-button').fadeIn('fast');
    ButtonSubPanelState = true;
}

function hideButtonSubPanel() {
    $('#cart-show-map').hide();
    $('#place_order').hide();
    $('#cart-panel-download-button').hide();
    ButtonSubPanelState = false;
}

function showCartDownloadOptions() {
    $('#cart-panel-btns').fadeIn('fast');
}

function toggleSearchShare() {
    var btn = $("#SearchShare");
    var content = $('#SearchShare-content');
    var div = $('#SearchShare-input-container');
    var input = '<input type="text" value="http://' + window.location.host + '/search/' + APP.guid + '/" onclick="this.select();"/>';
    if (!searchShareOpen) {
        div.html(input);
        content.fadeIn('fast');
        btn.html('<i class="icon-remove"></i>');
        searchShareOpen = true;
    } else {
        content.fadeOut('fast');
        btn.html('<i class="icon-link"></i>');
        searchShareOpen = false;
    }
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
    } else {
        showResultDownloadOptions();
    }
}

function toggleCartDownloadButton() {
    if (CartDownloadOptionsState) {
        hideCartDownloadOptions();
        $('#cart-panel-download-button').html('<i class="icon-download"></i>');
        CartDownloadOptionsState = false;
    } else {
        showCartDownloadOptions();
        $('#cart-panel-download-button').html('<i class="icon-remove"></i> Hide Options');
        CartDownloadOptionsState = true;
    }
}

function toggleLayerSwitcher() {
    if (LayerSwitcherState) {
        $('#map-layerswitcher').hide();
        $('#map-layerswitcher-control').children('button').removeClass('btn-success');
        $('#map-layerswitcher-control').children('button').addClass('btn-info');

        LayerSwitcherState = false;
    } else {
        $('#map-layerswitcher').show();
        $('#map-layerswitcher-control').children('button').removeClass('btn-info');
        $('#map-layerswitcher-control').children('button').addClass('btn-success');
        LayerSwitcherState = true;
    }
}

function validate_form(){
  var form_ok = false;
  var myDateRange = $('#date_range .date_range_row');
  if (myDateRange.length === 0) {
        var helpElem = '<span class="error-block">You have to select at least 1 date range!</span>'
        $('#date_range').parent().prepend(helpElem);
        $('#content-2').collapse('show');
  } else {
    form_ok = true;
  }
  return form_ok;
}

function submitSearchForm() {
    $('#catalogueSearch').ajaxForm({
        type: 'POST',
        dataType: 'json',
        beforeSubmit: function(formData, jqForm, options) {
            // check if bounding box exists when KML/KMZ file presents
            if ($('#id_geometry_file').val() != "") {
                if ($('#id_aoi_geometry').val() == "")
                {
                    alert("Please specify Bounding Box");
                    $('#id_aoi_geometry').focus();
                    return false;
                }
            }
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
            resetSearchFromErrors();
            APP.guid = data.guid;
            $APP.trigger('collectionSearch', {
              offset: 0
            });
            //set redirect link if user it not loged in
            // if he logs in, he will be redirected  back to last performed search
            if (!UserLoged) {
                var link = $('#login_link').attr("href") + '?next=/search/' + APP.guid + '/';
                $('#login_link').attr("href", link);
                link = $('#login_register').attr("href") + '?next=/search/' + APP.guid + '/';
                $('#login_register').attr("href", link);
            }
            openResultPanel();
            //toggleSearchPanel();
        },
        error: function(data) {
            if (data.status == '404') {
                processSearchFormErrors(data.responseText);
            } else {
                alert('Sorry! There has been an error. Please try again');
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
    $('.error-block').first().closest('.accordion-body').collapse('show');
}

function resetSearchFromErrors() {
    /* remove all error notifciatons on search form */
    $('.error-block').each( function() { this.remove(); })
    $('.error').each( function() { $(this).removeClass('error'); })
}

function resetSearchForm() {
    // reset listTree
    $('.listTree').listTree('deselectAll');
    // remove dateranges
    $('#date_range').daterange('reset');
    // reset text fields
    $('input:text').each(function() {
        $(this).val('');
    });
    // set cloud back to 100
    $('#id_cloud_min').val(0);
    $('#id_cloud_max').val(100);
    // clear checkboxes
    $('input:checkbox').each(function() {
        $(this).attr('checked', false);
    });
    // reset dropdowns
    $('#id_spatial_resolution').prop('selectedIndex',0);
    $('#id_band_count').prop('selectedIndex',0);

    // reset file filed
    file = $('#id_geometry_file');
    file.val("");
    file.replaceWith( file = file.clone( true ) );

    // reset search summary widget
    // searchSummary.reset();
    resetSearchFromErrors();
}

// backbone models/collections/views



APP.$modal = $('#ajax-modal');
APP.$imagemodal = null;
APP.guid = '';
APP.selectedFeatureID = '';

APP.isNumber = function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

APP.checkDateRange = function(e) {
    if (JSON.parse(e.dates).length > 0) {
        $('#search_button').removeClass('disabled');
        $('#daterange_heading').removeClass('red');
    } else {
        $('#search_button').addClass('disabled');
        $('#daterange_heading').addClass('red');
    }
};

APP.addErrorNotifiction = function(e, msg) {
    $(e.target).parent().parent().addClass('error');
            var helpElem = '<span class="error-block">'+msg+'</span>'
            $(e.target).parent().append(helpElem);
}

APP.removeErrorNotification = function(e) {
    $(e.target).parent().find('.error-block').each( function() { this.remove(); })
    $(e.target).parent().parent().removeClass('error');
}

APP.handleAoiGeometry = function(e) {
    var error_msg = 'Area of interest geometry is not valid.';
    APP.removeErrorNotification(e);
    $APP.trigger('clearAoiBounds');
    if (e.target.value != '') {
        var values = e.target.value.split(',');
        if (values.length == 3) {
            if (!APP.isNumber(values[0]) || !APP.isNumber(values[1]) || !APP.isNumber(values[2]))
                {
                    APP.addErrorNotifiction(e,error_msg);
                    return;
                }
            $APP.trigger('drawCircle', {'x': values[0], 'y': values[1], 'r': values[2]});
        } else if (values.length == 4) {
            if (!APP.isNumber(values[0]) || !APP.isNumber(values[1]) || !APP.isNumber(values[2]) || !APP.isNumber(values[3]))
                {
                    APP.addErrorNotifiction(e,error_msg);
                    return;
                }
            $APP.trigger('drawBox', {'x1': values[0], 'y1': values[1], 'x2': values[2], 'y2': values[3]});
        } else {
            APP.addErrorNotifiction(e,error_msg);
        }
    }
}

APP.handlePathorRow = function(e) {
    var error_msg = 'Enter a valid value.';
    APP.removeErrorNotification(e);
    if (e.target.value != '') {
        if (e.target.value.length == 1) {
            if (!APP.isNumber(e.target.value)) {
                APP.addErrorNotifiction(e,error_msg);
                return;
            }
        }
        if (e.target.value.search(/^[0-9\-,\s]+$/) === -1) {
            APP.addErrorNotifiction(e,error_msg);
            return;
        }

    }
}

APP.handleCloudMax = function(e) {
    var error_msg = 'Enter a valid value, number between 0 and 100.';
    APP.removeErrorNotification(e);
    if(!isValidCloud(e.target.value) || !isValidCloud($('#id_cloud_min').val())) {
        APP.addErrorNotifiction(e,error_msg);
        return;
    }
    if($('#id_cloud_min').val() - e.target.value > 0) {
        error_msg = 'Range is incorrect';
        APP.addErrorNotifiction(e,error_msg);
    }
}

APP.handleCloudMin = function(e) {
    var error_msg = 'Enter a valid value, number between 0 and 100.';
    APP.removeErrorNotification(e);

    if(!isValidCloud(e.target.value) || !isValidCloud($('#id_cloud_max').val())) {
        APP.addErrorNotifiction(e,error_msg);
        return;
    }

    if($('#id_cloud_max').val() - e.target.value < 0) {
        error_msg = 'Range is incorrect';
        APP.addErrorNotifiction(e,error_msg);
    }
}

function isValidCloud(cloud) {
    if (cloud != '') {
        if (!APP.isNumber(cloud)) {
            return false;
        }
        if (cloud < 0 || cloud > 100) {
            return false;
        }
        return true;
    }
    return false;
}

APP.handleAngle = function(e) {
    var error_msg = 'Enter a number.';
    APP.removeErrorNotification(e);
    if (e.target.value != '') {
        if (!APP.isNumber(e.target.value)) {
            APP.addErrorNotifiction(e,error_msg);
            return;
        }
    }
}

APP.upload_image = function(field, upload_url) {
    if (field.files.length == 0) {
        return;
    }
    file = field.files[0];
    var formdata = new FormData();
    formdata.append('file_upload', file);
    $.ajax({
        url: upload_url,
        type: 'POST',
        data: formdata,
        processData: false,
        contentType: false,
        success: function(data) {
            $APP.trigger('clearAoiBounds');
            $APP.trigger('drawWKT', {'wkt': data.wkt});
        },
        error: function(data, text) {
            alert($.parseJSON(data.responseText).error);
        }
    });
}

$(document).on("sansaDateRangeChanged", APP.checkDateRange);
$('#id_aoi_geometry').on("keyup", APP.handleAoiGeometry);
$('#id_k_orbit_path').on("keyup", APP.handlePathorRow);
$('#id_j_frame_row').on("keyup", APP.handlePathorRow);
$('#id_cloud_max').on("keyup", APP.handleCloudMax);
$('#id_cloud_min').on("keyup", APP.handleCloudMin);
$('#id_sensor_inclination_angle_start').on("keyup", APP.handleAngle);
$('#id_sensor_inclination_angle_end').on("keyup", APP.handleAngle);
$('#id_geometry_file').on("change", function() {
      APP.upload_image(document.getElementById("id_geometry_file"),'/upload_geo/')
    });

APP.ResultItem = Backbone.Model.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/'
});
APP.ResultItemCollection = PaginatedCollection.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/',
    urlRoot: function() {
        return '/api/v1/searchresults/'+ APP.guid + '/';
    },
    model: APP.ResultItem,
    limit: APP.searchresults
});

APP.Results = new APP.ResultItemCollection();

APP.ResultGridView = Backbone.View.extend({
    el: $("#result-panel"),

    events: {
        'click div.searchPrev': 'previous',
        'click div.searchNext': 'next',
        'click button.resetZoom': 'resetZoom'
    },

    resetZoom: function() {
        $APP.trigger('resetZoom');
    },

    jumpToPage: function(page) {
        APP.blockResultPanel();
        this.collection.jumpToPage(page);
        return false;
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

    clearHTML: function() {
        this.cont.empty();
        $('#searchPrev').hide();
        $('#searchNext').hide();
        $('#SearchShare').hide();
        $('#paginator').html('');
        this.$el.find('#resultsPosition').html('');
    },

    collectionSearch: function (evt, options) {
        $APP.trigger('ResultGridView_fetchresults');
        APP.blockResultPanel();
        this.clearHTML();
        _.extend(this.collection, options);
        this.collection.fetch({
            reset: true,
            error: function() { APP.unblockResultPanel(); }
        });
    },
    render: function() {
        $('#result-panel-toggle').removeClass('hide');
        if (_.size(this.collection.models) != 0) {
            $APP.trigger('SearchLayer_addFeatures', {
                'data': this.collection.models
            });

            this.cont.empty();
            $('#results-container').perfectScrollbar('destroy');
            this.cont.append('<div class="result-items-header"><div class="result-item-info">Product</div><div class="result-item-info-date">Date</div><div class="cloud-cover">Cloud cover</div></div>');
            var self=this;
            _(this.collection.models).each(function(item){
                self.renderItem(item);
            },this);
            this._update_pagination_info();
        }
        $('#results-container').perfectScrollbar( { wheelSpeed: 20, wheelPropogation: true } );
        APP.unblockResultPanel();
        return this;
    },
    renderItem: function(item) {
        var myItem = new APP.ResultGridViewItem({
            model:item,
            collection:this.collection
        });
        var el = myItem.render().el;
        this.cont.append(el);
        // check if result item if is in cart
        var id = myItem.model.get('id');
        var exist = APP.Cart.filter(function(item) {
            return item.get("product").id == id;
        });
        // if it is, color it differently
        if (exist.length > 0) {
            $("#result_item_"+ myItem.model.get('original_product_id')).addClass('cartResultRow');
            $("#result_item_"+ myItem.model.get('original_product_id')).children('.cart-remove-button').removeClass('hide');
            $("#result_item_"+ myItem.model.get('original_product_id')).children('.cart-button').addClass('hide');
        }
    },

    _createSelectPaginator: function(current, end) {
        var select = document.createElement("select");
        select.style.width = "50px";
        var self = this;
        select.onchange = function(event) {
            self.jumpToPage(event.target.value);
        };
        var option;
        for (var i = 1; i < end+1; i++) {
            option = document.createElement("option");
            option.setAttribute("value", i);
            option.innerHTML = i;
            select.appendChild(option);
        }
        select.options.selectedIndex = current-1;
        return select;
    },

    _update_pagination_info:function() {
        var cur_pag_el = this.$el.find('#resultsPosition');
        var page_info = this.collection.pageInfo();
        var paginator = this._createSelectPaginator(page_info.current_page, page_info.pages);
        var showing = page_info.limit;
        if (page_info.total < page_info.limit) showing = page_info.total;
        var text = 'Page <span id="paginator"></span> of ' + page_info.pages + ' ('+page_info.total+' records)';
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
        $('#SearchShare').show();
        cur_pag_el.html(text);
        $('#paginator').html(paginator);
        if (page_info.current_page == 1) {
            $('#main-content').prepend('<div class="alert alert-info alert-dismissable alert-search"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>'+page_info.total+' Records Returned. Displaying '+showing+'.</strong></div>');
            window.setTimeout(function () {
                $(".alert").alert('close');
            }, 6000);
        }
    }
});

APP.ResultGridViewItem = Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata',
        'click span.cart-button': 'addToCart',
        'click span.cart-remove-button': 'removeFromCart',
        'click': 'highlightResultItem',
        'click img': 'imagePopover',
        'mouseenter': 'focusItem',
        'mouseleave': 'blurItem',
        'mouseleave span': function() {console.log('test');},
    },
    initialize: function() {
        $APP.on('highlightResultItem', $.proxy(this.highlightResultItem, this));
        $APP.on('removedItemFromCartUpdateResults', $.proxy(this.removedItemFromCartUpdateResults, this));
        this.expanded = false;
    },

    imagePopover: function(event) {
        if (typeof varPopover == 'undefined') varPopover = [{'id': 0}];
        if (varPopover[0].id == $(event.currentTarget).parent()[0].id) {
            $(event.currentTarget).parent().popover('hide');
            varPopover = [{'id': 0}];
        } else {
            if (varPopover[0].id != 0) varPopover.popover('destroy');
            var src = event.currentTarget.src.replace('mini','large');
            varPopover = $(event.currentTarget).parent();
            $.loadImage(src).done(function(image) {
                var src = image.src.replace('large','raw');
                varPopover.popover({
                    content: '<img src="'+image.src+'" /><br /><a data-lightbox="'+src+'" href="' + src + '">Open large preview</a>',
                    placement: 'left',
                    container: 'body',
                    html: true
                }).popover('show');
            });
        }
        event.stopPropagation();
    },

    focusItem: function() {
        var selectedID = this.model.get('original_product_id');
        var pos2 = $("#result_item_"+ selectedID).offset();
        var targetFeature = searchLayer.getFeatureElementRecordId(selectedID);
        if (targetFeature.onScreen()) {
            var point = targetFeature.geometry.getCentroid();
            var pos = myMap.map.getPixelFromLonLat(new OpenLayers.LonLat(point.x, point.y));
            this.line = APP.s.line(pos.x, pos.y + 35, pos2.left+2, pos2.top+9);
            this.line.animate({stroke: "#2f96b4", strokeWidth: "4"}, 500);
        }
        $APP.trigger('focusFeature', {'original_product_id': selectedID});
    },

    blurItem: function() {
        if (typeof this.line != 'undefined') this.line.remove();
        var selectedID = this.model.get('original_product_id');
        if (APP.selectedFeatureID == selectedID) {
            $APP.trigger('highlightSearchRecord', {'original_product_id': selectedID, 'zoom': false});
        } else {
            $APP.trigger('removeFocusFeature', {'original_product_id': selectedID});
        }
    },

    removedItemFromCartUpdateResults: function(event, data) {
        var exist = this.collection.filter(function(item) {
                return item.get("original_product_id") == data.original_product_id;
            });
        if (exist.length > 0) {
            this._removeFromCart(data.original_product_id);
            $APP.trigger('removedItemFromCart', {'original_product_id': data.original_product_id});
        }
    },

    highlightResultItem: function(event, data) {
        // if id is not set presume user has clicked in result panel on item
        // if id is set presume user has clicked record on the map
        if (typeof data == 'undefined') {
            $APP.trigger('highlightSearchRecord', {'original_product_id': this.model.get('original_product_id'), 'zoom': true});
            var selectedID = this.model.get('original_product_id');
            $('#resetZoom').show();
            this.line.remove();
        } else {
            var selectedID = data.id;
        }
        $("#results-container div:first-child").each(function (id, data) {
            // reset selected rows
            $(data).removeClass('focusedResultRow');
        });
        $("#result_item_"+ selectedID).addClass('focusedResultRow');
    },

    showMetadata: function(event) {
        var id = this.model.get('id');
        APP.$modal.load('/metadata/'+id, '', function(){
            APP.$modal.modal();
        });
        event.stopPropagation();
    },
    addToCart: function(event) {
        if (UserLoged) {
            var id = this.model.get('id');
            var exist = APP.Cart.filter(function(item) {
                return item.get("product").id == id;
            });
            if (exist.length > 0) {
                alert('Product already in cart!');
            } else {
                APP.Cart.create({'product': {'id':id}},{wait: true});
                $APP.trigger('colorCartFeature', {'original_product_id': this.model.get('original_product_id')});
                $("#result_item_"+ this.model.get('original_product_id')).addClass('cartResultRow');
                $("#result_item_"+ this.model.get('original_product_id')).children('.cart-remove-button').removeClass('hide');
                $("#result_item_"+ this.model.get('original_product_id')).children('.cart-button').addClass('hide');
            }
            showButtonSubPanel();
        } else {
            alert('You need to log in first!');
        }
        event.stopPropagation();
    },

    removeFromCart: function(event) {
        $APP.trigger('removedItemFromCart', {'original_product_id': this.model.get('original_product_id')});
        $APP.trigger('deleteCartItem', {'id': this.model.get('original_product_id')});
        this._removeFromCart(this.model.get('original_product_id'));
        event.stopPropagation();
    },

    _removeFromCart: function(id) {
        $("#result_item_"+ id).removeClass('cartResultRow');
        $("#result_item_"+ id).children('.cart-remove-button').addClass('hide');
        $("#result_item_"+ id).children('.cart-button').removeClass('hide');
    },

    render: function() {
       $(this.el).html(_.template(template, {model:this.model}));
        return this;
    },
});

var template = [
            '<div class="result-item" id="result_item_<%= model.get("original_product_id") %>">',
            '<img class="result-img" src="/thumbnail/<%= model.get("id") %>/mini/" />',
            '<div class="result-item-info">',
              '<p><%= model.get("productName") %></p>',
            '</div>',
            '<div class="result-item-info-date">',
              '<p><%= model.get("product_date") %></p>',
            '</div>',
            '<div class="cloud-cover"><p>',
              '<% if(model.get("cloud_cover") != -1) { %><%= model.get("cloud_cover") %>%',
              '<% } else { %>UNK',
              '<% } %>',
            '</p></div>',
            '<span class="button metadata-button btn btn-default" data-title="View Metadata"><i class="icon-list-alt"></i></span>',
            '<span class="button cart-button btn btn-default" data-title="Add to Cart"><i class="icon-shopping-cart"></i></span>',
            '<span class="button cart-remove-button btn btn-danger hide" data-title="Remove From Cart"><i class="icon-remove"></i></span>',
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
        $APP.on('deleteCartItem', $.proxy(this.deleteItem, this));
    },

    deleteItem: function(event, data) {
        var exist = APP.Cart.find(function(item) {
            return item.get('product').original_product_id == data.id;
        });
        if (exist) {
            exist.destroy({wait: true});
        }
        if (APP.Cart.length-1==0) {
            // If cart is empty after item has been removed then hide bottom panel button
            hideButtonSubPanel();
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
        $APP.trigger('SearchCartLayer_addFeatures', {
                'data': this.collection.models
            });
        if(APP.Cart.length==0) {
            hideButtonSubPanel();
        }
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
        $APP.trigger('removedItemFromCartUpdateResults', {'original_product_id': this.model.get('product').original_product_id});
        $APP.trigger('deleteCartItem', {'id': this.model.get('product').original_product_id});
    },
    render: function() {
       $(this.el).html(_.template(templateCart, {model:this.model}));
        return this;
    }
});


var templateCart = [
        '<div class="cart-item">',
          '<img src="/thumbnail/<%= model.get("product").id %>/mini/" />',
          '<div class="cart-item-info">',
            '<p><%= model.get("product").productName %></p>',
          '</div>',
          '<div class="cart-item-info-date">',
            '<p><%= model.get("product").product_date %></p>',
          '</div>',
          '<div class="cart-item-buttons">',
              '<span class="button metadata-button btn btn-default" data-toggle="tooltip" data-title="View Metadata"><i class="icon-list-alt"></i></span>',
              '<span class="button delete-button btn btn-danger" data-toggle="tooltip" data-title="Remove From Cart"><i class="icon-remove"></i></span>',
          '</div>',
          '<div class="cart-item-cloud-cover"><p>',
            '<% if(model.get("product").cloud_cover != -1) { %><%= model.get("product").cloud_cover %>%',
              '<% } else { %>UNK',
              '<% } %>',
          '</p></div>',
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