define(['backbone', 'models/cart_item'], function (Backbone, CartItem) {
   return Backbone.Collection.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/',
    urlRoot: '/api/searchrecords/',
    model: CartItem,
    limit: 100,
    })
});
