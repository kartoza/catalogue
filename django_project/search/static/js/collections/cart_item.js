define(['backbone', 'models/cart_item'], function (Backbone, CartItem) {
   return Backbone.Collection.extend({
    urlRoot: '/api/search-records/',
    model: CartItem,
    limit: 100,
    })
});
