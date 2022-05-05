define(['shared', 'backbone', 'underscore', 'jqueryUi', 'jquery'], function (Shared, Backbone, _, JqueryUI, $) {
    return Backbone.View.extend({
        template: _.template($('#side-result-panel').html()),
        className: 'panel-wrapper',
        rightPanel: null,
        sideBar: null,
        isResultPanelOpen: true,
        events: {
            'click .sidebar-result': 'toggleSidePanel',

        },
        initialize: function () {
            // Events
            Shared.Dispatcher.on('sidePanel:openSidePanel', this.openSidePanel, this);
            Shared.Dispatcher.on('sidePanel:closeSidePanel', this.closeSidePanel, this);

        },

        render: function () {
            this.$el.html(this.template());

            // Hide the side panel
            this.rightPanel = this.$el.find('.result-panel');
            this.sideBar = this.$el.find('.sidebar-result');
            this.sideBar.css('display', 'none');
            this.rightPanel.css('display', 'none');

            return this;
        },


        openSidePanel: function (properties) {

            Shared.SidePanelOpen = true;
            this.rightPanel.show('slide', {direction: 'right'}, 200);
            this.sideBar.css('transform', 'translate(0px)');
             this.isResultPanelOpen = true;

        },

        closeSidePanelAnimation: function () {
            this.rightPanel.hide('slide', {direction: 'right'}, 200, function () {
            });
            this.sideBar.css('transform', 'translate(500px)');
        },

        closeSidePanel: function (e) {

            this.closeSidePanelAnimation();
            if(this.isResultPanelOpen){
                this.isResultPanelOpen = false;
            }
        },


        toggleSidePanel: function (){

            if (this.isResultPanelOpen){
                this.closeSidePanel();
            }
            else{
                 this.openSidePanel();
            }


        }




    })
});
