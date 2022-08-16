define(
    [
        'backbone',
        'underscore',
        'shared',
        'jquery',
        'jqueryUi',
        'ol',
    ],
    function (Backbone, _, Shared, $, jqueryUi, ol) {
        return Backbone.View.extend({
            template: _.template($('#map-control-panel').html()),
            locationControlActive: false,
            uploadDataActive: false,
            catchmentAreaActive: false,
            locateView: null,
            closedPopover: [],
            validateDataListOpen: false,
            layerSelectorSearchKey: 'layerSelectorSearch',
            events: {
                'click .search-control': 'searchClicked',
                'click .map-search-close': 'closeSearchPanel',
                'input #layer-selector-search': 'handleSearchInLayerSelector',
                'click #permalink-control': 'handlePermalinkClicked',
                'click #sidebarToggle': 'sidebarToggle'

            },
            initialize: function (options) {
                _.bindAll(this, 'render');
                this.parent = options.parent;
                this.validateDataListOpen = false;
                Shared.Dispatcher.on('mapControlPanel:clickSpatialFilter', this.spatialFilterClicked, this);
                Shared.Dispatcher.on('mapControlPanel:validationClosed', this.validationDataClosed, this);
                Shared.Dispatcher.on('mapControlPanel:thirdPartyLayerClicked', this.thirdPartyLayerClicked, this);
            },
            addPanel: function (elm) {
                elm.addClass('sub-control-panel');
                var mapControlPanel = this.$el.find('.map-control-panel');
                mapControlPanel.append(elm);
            },
            hidePopOver: function (elm) {
                if (!elm.hasClass('sub-control-panel')) {
                    elm = elm.parent();
                }
                for (var i = 0; i < this.closedPopover.length; i++) {
                    this.closedPopover[i].popover('enable');
                    this.closedPopover[i].splice(i, 1);
                }
                elm.popover('hide');
                this.closedPopover.push(elm);
            },

            searchClicked: function (e) {
                if (!this.searchView.isOpen()) {
                    this.hidePopOver($(e.target));
                    this.openSearchPanel();
                }
            },

            render: function () {
                this.$el.html(this.template())
                var layerSelectorSearchValue = Shared.StorageUtil.getItem(this.layerSelectorSearchKey);
                if (layerSelectorSearchValue) {
                    var $layerSelectorSearch = this.$el.find('#layer-selector-search');
                    $layerSelectorSearch.val(layerSelectorSearchValue);
                }
                return this;
            },
            openSearchPanel: function () {
                this.$el.find('.search-control').addClass('control-panel-selected');
                this.searchView.show();
            },
            closeSearchPanel: function () {
                this.$el.find('.search-control').removeClass('control-panel-selected');
                this.searchView.hide();
            },

            sidebarToggle: function (event){
                event.preventDefault();
                document.body.classList.toggle('sidenav-toggled');
                // localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sidenav-toggled'));
            },

        })
    });
