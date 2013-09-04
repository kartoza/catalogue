/*
 * deliveryform widget - enables users dynamically request
 * @author: Dražen Odobašić <dodobasic@gmail.com>
 *
 */

/* this prototype adds "indexOf" function to Array object for browsers
 * which don't implement it. HINT: Internet explorer is the KING!
 */

//This prototype is provided by the Mozilla foundation and
//is distributed under the MIT license.
//http://www.ibiblio.org/pub/Linux/LICENSES/mit.license

if (!Array.prototype.indexOf)
{
  Array.prototype.indexOf = function(elt /*, from*/)
  {
    var len = this.length;

    var from = Number(arguments[1]) || 0;
    from = (from < 0)
         ? Math.ceil(from)
         : Math.floor(from);
    if (from < 0)
      from += len;

    for (; from < len; from++)
    {
      if (from in this &&
          this[from] === elt)
        return from;
    }
    return -1;
  };
}

(function($) {
    $.widget("sansa.deliveryDetails",{
	// default options
	options: {
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
	    //add jQuery UI button
	    this.element.button();
	    //find input element in which we'll store ids of delivery details forms
	    this.main_refs_id = $("#add_form #id_ref_id");
	    this.form=null;
	    this._setup_events();
	},
	
	_setup_events: function(){
	    var self=this;

	    this.element.bind('click',function (evt){
		var order_product = $(this);
		var ref_id = $(this).attr('ref_id');
		var current_refs=self._check_ref();
		var index=current_refs.indexOf(ref_id);
		//append form
		if (index>-1){
		    // if ref already exists
		    order_product.text('Delivery details');
		    //use jQuery to remove all sibling elements
		    // CAUTION: if we change templating we must update this
		    order_product.nextAll().remove();
		    //remove ref_id and update form element
		    current_refs.splice(index,1);
		    self.main_refs_id.val(current_refs.join(','));
		} else {
		    $.ajax({
			url:"/deliverydetailform/"+ref_id+"/",
			success: function (result){
			    self.form=$(result);
			    self.form.insertAfter(order_product);
			    //add 'toggle visibility' button
			    $('<span style="margin-left:10px">Toggle visibility</span>').button().insertAfter(order_product).bind('click',function (evt){
				evt.preventDefault();
				self.form.toggle();
			    });
			    //add ref_id to the main form
			    current_refs.push(ref_id);
			    self.main_refs_id.val(current_refs.join(','));
			    order_product.text('Remove delivery details');
			}
		    });   
		}
		evt.preventDefault();
	    });

	},

	_check_ref:function(){
	    var current_refs=this.main_refs_id.val();
	    //check if current_refs are empty
	    if (current_refs.length){
		current_refs=current_refs.split(',');
	    } else {
		current_refs=[];
	    }
	    return current_refs
	},
	//called everytime when accessing element without calling function
	//$('#').dialog({'something':'something else'})
	_init: function(){

	}

    })//end widget
})(jQuery);