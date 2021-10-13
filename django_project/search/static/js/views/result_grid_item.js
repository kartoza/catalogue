define([
    'backbone',
    'underscore',
    'shared',
    'jquery',
    'views/cart_item_collection',
], function (Backbone,_, Shared, $, Cart){
    return Backbone.View.extend({
    tagName: 'div',
    selectedFeatureID: '',
    modal: $('#ajax-modal'),
    // snap: Snap('#svg'),
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
        const targetFeature = searchLayer.getFeatureElementRecordId(selectedID);
        if (targetFeature.onScreen()) {
            const point = targetFeature.geometry.getCentroid();
            const pos = myMap.map.getPixelFromLonLat(new OpenLayers.LonLat(point.x, point.y));
            // this.line = this.snap.line(pos.x, pos.y + 35, pos2.left+2, pos2.top+9);
            this.line.animate({stroke: "#2f96b4", strokeWidth: "4"}, 500);
        }
        Shared.Dispatcher.trigger('focusFeature', {'original_product_id': selectedID});
    },

    blurItem: function() {
        if (typeof this.line != 'undefined') this.line.remove();
        const selectedID = this.model.get('original_product_id');
        if (this.selectedFeatureID == selectedID) {
            Shared.Dispatcher.trigger('highlightSearchRecord', {'original_product_id': selectedID, 'zoom': false});
        } else {
            Shared.Dispatcher.trigger('removeFocusFeature', {'original_product_id': selectedID});
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
        var id = this.model.get('id');
        this.modal.load('/metadata/'+id, '', function(){
            this.modal.modal();
        });
        event.stopPropagation();
    },
    addToCart: function(event) {
        if (UserLoged) {
            const id = this.model.get('id');
            var exist = Cart.filter(function(item) {
                return item.get("product").id == id;
            });
            if (exist.length > 0) {
                alert('Product already in cart!');
            } else {
                Cart.create({'product':id},{wait: true});
                Shared.Dispatcher.trigger('colorCartFeature', {'original_product_id': this.model.get('original_product_id')});
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
       $(this.el).html(_.template(template, {model:this.model}));
        return this;
    },
});
})