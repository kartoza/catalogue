require.config({
    urlArgs: "bust=" + (new Date()).getTime(),
    paths: {
        jquery: 'libs/jquery/jquery-3.6.0.min',
        ol: 'libs/openlayers-6.5.0/ol',
        underscore: 'libs/underscore-1.13.1/underscore-min',
        backbone: 'libs/backbone-1.4.0/backbone-min',
        bootstrap: 'libs/bootstrap-5.0.2/js/bootstrap.bundle',
        jqueryUi: 'libs/jquery-ui-1.12.1/jquery-ui.min',
        layerSwitcher: 'libs/ol-layerswitcher/ol-layerswitcher',
        htmlToCanvas: 'libs/htmlToCanvas/html2canvas',
        jqueryTouch: 'libs/jqueryui-touch-punch/jquery.ui.touch-punch.min',
        noUiSlider: 'libs/noUiSlider.15.2.0/nouislider',
        jqueryForm: 'libs/jquery.form.min',
        datetimepicker: 'libs/datepicker/js/bootstrap-datepicker',
        listTree: 'libs/bootstrap-listTree',
        backbonePaginator: 'libs/backbone.paginator',
        blockUI: 'libs/jquery.blockUI',
        perfectScrollbar: 'libs/perfect-scrollbar-0.4.3.with-mousewheel.min'

    },
    shim: {
        ol: {
            exports: ['ol']
        },
        underscore: {
            exports: '_'
        },
        bootstrap: {
            deps: ['jquery']
        },
        backbone: {
            deps: [
                'underscore',
                'bootstrap',
                'jqueryUi',
                'jquery'
            ],
            exports: 'Backbone'
        },
        app: {
            deps: ['backbone']
        },
        layerSwitcher: {
            deps: ['ol'],
            exports: 'LayerSwitcher'
        }
    }
});

require([
    'router',
    'views/olmap',
    'shared',
    'app',
    'bootstrap',
    'jqueryUi',
    'jquery',
], function (Router, olmap, Shared, App, Bootstrap, jqueryUi, $) {
    // Display the map
    Shared.Router = new Router();

    Backbone.history.start({hashChange: true, root: "/search/"});

    $(document).ready(function () {

        $('[data-bs-toggle="tooltip"]').tooltip();
        $('[data-bs-toggle="popover"]').popover();

    })

});
