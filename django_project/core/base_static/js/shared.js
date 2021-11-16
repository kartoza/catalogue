/*global define*/
'use strict';

define(['backbone', 'underscore', 'utils/storage',], function (Backbone, _, StorageUtil) {
    return {
        Dispatcher: _.extend({}, Backbone.Events),
        Router: {},
        ClusterSize: 30,
        StorageUtil: new StorageUtil(),
        GetFeatureRequested: false,
        SidePanelOpen: false,
        EndemismList: [],
        CurrentState: {
            FETCH_CLUSTERS: false,
            SEARCH: false,
        },
        EVENTS: {
            SEARCH: {
                HIT: 'search:hit'
            }
        }
    };
});
