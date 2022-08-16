define(['backbone', 'underscore'], function (Backbone, _) {
   return Backbone.Model.extend({
       url: '/api/search-records/',
       destroy: function () {
            this.unbind();
            delete this;
        }
   })
});
