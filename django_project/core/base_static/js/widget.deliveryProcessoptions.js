/*
 * deliveryUTMoptions widget - enables users dynamically set product
 * delivery options
 * @author: Igor Crnković <icrni@candela-it.com>
 *
 */

(function($) {
    $.widget("sansa.deliveryProcessOptions",{
	// default options
	options: {
		id: 0,
		data: {}
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
		var elem = this.element;
		elem.attr('id',this.options.id + '_process');
		elem.attr('name',this.options.id + '_process');
		_.each(this.options.data, function(process) {
			var option = new Option(process[1], process[0]);
			elem.append(option);
		});
		document.write(elem.prop('outerHTML'));
	},

	//called everytime when accessing element without calling function
	//$('#').dialog({'something':'something else'})
	_init: function(){

	}

    })//end widget
})(jQuery);