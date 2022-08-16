+function () {

    "use strict"; // jshint ;_;

    APP.SearchSummary = function (div, options) {
        this.options = options || {};
        this.div = $(div);
        this.data = [
            { 'id': 'ssd1', 'label': 'Satellites', 'data': {}},
            { 'id': 'ssd2', 'label': 'Date Ranges', 'data': {}},
            { 'id': 'ssd3', 'label': 'Search Area', 'data': {}},
            { 'id': 'ssd4', 'label': 'Cloud Cover', 'data': {}},
            { 'id': 'ssd5', 'label': 'Other options', 'data': {}}
        ];
        this.template = [
            '<table class="table table-striped">',
            // iterate each  row
            '<% _.each(context, function(row) { %>',
                // if there is any data it means there is something to show
                '<% if (_.keys(row.data).length > 0) { %>',
                    // display row name
                    '<tr><td><%= row.label %></td><td>',
                    // display each option in new row
                    '<% _.each(row.data, function(text) { %>',
                        '<%= text %><br />',
                    '<% }); %>',
                    '</td></tr>',
                '<% } %>',
            '<% }); %>',
            '</table>'
        ].join('');
        this._initialize();
    };

    APP.SearchSummary.prototype = {

        _initialize: function() {
            // listening on events to fire updates
            $(document).on("listTreeChange", $.proxy(this._handleListTree, this));
            $(document).on("sansaDateRangeChanged", $.proxy(this._handleDateRange, this));
            $('#id_aoi_geometry').on("blur", $.proxy(this._handleAoiGeometry, this));
            $('#id_k_orbit_path').on("blur", $.proxy(this._handlePath, this));
            $('#id_j_frame_row').on("blur", $.proxy(this._handleRow, this));
            $('#id_cloud_mean').on("blur", $.proxy(this._handleCloud, this));
            $('#id_sensor_inclination_angle_start').on("blur", $.proxy(this._handleAngleStart, this));
            $('#id_sensor_inclination_angle_end').on("blur", $.proxy(this._handleAngleEnd, this));
            $('#id_spatial_resolution').on("change", $.proxy(this._handleResolution, this));
            $('#id_band_count').on("change", $.proxy(this._handleBand, this));
            $('#id_free_imagery').on("change", $.proxy(this._handleImagery, this));
            $('#id_panchromatic_imagery').on("change", $.proxy(this._handlePImagery, this));
        },

        _forcePopulateData: function() {
            var e = {};
            $.proxy(this._handleListTree, this);
            $('#date_range').daterange('notify');
            e.target = $('#id_aoi_geometry')[0];
            this._handleAoiGeometry(e);
            e.target = $('#id_k_orbit_path')[0];
            this._handleAoiGeometry(e);
            e.target = $('#id_j_frame_row')[0];
            this._handleRow(e);
            e.target = $('#id_cloud_mean')[0];
            this._handleCloud(e);
            e.target = $('#id_sensor_inclination_angle_start')[0];
            this._handleAngleStart(e);
            e.target = $('#id_sensor_inclination_angle_end')[0];
            this._handleAngleEnd(e);
            e.target = $('#id_spatial_resolution')[0];
            this._handleResolution(e);
            e.target = $('#id_band_count')[0];
            this._handleBand(e);
            e.target = $('#id_free_imagery')[0];
            this._handleImagery(e);
            e.target = $('#id_panchromatic_imagery')[0];
            this._handlePImagery(e);
        },

        _handleListTree: function() {

            var text = '';
            // iterate through each sattelite group
            _.each($('.listTree').data('listTree').selected, function(data) {
                // add bolded satellite groupe name for output
                text = text + '<b>' + data.key + ': </b>';
                _.each(data.values, function(item) {
                    // add each satellite name
                    text = text + ' ' + item.key + ',';
                });
                // remove last comma
                text = text.slice(0, - 1);
                text = text + '<br />';
            });
            //remove last br
            text = text.slice(0, - 7);

            // remove existing
            if (typeof this.data[0].data.listTree != undefined) delete this.data[0].data.listTree;

            // save data
            if (text != '') this.data[0].data.listTree = text;

            // request render of specific element
            this._render();
        },

        _handleDateRange: function(e) {
            var text = '';
            // parse payload from event as json and iterate
            _.each(JSON.parse(e.dates), function(daterange) {
                text = text + daterange.from + ' to ' + daterange.to + ', ';
            });
            // remove last comma
            text = text.slice(0, - 2);

            // remove existing
            if (typeof this.data[1].data.dateRange != undefined) delete this.data[1].data.dateRange;

            // save data
            if (text != '') this.data[1].data.dateRange = text;

            // request render of specific element
            this._render();
        },

        _handleAoiGeometry: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = '<b>Bbox: </b>' + e.target.value;
            }

            // remove existing
            if (typeof this.data[2].data.bbox != undefined) delete this.data[2].data.bbox;

            // save data
            if (text != '') this.data[2].data.bbox = text;

            // request render of specific element
            this._render();
        },

        _handlePath: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = '<b>Path: </b>' + e.target.value;
            }

            // remove existing
            if (typeof this.data[2].data.path != undefined) delete this.data[2].data.path;

            // save data
            if (text != '') this.data[2].data.path = text;

            // request render of specific element
            this._render();
        },

        _handleRow: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = '<b>Row: </b>' + e.target.value;
            }

            // remove existing
            if (typeof this.data[2].data.row != undefined) delete this.data[2].data.row;

            // save data
            if (text != '') this.data[2].data.row = text;

            // request render of specific element
            this._render();
        },

        _handleCloud: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = e.target.value + '%';
            }

            // remove existing
            if (typeof this.data[3].data.cloud != undefined) delete this.data[3].data.cloud;

            // save data
            if (text != '') this.data[3].data.cloud = text;

            // request render of specific element
            this._render();
        },

        _handleAngleStart: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = '<b>Inclination start: </b>' + e.target.value;
            }

            // remove existing
            if (typeof this.data[4].data.anglestart != undefined) delete this.data[4].data.anglestart;

            // save data
            if (text != '') this.data[4].data.anglestart = text;

            // request render of specific element
            this._render();
        },

        _handleAngleEnd: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = '<b>Inclination end: </b>' + e.target.value;
            }

            // remove existing
            if (typeof this.data[4].data.angleend != undefined) delete this.data[4].data.angleend;

            // save data
            if (text != '') this.data[4].data.angleend = text;

            // request render of specific element
            this._render();
        },

        _handleResolution: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = '<b>Spatial resolution: </b>' + $(e.target).find('option:selected').text();
            }

            // remove existing
            if (typeof this.data[4].data.resolution != undefined) delete this.data[4].data.resolution;

            // save data
            if (text != '') this.data[4].data.resolution = text;

            // request render of specific element
            this._render();
        },

        _handleBand: function(e) {
            var text = '';
            // if its not empty create text
            if (e.target.value != '') {
                text = '<b>Band count: </b>' + $(e.target).find('option:selected').text();
            }

            // remove existing
            if (typeof this.data[4].data.band != undefined) delete this.data[4].data.band;

            // save data
            if (text != '') this.data[4].data.band = text;

            // request render of specific element
            this._render();
        },

        _handleImagery: function(e) {
            var text = '';
            // if its not empty create text
            if ($(e.target).attr('checked')) {
                text = 'Free images only';
            }

            // remove existing
            if (typeof this.data[4].data.imagery != undefined) delete this.data[4].data.imagery;

            // save data
            if (text != '') this.data[4].data.imagery = text;

            // request render of specific element
            this._render();
        },

        _handlePImagery: function(e) {
            var text = '';
            // if its not empty create text
            if ($(e.target).attr('checked')) {
                text = 'Panchromatic images only';
            }

            // remove existing
            if (typeof this.data[4].data.pimagery != undefined) delete this.data[4].data.pimagery;

            // save data
            if (text != '') this.data[4].data.pimagery = text;

            // request render of specific element
            this._render();
        },

        _render: function() {
            this.div.html( _.template( this.template, { "context": this.data } ) );
        },

        _clearData: function() {
            _.each(this.data, function(row) {
                row.data = {};
            });
        },

        reset: function() {
            this._clearData();
            this._render();
        },

        force: function() {
            this._forcePopulateData();
            this._render();
        }
    };

}(); // anonfunc

