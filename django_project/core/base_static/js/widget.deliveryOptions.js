/*
 * deliveryOptions widget - enables users dynamically set product
 * options
 * @author: Igor Crnković <icrni@candela-it.com>
 *
 */

(function($) {
    $.widget("sansa.deliveryOptions",{
	// default options
	options: {
		id: 0,
		// data example
		// projection: {[id, name]}
		// processing: {[id, name, cost]}
		data: {},
		// must be either projection or processing
		type: '',
		value: ''
	},

	default: {
		'projection': {
			'suffix': '_projection',
			'option': new Option('Geographic WGS84', 4326)
		},
		'processing': {
			'suffix': '_processing',
		}
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
		var options = this.options;
		var elem = this.element;
		var suffix = this.default[options.type].suffix;
		elem.attr('id', options.id + suffix);
		elem.attr('name', options.id + suffix);
		_.each(options.data, function(opt) {
			var option = new Option(opt[1], opt[0]);
			elem.append(option);
		});
		// process widget gets all options in data
		// but we must add secondary option for projection
		if (options.type == 'projection') {
			var requiredOption = this.default[options.type].option;
			elem.append(requiredOption);
		}

		document.write(elem.prop('outerHTML'));
		// select inital value
		if (this.options.value != '')
			$('#'+options.id + suffix).val(this.options.value);

		// for process level widget we must set on change trigger to update cost
		if (options.type == 'processing') {
			$('#'+options.id + suffix).on('change', function() {
				$('#'+options.id+'_cost').html(options.data[this.selectedIndex][2])
				setTotalCost();
			})
		}
		// add widget to APP namespace
		APP['widget_' + options.id + suffix ] = this;
	},

	getCost: function() {
		return this.options.data[$('#'+this.options.id + '_processing').prop('selectedIndex')][2]
	},

	//called everytime when accessing element without calling function
	//$('#').dialog({'something':'something else'})
	_init: function(){

	}

	//elem.append( new Option('Geographic WGS84', 4326));

    })//end widget
})(jQuery);