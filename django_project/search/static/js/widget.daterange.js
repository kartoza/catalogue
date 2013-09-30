+function ($) {

  // BUTTON PUBLIC CLASS DEFINITION
  // ==============================

  var DateRange = function (element, options) {
    this.$element = $(element);
    this.options = $.extend({}, DateRange.DEFAULTS, options);

    this.datecount = 0;
    var self=this;
    this.input_element = this.$element.find('input');

    // TODO: we need to support existing daterange records

    // //Initial fill of dr_text - when modifysearch view is loaded
    // this.element.find('.dr_row .dr_input').each(function(index, elem){
    //     //extract date range from the formset
    //     var myDateRange = $(elem).find(':text').map(function(index,elem){return $(elem).val();});
    //     //parse the dates
    //     myStartDate = self._parse_date(myDateRange[0]);
    //     myEndDate = self._parse_date(myDateRange[1]);

    //     var myDateString = self._format_output(myStartDate, myEndDate);
    //     $(this).closest('.dr_row').find('.dr_text').html(myDateString);

    //     //increase datecount
    //     self.datecount++;
    // });
    // $('#id_searchdaterange_set-TOTAL_FORMS').val(self.datecount);
    // $('#id_searchdaterange_set-INITIAL_FORMS').val(self.datecount);

    this._setup_events();
  };

  DateRange.DEFAULTS = {
    dateFormat: 'yy-mm-dd'
  };

  DateRange.prototype._resliver_dateranges = function() {
    // resilver all of the date ranges
    // this is needed because Django expects to have all of the forms in
    // a continuous sequence 0,1,2,3...
    var self = this;
    var total = 0;
    this.$element.find('.date_range_row').each(function(){
        var tmpDateFrom = $(this).find('.date_from').text();
        var tmpDateTo = $(this).find('.date_to').text();
        $(this).empty();
        $(this).append(
            self._dr_input_template(
                total, self._parse_date(tmpDateFrom.trim(),'yy-mm-dd'), self._parse_date(tmpDateTo.trim(),'yy-mm-dd'))
            );
        total++;
    });
    $('#id_searchdaterange_set-TOTAL_FORMS').val(total);
    $('#id_searchdaterange_set-INITIAL_FORMS').val(total);

  };

  DateRange.prototype._setup_events = function () {
    var self=this;
    this.$element.find('.date-range').on('click', function () {

      //remove error classes from inputs
      $('#date_to_cg').removeClass('error');
      $('#date_from_cg').removeClass('error');

      if ($("#id_start_datepicker").val() === '') {
        $('#date_from_cg').addClass('error');
        return false
      }

      if ($("#id_end_datepicker").val() === '') {
        $('#date_to_cg').addClass('error');
        return false;
      }


      // get the dates from datepickers and parse them
      var myStartDate = self._parse_date($("#id_start_datepicker").val(),'mm/dd/yy');
      var myEndDate = self._parse_date($("#id_end_datepicker").val(),'mm/dd/yy');


      if(myStartDate && myEndDate) {
          // basic checks for date range
          if (myStartDate <= myEndDate) {
              var in_list;
              in_list = false;
              self.$element.find('.date_range_row').each(function(){
                  var tmpDateFrom = self._parse_date($(this).find('.date_from').text(), 'yy-mm-dd');
                  var tmpDateTo = self._parse_date($(this).find('.date_to').text(), 'yy-mm-dd');
                  if (myStartDate.getTime() === tmpDateFrom.getTime() && myEndDate.getTime() === tmpDateTo.getTime() ){
                      in_list = true;
                  }
              });
              // TODO: find overlapping ranges
              if(in_list){
                  alert('The date range is already in the list.');
              } else {
                  self.$element.append(self._cloneMore(myStartDate, myEndDate));
                  self.datecount++;
              }
          } else {
              alert('Please check the date range.');
          }
      } else {
          alert('Please select both start and end dates.');
      }
      return false;
    });

    //handle remove events...
    this.$element.find('.del_daterange').live('click', function () {
      //remove the date range
      $(this).parent().parent().remove();
      self._resliver_dateranges();
    }
    );
  };

    DateRange.prototype._cloneMore = function(theStartDate, theEndDate){
      var total = $('#id_searchdaterange_set-TOTAL_FORMS').val();
      // prepare template
      var tpl = [
        '<p class="date_range_row">',
          this._dr_input_template(total, theStartDate, theEndDate),
        '</p>'
        ].join('');

      //increase total number of forms
      total++;
      $('#id_searchdaterange_set-TOTAL_FORMS').val(total);
      $('#id_searchdaterange_set-INITIAL_FORMS').val(total);
      return tpl;
    };

    DateRange.prototype._dr_input_template = function (total, theStartDate, theEndDate) {
      var tpl=[
          '<input type="hidden" id="id_searchdaterange_set-'+total+'-start_date" name="searchdaterange_set-'+total+'-start_date" value="'+this._format_date(theStartDate)+'">',
          '<input type="hidden" id="id_searchdaterange_set-'+total+'-end_date" name="searchdaterange_set-'+total+'-end_date" value="'+this._format_date(theEndDate)+'">',
          '<span class="date_from">', this._format_date(theStartDate), '</span>',
          '<span>-</span>',
          '<span class="date_to">', this._format_date(theEndDate), '</span>',
          '<span> <i class="del_daterange icon-trash"></i> </span>'
      ].join('');
      return tpl;
    };

    DateRange.prototype._format_date = function(theDate, theFormat) {
      if (theFormat===undefined) {
          theFormat = this.options.dateFormat;
      }
      return sansa_dateutils.formatDate(theFormat, theDate);
    };

    DateRange.prototype._parse_date = function(theDate, theFormat) {
      if (theFormat===undefined) {
          theFormat = this.options.dateFormat;
      }
      return sansa_dateutils.parseDate(theFormat, theDate);
    };

  $.fn.daterange = function (option) {
    return this.each(function () {
      var $this = $(this);
      // var data = $this.data('bs.button')
      var options = typeof option == 'object' && option;
      this.widget = new DateRange(this, options);
      //if (!data) $this.data('bs.button', (data = new Button(this, options)))

      // if (option == 'toggle') data.toggle()
      // else if (option) data.setState(option)
    });
  };

  $.fn.daterange.Constructor = DateRange;

}(window.jQuery);