/*
 * MapResizer widget - enables users to resize map to arbitary size
 * @author: Dražen Odobašić <dodobasic@gmail.com>
 *
 * Options:
 *
 * map - mandatory, reference to OpenLayers map object
 *
 * scrollTo - if set browser is scrolled to top of the map
 *  - optional, default true
 *
 * map_id - id of div which contains OL map
 *  - optional, default 'map'
 *
 * map_panel_id - id of div containg map tools, scale, ...
 *  - optional, default 'map-panel'
 */

(function($) {
    $.widget("sansa.mapResizer",{
	
	// default options
	options: {
	    'map': null,
	    'scrollTo':true,
	    'map_id':'map',
	    'map_panel_id':'map-panel'
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
	    var self=this;
	    if (!this.options.map){
		$.error('Map object is mandatory');
	    }
	    
	    //calculate minimal right edge for the map
	    this.offset_left = this.element.offset().left;
	    this.right_edge_limit = this.offset_left + this.element.width();

	    //set min_width to parent width and height
	    this.min_width=this.element.width();
	    this.min_height=this.element.height();

	    //set map_panel_height +2 (for borders)
	    this.map_panel_height=this.element.find("#"+this.options.map_panel_id).height()+2;
	    this.map=this.element.find("#"+this.options.map_id);

	    //add toolbox
	    this.element.append(this._toolbox());
	    
	    //this.element.css({'position':'relative'});
	    this.element.resizable({
		minHeight: self.min_height,
		minWidth: self.min_width,
		
		start: function (evt){
		    self.old_width=self.element.width();//store old width
		},
		resize: function (evt){
		    //called during resize
		    self.map.height(self.element.height()-self.map_panel_height);
		    self.map.width(self.element.width());
		},
		stop: function (evt){
		    var new_width=self.element.width();
		    var offset = self.element.offset();
		    
		    var right_edge=offset.left+new_width;
		    if (right_edge < self.right_edge_limit) {
			self._set_dim({top:offset.top,left:self.right_edge_limit-self.min_width},self.min_width,self.element.height());
		    }
		    else {
			var left_offset = new_width-self.old_width;//mirror left side as much as right side == mirror
			self._set_dim({top:offset.top,left:offset.left-left_offset},new_width+left_offset,self.element.height());
		    }
		}
	    });
	    //bind browser window resize
	    $(window).resize(function() {
		var elem = $(this);
		var offset=self.element.offset();
		var windowHeight=elem.height();
		var windowWidth=elem.width();
		//if the browser window is smaller then map, restore map 
		if (self.element.width()>windowWidth || self.element.height()>windowHeight+10) {
		    var left_edge= self.element.parent().offset().left;//find left offset of the parent containter to align map
		    self._set_dim({top:offset.top,left:left_edge},self.min_width,self.min_height);
		}
	    });
	},
	
	//called everytime when accessing element without calling function 
	//$('#').dialog({'something':'something else'})
	_init: function(){

	},
	// resize map and recenter (mandatory for draw feature controls)
	_set_dim: function (offset,width,height){
	    this.element.offset(offset);
	    this.element.width(width);
	    this.map.width(width);
	    this.element.height(height);
	    var map_height=height-this.map_panel_height;
	    this.map.height(map_height);

	    var center = this.options.map.getCenter();
	    var zoom = this.options.map.getZoom();
	    this.options.map.setCenter(center,zoom);
	},

	_toolbox:function(arg){
	    var self=this;

	    var toolbox = $('<div>').attr({
		'id':'resizer_toolbox'
	    });
	    toolbox.css({
		'display':'block',
		'position':'absolute',
		'bottom':'5px',
		'right':'10px'
	    });

	    var fullscreen_image = $('<img>').attr({
		'id':'fullscreen_img',
		'title':'Resize map to full screen',
		'src':"/static/images/view-fullscreen-4.png"
	    });

	    fullscreen_image.bind('click', function (evt){
		var H=$(window).height();
		var W=$(window).width();
		var offset=self.element.offset();
		//hardcoded decrements, to avoid browser horizontal scroll bar
		self._set_dim({top:offset.top,left:5},W-15,H-10);
		//scroll window to the top of the map
		if (self.options.scrollTo){
		    $(window).scrollTop(offset.top);
		}
	    });

	    var restore_image = $('<img>').attr({
		'id':'fullscreen_img',
		'title':'Restore map to original size',
		'src':"/static/images/view-restore-2.png"
	    });

	    restore_image.bind('click', function (evt){
		var offset=self.element.offset();
		self._set_dim({top:offset.top,left:self.right_edge_limit-self.min_width},self.min_width,self.min_height);
		//scroll window to the top of the map
		if (self.options.scrollTo){
		    $(window).scrollTop(offset.top);
		}
	    });

	    toolbox.append(restore_image);
	    toolbox.append(fullscreen_image);

	    return toolbox
	}

    })//end widget
})(jQuery);

