define([
    'backbone',
    'underscore',
    'models/result_item'
], function (Backbone, _, ResultItem) {
    var PaginatedCollection = Backbone.Collection.extend({
    initialize: function() {
        _.bindAll(this, 'parse', 'url', 'pageInfo', 'nextPage', 'previousPage');
        typeof(options) !== 'undefined' || (options = {});
        typeof(this.limit) !== 'undefined' || (this.limit = 20);
        typeof(this.offset) !== 'undefined' || (this.offset = 0);
    },
    fetch: function(options) {
        typeof(options) != 'undefined' || (options = {});
        var self = this;
        var success = options.success;
        options.success = function(resp) {
            if (success) {
                success(self, resp);
            }
        };
        options.reset = true;
        return Backbone.Collection.prototype.fetch.call(this, options);
    },
    parse: function (resp) {
        this.nextLink = resp.next;
        this.prevLink = resp.previous;
        this.total    = resp.count || 0;
        var limit  = this.limit || 50;
        var offset = 0;

        if (this.prevLink) {
            var prevParams = new URL(this.prevLink, window.location.origin).searchParams;
            limit  = parseInt(prevParams.get('limit'))  || limit;
            offset = (parseInt(prevParams.get('offset')) || 0) + limit;
        } else {
            if (this.nextLink) {
                var nextParams = new URL(this.nextLink, window.location.origin).searchParams;
                limit = parseInt(nextParams.get('limit')) || limit;
            }
            offset = 0;
        }

        this.limit  = limit;
        this.offset = offset;

        return resp.results;
    },
    url: function() {
        urlparams = {
            offset: this.offset,
            limit: this.limit
        };
        urlparams = $.extend(urlparams, this.filter_options);
        if (this.sort_field) {
            urlparams = $.extend(urlparams, {
                sort_by: this.sort_field
            });
        }
        var urlRoot;
        if (_.isFunction(this.urlRoot)) { urlRoot = this.urlRoot(); } else { urlRoot = this.urlRoot; }

        return urlRoot + '?' + $.param(urlparams);
    },
    pageInfo: function() {
        var info = {
            total: this.total,
            offset: this.offset,
            limit: this.limit,
            pages: Math.ceil(this.total / this.limit),
            current_page: (this.offset / this.limit) + 1,
            prev: false,
            next: false
        };

        var max = Math.min(this.total, this.offset + this.limit);

        if (this.total == this.pages * this.limit) {
            max = this.total;
        }

        info.range = [(this.offset + 1), max];

        if (this.offset > 0) {
            info.prev = (this.offset - this.limit) || 1;
        }

        if (this.offset + this.limit < info.total) {
            info.next = this.offset + this.limit;
        }

        return info;
    },
    nextPage: function (options) {
        if (!this.nextLink) { return false; }
        options = _.extend({ reset: true, url: this.nextLink }, options || {});
        return this.fetch(options);
    },
    previousPage: function (options) {
        if (!this.prevLink) { return false; }
        options = _.extend({ reset: true, url: this.prevLink }, options || {});
        return this.fetch(options);
    },

    firstPage: function(){
        this.offset = 0;
        return this.fetch();
    },

    lastPage: function(){
        var info = this.pageInfo();
        this.offset = (info.pages - 1) * info.limit;
        return this.fetch();
    },

    jumpToPage: function(page) {
        var info = this.pageInfo();
        this.offset = (page - 1) * info.limit;
        return this.fetch();
    }

});
   return PaginatedCollection.extend({

       urlRoot: function() {
           return '/api/search-results/'+ guid +'/';
       },
       model: ResultItem,
       limit: searchresults
   })
});
