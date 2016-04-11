// SANSA-EO Catalogue - Search criteria display widget

// Contact : lkleyn@sansa.org.za

// .. note:: This program is the property of the South African National Space
//    Agency (SANSA) and may not be redistributed without expresse permission.
//    This program may include code which is the intellectual property of
//    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
//    license to use any code contained herein which is the intellectual property
//    of Linfiniti Consulting CC.


// __author__ = 'dodobasic@gmail.com'
// __version__ = '0.1'
// __date__ = '24/03/2013'
// __copyright__ = 'South African National Space Agency'


$.widget("linfinity.searchcriteria", {
    // default options
    options: {
    },

    _template:[
    '<span>',
        '<%= collections_text %>',
        '<%= satellite_text %>',
        '<%= sensors_text %>',
        '<%= spectral_group_text %>',
        '<%= license_type_text %>',
        '<%= cloud_mean_text %>',
        '<%= path_text %>',
        '<%= row_text %>',
    '</span>'
    ].join(''),

    // the constructor
    _create: function() {
        var self = this;
        // we need to use proxy to propagate widget context into anonymous function
        $('#search_form').on('change', '#id_collection', $.proxy(this._update_collection_text, this));
        $('#search_form').on('change', '#id_satellite', $.proxy(this._update_satellite_text, this));
        $('#search_form').on('change', '#id_instrumenttype', $.proxy(this._update_sensors_text, this));
        $('#search_form').on('change', '#id_spectral_group', $.proxy(this._update_spectral_group_text, this));
        $('#search_form').on('change', '#id_license_type', $.proxy(this._update_license_type_text, this));

        $('#search_form').on('blur', '#id_cloud_max', $.proxy(this._update_cloud_max_text, this));
        $('#search_form').on('blur', '#id_k_orbit_path', $.proxy(this._update_path_text, this));
        $('#search_form').on('blur', '#id_j_frame_row', $.proxy(this._update_row_text, this));

        this._initial_render();
    },

    _initial_render: function() {
        // update search display, but don't trigger render, we will call it manually
        this._update_collection_text('#id_collection', false);
        this._update_satellite_text('#id_satellite', false);
        this._update_sensors_text('#id_instrumenttype', false);
        this._update_spectral_group_text('#id_spectral_group', false);
        this._update_license_type_text('#id_license_type', false);
        this._update_cloud_max_text('#id_cloud_max', false);
        this._update_path_text('#id_k_orbit_path', false);
        this._update_row_text('#id_j_frame_row', false);
        this._render_string();
    },

    _get_selected: function (target){
        return _.map(
            $(target).find('option:selected'),
            function(selected, i) {
                return $(selected).text();
            }
        );
    },

    _get_int_value: function(target) {
        var tmpVal = $(target).val();
        return parseInt(tmpVal, 10);
    },

    _get_str_value: function(target) {
        return $(target).val();
    },

    _update_collection_text: function (evt, render) {
        var self = this;
        this.collections_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;

        var target = typeof evt !== "string" ? evt.target : evt;
        var selected = this._get_selected(target);

        if (selected.length > 1) {
            this.collections_text = ' <b>Collections:</b> ' + selected.join(', ');
        }
        else if (selected.length === 1) {
            this.collections_text = ' <b>Collection:</b> ' + selected.join(', ');
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _update_satellite_text: function (evt, render) {
        var self = this;
        this.satellite_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;

        var target = typeof evt !== "string" ? evt.target : evt;
        var selected = this._get_selected(target);

        if (selected.length > 1) {
            this.satellite_text = ' <b>Satellites:</b> ' + selected.join(', ');
        }
        else if (selected.length === 1) {
            this.satellite_text = ' <b>Satellite:</b> ' + selected.join(', ');
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _update_sensors_text: function (evt, render) {
        var self = this;
        this.sensors_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;

        var target = typeof evt !== "string" ? evt.target : evt;
        var selected = this._get_selected(target);

        if (selected.length > 1) {
            this.sensors_text = ' <b>Sensors:</b> ' + selected.join(', ');
        }
        else if (selected.length === 1) {
            this.sensors_text = ' <b>Sensor:</b> ' + selected.join(', ');
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _update_spectral_group_text: function (evt, render) {
        var self = this;
        this.spectral_group_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;

        var target = typeof evt !== "string" ? evt.target : evt;
        var selected = this._get_selected(target);

        if (selected.length > 1) {
            this.spectral_group_text = ' <b>Spectral groups:</b> ' + selected.join(', ');
        }
        else if (selected.length === 1) {
            this.spectral_group_text = ' <b>Spectral group:</b> ' + selected.join(', ');
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _update_license_type_text: function (evt, render) {
        var self = this;
        this.license_type_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;

        var target = typeof evt !== "string" ? evt.target : evt;
        var selected = this._get_selected(target);

        if (selected.length > 1) {
            this.license_type_text = ' <b>Licence types:</b> ' + selected.join(', ');
        }
        else if (selected.length === 1) {
            this.license_type_text = ' <b>Licence type:</b> ' + selected.join(', ');
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _update_cloud_max_text: function (evt, render) {
        var self = this;
        this.cloud_max_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;
        var target = typeof evt !== "string" ? evt.target : evt;

        var myValue = this._get_int_value(target);

        if (!_.isNaN(myValue) && myValue !== 100) {
            this.cloud_max_text = ' <b>Cloud mean:</b> ' + myValue;
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _update_path_text: function (evt, render) {
        var self = this;
        this.path_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;
        var target = typeof evt !== "string" ? evt.target : evt;

        var myValue = this._get_str_value(target);

        if (myValue !== '') {
            this.path_text = ' <b>Path (K/orbit):</b> ' + myValue;
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _update_row_text: function (evt, render) {
        var self = this;
        this.row_text = '';

        var triggerRender = typeof render === 'boolean' ? render : true;
        var target = typeof evt !== "string" ? evt.target : evt;

        var myValue = this._get_str_value(target);

        if (myValue !== '') {
            this.row_text = ' <b>Row (J/frame):</b> ' + myValue;
        }

        // update search string
        if (triggerRender === true) {
            this._render_string();
        }
    },

    _render_string: function () {
        this.element.html(_.template(this._template, {
            'collections_text': this.collections_text,
            'satellite_text': this.satellite_text,
            'sensors_text': this.sensors_text,
            'spectral_group_text': this.spectral_group_text,
            'license_type_text': this.license_type_text,
            'cloud_max_text': this.cloud_max_text,
            'path_text': this.path_text,
            'row_text': this.row_text,
            'aoi_text': this.aoi_text
        }));
    }
});
