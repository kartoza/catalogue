define(['backbone', 'underscore'], function (Backbone, _) {
   return Backbone.Model.extend({
      destroy: function () {
            this.unbind();
            delete this;
        }
   })
});
