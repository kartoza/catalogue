define([
    'backbone',
    'underscore',
    'shared',
    'jquery',
    'collections/cart_item',
], function (Backbone,_, Shared, $, CartItemCollection){
    return Backbone.View.extend({
    selectedFeatureID: '',
    // modal: $('#ajax-modal'),
    // snap: Snap('#svg'),
    events: {
        'click .metadata-button': 'showMetadata',
        'click .cart-button': 'addToCart',
        'click .cart-remove-button': 'removeFromCart',
        'click': 'highlightResultItem',
        'click img': 'imagePopover',
        'mouseenter': 'focusItem',
        'mouseleave': 'blurItem',
        'mouseleave span': function() {console.log('test');},
    },
    initialize: function() {
        _.bindAll(this, 'render');
        Shared.Dispatcher.on('highlightResultItem', $.proxy(this.highlightResultItem, this));
        Shared.Dispatcher.on('removedItemFromCartUpdateResults', $.proxy(this.removedItemFromCartUpdateResults, this));
        this.expanded = false;
    },

    imagePopover: function(event) {
        if (typeof varPopover == 'undefined') varPopover = [{'id': 0}];
        if (varPopover[0].id == $(event.currentTarget).parent()[0].id) {
            $(event.currentTarget).parent().popover('hide');
            varPopover = [{'id': 0}];
        } else {
            if (varPopover[0].id != 0) varPopover.popover('destroy');
            const src = event.currentTarget.src.replace('mini', 'large');
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
        const selectedID = this.model.get('original_product_id');
        const pos2 = $("#result_item_" + selectedID).offset();
        // const targetFeature = searchLayer.getFeatureElementRecordId(selectedID);
        // if (targetFeature.onScreen()) {
        //     const point = targetFeature.geometry.getCentroid();
        //     const pos = myMap.map.getPixelFromLonLat(new OpenLayers.LonLat(point.x, point.y));
        //     // this.line = this.snap.line(pos.x, pos.y + 35, pos2.left+2, pos2.top+9);
        //     this.line.animate({stroke: "#2f96b4", strokeWidth: "4"}, 500);
        // }
        Shared.Dispatcher.trigger('layer:focusFeature', selectedID);
    },

    blurItem: function() {
        if (typeof this.line != 'undefined') this.line.remove();
        const selectedID = this.model.get('original_product_id');
        if (this.selectedFeatureID == selectedID) {
            Shared.Dispatcher.trigger('highlightSearchRecord', {'original_product_id': selectedID, 'zoom': false});
        } else {
            Shared.Dispatcher.trigger('layer:removeFocusFeature', selectedID);
        }
    },

    removedItemFromCartUpdateResults: function(event, data) {
        var exist = this.collection.filter(function(item) {
                return item.get("original_product_id") == data.original_product_id;
            });
        if (exist.length > 0) {
            this._removeFromCart(data.original_product_id);
            Shared.Dispatcher.trigger('removedItemFromCart', {'original_product_id': data.original_product_id});
        }
    },

    highlightResultItem: function(event, data) {
        // if id is not set presume user has clicked in result panel on item
        // if id is set presume user has clicked record on the map
        if (typeof data == 'undefined') {
            Shared.Dispatcher.trigger('highlightSearchRecord', {'original_product_id': this.model.get('original_product_id'), 'zoom': true});
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
        const id = this.model.get('id');
        // $('#ajax-modal').load('/metadata/'+id, '', function(){
        //     $('#ajax-modal').modal();
        // });
        const url = '/metadata/' + id;
        $.ajax({
            type: 'GET',
            url: url,
            success: function (output) {
                console.log(output);
                $("#product-metadata").html(output).show();//now its working
            },
            error: function(output){
            alert("fail");
            }
        });
        event.stopPropagation();
    },
    addToCart: function(event) {
        if (UserLoged) {
            const id = this.model.get('id');
            const cart = new CartItemCollection()
            const exist = cart.filter(function(item) {
                return item.get("product").id == id;
            });
            if (exist.length > 0) {
                alert('Product already in cart!');
            } else {
                cart.create({'product':id},{wait: true});
                Shared.Dispatcher.trigger('colorCartFeature', {'original_product_id': this.model.get('original_product_id')});
                $("#result_item_"+ this.model.get('original_product_id')).addClass('cartResultRow');
                $("#result_item_"+ this.model.get('original_product_id')).children('.cart-remove-button').show();
                $("#result_item_"+ this.model.get('original_product_id')).children('.cart-button').hide();
            }
            showButtonSubPanel();
        } else {
            alert('You need to log in first!');
        }
        event.stopPropagation();
    },

    removeFromCart: function(event) {
        Shared.Dispatcher.trigger('removedItemFromCart', {'original_product_id': this.model.get('original_product_id')});
        Shared.Dispatcher.trigger('deleteCartItem', {'id': this.model.get('original_product_id')});
        this._removeFromCart(this.model.get('original_product_id'));
        event.stopPropagation();
    },

    _removeFromCart: function(id) {
        $("#result_item_"+ id).removeClass('cartResultRow');
        $("#result_item_"+ id).children('.cart-remove-button').addClass('hide');
        $("#result_item_"+ id).children('.cart-button').removeClass('hide');
    },

    render: function() {
        const template = _.template([
            '<div class="result-item" id="result_item_<%= model.get("original_product_id") %>">',
            '<div class="result-image-thumb">',
            '<img class="result-img" style="float: left" src="/thumbnail/<%= model.get("id") %>/mini/" />',
            '</div>',
            '<div class="result-item-info">',
            '<div class="result-item-info-name">',
            '<p><%= model.get("product_name") %></p>',
            '</div>',
            '<div class="result-item-info-date">',
            '<p><%= model.get("product_date") %></p>',
            '</div>',
            '<div class="cloud-cover"><p>',
            '<% if(model.get("cloud_cover") != -1) { %><%= model.get("cloud_cover") %>%',
            '<% } else { %>UNK',
            '<% } %>',
            '</p></div>',
            '</div>',
            '<div class="button-action">',
            '<span class="button metadata-button btn btn-default" data-title="View Metadata"><i class="icon-list-alt"></i></span>',
            '<span class="button cart-button btn btn-default" data-title="Add to Cart"><i class="icon-shopping-cart"></i></span>',
            '<span class="button cart-remove-button btn btn-danger" style="display: none" data-title="Remove From Cart"><i class="fa fa-trash"></i></span>',
            '</div>',
            '</div>'
        ].join(''))
       $(this.el).html(template({"model":this.model}));
        return this;
    },
});
})