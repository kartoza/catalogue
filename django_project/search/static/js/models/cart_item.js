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
       sync: function(method, model, options) {
              if (!options.noCSRF) {
                  const beforeSend = options.beforeSend;

                  // Set X-CSRF-Token HTTP header
                  console.log(options.beforeSend)
                options.beforeSend = function(xhr) {
                    if (csrfToken) { xhr.setRequestHeader('X-CSRF-Token', csrfToken); }
                  if (beforeSend) { return beforeSend.apply(this, arguments); }
                };
              }
            }

   })
});
