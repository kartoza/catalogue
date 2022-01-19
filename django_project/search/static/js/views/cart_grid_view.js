define([
    'backbone',
    'jquery',
    'shared',
    'views/cart_grid_view_item',
    ],
    function (Backbone, $, Shared, Cart, CartGridViewItem) {
    return  Backbone.View.extend({
        el: $("#cart-container"),
        initialize: function() {
            this.collection.bind('reset', this.render, this);
            this.collection.bind('add', this.render, this);
            this.collection.bind('destroy', this.render, this);
            if (UserLoged) {
                this.collection.fetch({reset: true});
            }
            Shared.Dispatcher.on('deleteCartItem', $.proxy(this.deleteItem, this));
        },

        deleteItem: function(event, data) {
            const exist = Cart.find(function (item) {
                return item.get('product').original_product_id == data.id;
            });
            if (exist) {
                exist.destroy({wait: true});
            }
            if (Cart.length-1==0) {
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
            if(Cart.length==0) {
                hideButtonSubPanel();
            }
            return this;
        },

        renderItem: function(item) {
            var myItem = new CartGridViewItem({
                model:item,
                collection:this.collection
            });
            this.$el.append(myItem.render().el);
        }
})
});
