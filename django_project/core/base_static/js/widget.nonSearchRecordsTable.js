/*
 * non search records widget - enables users dynamically add non search records
 * @author: Igor Crnković <icrni@candela-it.com>
 *
 */

(function($) {
    $.widget("sansa.nonSearchRecordsTable",{
	// default options
	options: {
		currency: {},
		records: {}
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
		var self = this;
		var options = this.options;
		var elem = this.element;
		this.currencyElem = document.createElement("select");
        this.currencyElem.setAttribute("id", "currency");
		_.each(options.currency, function(element) {
			var option = new Option(element[1], element[0]);
			$(self.currencyElem).append(option);
		});

		elem.append(this._writeHeader());
		elem.append(this._writeBody());
		this.numProducts = 0;
		this.btnAdd = elem.find('.addNewRow');
		this.btnSave = elem.find('.submitNewRow');
		this.frm = elem.find('.nonsearchForm');
		this.elemTotal = elem.find('.totalPrice');
		this.formVisible = false;
  		this.btnAdd.click(function() {
  			if (self.formVisible) {
  				self._hideForm();
  			} else {
  				self._showForm();
  			}
  		});

  		this.btnSave.click(function() {
  			var product = self.frm.find('.product_desc').val();
  			var price = self.frm.find('.product_price').val();
  			var currency = self.frm.find('select').val();
  			var pattern=/\d+(\.\d{2})?$/;
			if(pattern.test(price))	{
  				self._addProduct(product, price, currency);
  				self._hideForm();
  				self.frm.find('.product_desc').val('');
  				self.frm.find('.product_price').val('');
  				self.frm.find('.product_price').parent().removeClass('error');
  				self.frm.find('.product_price').parent().removeClass('control-group');
  				datachanged = true;
  			} else {
  				self.frm.find('.product_price').parent().addClass('error');
  				self.frm.find('.product_price').parent().addClass('control-group');
  			}
  	 	});

  		if (_.keys(this.options.records).length > 0) {
  			_.each(this.options.records, function(element) {
  				self._addExistingProduct(element.id, element.desc, element.price, element.currency, element.rand_price);
  			});
  			this._calculateTotal();
  		}

  		$(document).on("click", '.deleteRow', function() {
  			datachanged = true;
  			$(this).parent().parent().remove();
  			self._calculateTotal();
  		});
        $('#currency').val('ZAR');
	},

	//called everytime when accessing element without calling function
	//$('#').dialog({'something':'something else'})
	_init: function(){

	},

	_hideForm: function() {
		this.formVisible = false;
		this.frm.addClass('hide');
		this.btnSave.addClass('hide');
		this.btnAdd.html('Add new row');
	},

	_showForm: function() {
		this.formVisible = true;
		this.frm.removeClass('hide');
		this.btnSave.removeClass('hide');
		this.btnAdd.html('Cancel');
	},

	_calculateTotal: function() {
		var total = 0;
		this.element.find('input[name*="_rand_price"]').each(function() {
			total = total + parseFloat($(this).val());
		});
		this.elemTotal.html(total);
	},

	_addProduct: function(product, price, currency) {
		this.numProducts++;
		var self = this;
		$.when($.ajax({
		  dataType: "json",
		  type: "POST",
		  url: '/convertprice/',
		  data: {'currency': currency, 'price': price}
		})).done(function(result) {
			var html = '<tr><td>'+product+'</td><td>'+price+'</td><td>'+currency+'</td><td>'+result.rand_price+'</td>';
			html = html + '<td><input type="hidden" name="'+self.numProducts+'_product" value="'+product+'">';
			html = html + '<input type="hidden" name="'+self.numProducts+'_price" value="'+price+'">';
			html = html + '<input type="hidden" name="'+self.numProducts+'_id" value="0">';
			html = html + '<input type="hidden" name="'+self.numProducts+'_currency" value="'+currency+'">';
			html = html + '<input type="hidden" name="'+self.numProducts+'_rand_price" value="'+result.rand_price+'">';
			html = html + '<input type="hidden" name="productlist" value="'+self.numProducts+'">';
			html = html + '<button class="btn deleteRow" type="button">Delete</button>';
			html = html + '</td></tr>';
			self.element.prepend(html);
			self._calculateTotal();
		});
		// TODO fail
	},

	_addExistingProduct: function(id, product, price, currency, rand_price) {
		this.numProducts++;
		var html = '<tr><td>'+product+'</td><td>'+price+'</td><td>'+currency+'</td><td>'+rand_price+'</td>';
		html = html + '<td><input type="hidden" name="'+this.numProducts+'_product" value="'+product+'">';
		html = html + '<input type="hidden" name="'+this.numProducts+'_price" value="'+price+'">';
		html = html + '<input type="hidden" name="'+this.numProducts+'_currency" value="'+currency+'">';
		html = html + '<input type="hidden" name="productlist" value="'+this.numProducts+'">';
		html = html + '<input type="hidden" name="'+this.numProducts+'_id" value="'+id+'">';
		html = html + '<input type="hidden" name="'+this.numProducts+'_rand_price" value="'+rand_price+'">';
		html = html + '<button class="btn deleteRow" type="button">Delete</button>';
		html = html + '</td></tr>';
		this.element.prepend(html);
	},

	_writeHeader: function() {
		return '<thead><tr><th>Product description</th><th>Price</th><th>Currency</th><th>ZAR</th><th>Remove</th></tr></thead>';
	},

	_writeBody: function() {
		var body = '<tbody id="products"><tr class="hide nonsearchForm">';
		body = body + '<td><input type="text" class="product_desc" style="width: 300px;"></td>';
		body = body + '<td><input type="text" class="product_price" style="width: 100px;"></td>';
		body = body + '<td>' + this.currencyElem.outerHTML + '</td>';
		body = body + '<td></td>';
		body = body + '<td></td>';
		body = body + '</tr><tr>';
		body = body + '<td colspan="3">';
		body = body + '<button type="button" class="btn addNewRow">Add new row</button>';
		body = body + '<button type="button" class="btn hide submitNewRow">Save</button>';
		body = body + '</td>';
		body = body + '<td colspan="2"> Total: R <span class="totalPrice">0</span></td>';
		body = body + '</tr></tbody>';
		return body;
	},

	_writeForm: function() {

	}

    })//end widget
})(jQuery);
