define(['backbone'], function (Backbone) {
   return Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata',
        'click span.delete-button': 'delete'
    },

    showMetadata: function() {
        const id = this.model.get('product').id;
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
})
});
