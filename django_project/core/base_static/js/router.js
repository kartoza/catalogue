define(['backbone', 'views/olmap', 'shared'], function (Backbone, olmap, Shared) {

    return Backbone.Router.extend({
        parameters: {},
        searchHistory: [],
        routes: {
            "": "toMap"
        },
        initialize: function () {
            let self = this;
            this.defaultFiltersExist = false;
            this.defaultFiltersParam = '';
            this.map = new olmap();
            this.eventsConnector = new EventsConnector();

        },
    })




})