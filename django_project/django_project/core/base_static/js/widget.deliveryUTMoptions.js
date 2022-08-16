/*
 * deliveryUTMoptions widget - enables users dynamically set product
 * delivery options
 * @author: Igor Crnković <icrni@candela-it.com>
 *
 */

(function($) {
    $.widget("sansa.deliveryUTMOptions",{
	// default options
	options: {
		id: 0,
		data: {}
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
		var elem = this.element;
		elem.attr('id',this.options.id + '_utm');
		elem.attr('name',this.options.id + '_utm');
		_.each(this.options.data, function(utm) {
			var option = new Option(utm[1], utm[0]);
			elem.append(option);
		});
		elem.append( new Option('Geographic WGS84', 4326));
		document.write(elem.prop('outerHTML'));
	},

	//called everytime when accessing element without calling function
	//$('#').dialog({'something':'something else'})
	_init: function(){

	}

	//elem.append( new Option('Geographic WGS84', 4326));

    })//end widget
})(jQuery);