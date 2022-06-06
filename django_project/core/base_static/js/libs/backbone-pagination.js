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
    parse: function(resp) {
        this.offset = resp.meta.offset;
        this.limit = resp.meta.limit;
        this.total = resp.meta.total_count;
        return resp.objects;
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
    nextPage: function() {
        if (!this.pageInfo().next) {
            return false;
        }
        this.offset = this.offset + this.limit;
        return this.fetch();
    },
    previousPage: function() {
        if (!this.pageInfo().prev) {
            return false;
        }
        this.offset = (this.offset - this.limit) || 0;
        return this.fetch();
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