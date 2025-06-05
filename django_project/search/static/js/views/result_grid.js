define([
    'jquery',
    'underscore',
    'backbone',
    'shared',
    'collections/cart_item',
    'views/result_grid_item',
    'blockUI',
    'perfectScrollbar'
    ],
    function ($, _, Backbone, Shared, CartItemCollection, ResultGridViewItem) {
    return Backbone.View.extend({
        el: 'body',
        template: _.template($("#side-result-panel").html()),
        cont: '',
        events: {
            'click #searchPrev': 'previous',
            'click #searchNext': 'next',
            'click button.resetZoom': 'resetZoom',
            'click #switchSearchLayer': 'switchSearchLayer',
        },
        blockResultPanel: function() {
            $.blockUI({
                message: '<div class="wrapperloading"><div class="loading up"></div><div class="loading down"></div></div>',
                css: {
                    border: '1px solid #000',
                    background: 'rgba(0, 0, 0, 0.3)',
                    width: '450px',
                    height:'450px'
                }
            });
        },
        unblockResultPanel: function (){
            $.unblockUI();
            
        },

        resetZoom: function() {
            $(APP).trigger('resetZoom');
        },

        switchSearchLayer: function (e) {
            const checked = e.target.checked;
            Shared.Dispatcher.trigger('toggleSearchLayer', checked);
        },

        jumpToPage: function(page) {
            this.blockResultPanel();
            this.collection.jumpToPage(page);
            return false;
        },

        previous: function() {
            this.blockResultPanel();
            this.collection.previousPage();
            return false;
        },

        next: function() {
            this.blockResultPanel();
            this.collection.nextPage();
            return false;
        },

        first: function() {
            this.collection.firstPage();
            return false;
        },

        last: function() {
            this.collection.lastPage();
            return false;
        },

        initialize: function() {
            _.bindAll(this, 'render');
            this.listenTo(this.collection, 'reset sync update', this.render);
            this.cont = $('#results-container');
            Shared.Dispatcher.on('collectionSearch', $.proxy(this.collectionSearch, this));
        },

        clearHTML: function() {
            this.cont.empty();
            $('#searchPrev').hide();
            $('#searchNext').hide();
            $('#SearchShare').hide();
            $('#paginator').html('');
            this.$el.find('#resultsPosition').html('');
        },

        collectionSearch: function (evt, options) {
            this.blockResultPanel();
            this.clearHTML();
            _.extend(this.collection, options);
            this.collection.fetch({
                reset: true,
                error: this.unblockResultPanel,
                success: this.unblockResultPanel
            });
        },

        renderItem: function(item) {
            const view_item = new ResultGridViewItem({
                model: item,
                collection: this.collection
            });

            // Enable permalink
            let permalink =  $('#permalink-control')
            permalink.css('cursor', 'pointer');
            permalink.removeClass('permalink-disabled');
            permalink.attr('data-bs-content', 'Copy the link for this map');
            $('#results-container').append(view_item.render().$el);
            // check if result item if is in cart
            const id = view_item.model.get('id');
            const cart = new CartItemCollection()
            const exist = cart.filter(function(item) {
                return item.get("product").id == id;
            });
            // if it is, color it differently
            if (exist.length > 0) {
                $("#result_item_"+ view_item.model.get('original_product_id')).addClass('cartResultRow');
                $("#result_item_"+ view_item.model.get('original_product_id')).children('.cart-remove-button').show();
                $("#result_item_"+ view_item.model.get('original_product_id')).children('.cart-button').hide();
            }
        },

        _createSelectPaginator: function(current, end) {
            const select = document.createElement("select");
            select.style.width = "50px";
            const self = this;
            select.onchange = function(event) {
                self.jumpToPage(event.target.value);
            };
            let option;
            for (let i = 1; i < end+1; i++) {
                option = document.createElement("option");
                option.setAttribute("value", i);
                option.innerHTML = i;
                select.appendChild(option);
            }
            select.options.selectedIndex = current-1;
            return select;
        },

        _update_pagination_info:function() {
            var cur_pag_el = this.$el.find('#resultsPosition');
            var page_info = this.collection.pageInfo();
            var paginator = this._createSelectPaginator(page_info.current_page, page_info.pages);
            var showing = page_info.limit;
            if (page_info.total < page_info.limit) showing = page_info.total;
            var text = 'Page <span id="paginator"></span> of ' + page_info.pages + ' ('+page_info.total+' records)';
            if (page_info.current_page > 1) {
                $('#searchPrev').show();
            } else {
                $('#searchPrev').hide();
            }
            if (page_info.current_page != page_info.pages) {
                $('#searchNext').show();
            } else {
                $('#searchNext').hide();
            }
            $('#SearchShare').show();
            cur_pag_el.html(text);
            $('#paginator').html(paginator);
            if (page_info.current_page == 1) {
                $('#main-content').prepend('<div class="alert alert-info alert-dismissable alert-search"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>'+page_info.total+' Records Returned. Displaying '+showing+'.</strong></div>');
                window.setTimeout(function () {
                    $(".alert").alert('close');
                }, 6000);
            }
        },

        render: function() {
            if ($('.result-panel').length === 0) {
                this.$el.append(this.template());
                this.delegateEvents()
            }
            this.cont = $('#results-container');
            if (_.size(this.collection.models) != 0) {
                $('.sidebar-result').show();
                Shared.Dispatcher.trigger('sidePanel:openSidePanel', this.collection.models);
                Shared.Dispatcher.trigger('layers:addSearch', this.collection.models);
                const record_html = '<div class="result-items-header">' +
                    '<div class="result-item-info" style="float: left">' +
                    'Product</div><div class="result-item-info-date" style="float: left">Date' +
                    '</div><div class="cloud-cover">Cloud cover</div>' +
                    '</div>'
                const self = this;
                $('#results-container').html('');
                _(this.collection.models).each(function(item){
                    self.renderItem(item);
                },this);
                this._update_pagination_info();
            }

            else {
                const modal = $('#alertNoResult');
                modal.modal('show');
            }
            // $('#results-container').perfectScrollbar( { wheelSpeed: 20, wheelPropogation: true } );
            this.unblockResultPanel();
            return this;
        },
});
})