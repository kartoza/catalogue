define(['backbone', 'underscore'], function (Backbone, _) {
   return Backbone.Model.extend({
       urlRoot: '/api/searchrecords/',
       idAttribute: 'id',
       url: function () {
           let urlRoot;
           if (_.isFunction(this.urlRoot)) {
               urlRoot = this.urlRoot();
           } else {
               urlRoot = this.urlRoot;
           }
           let id;
           if (typeof this.id === 'undefined') {
               id = '';
           } else {
               id = this.id + '/';
           }
           return urlRoot+id;
       },
   })
});
