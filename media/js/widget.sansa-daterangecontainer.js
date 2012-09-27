$.widget( "linfinity.sansa_daterangecontainer", {
    // default options
    options: {
        dateFormat: 'yy-mm-dd',
        currentDate: new Date()
    },

    // the constructor
    _create: function() {
        var self=this;
        this.input_element = this.element.find('input');

    this.element.find('.dr_row').live('click', function(){
        $(this).toggleClass('selected');
    });

    //Initial fill of dr_text - when modifysearch view is loaded
    this.element.find('.dr_row .dr_input').each(function(index, elem){
        //extract date range from the formset
        var myDateRange = $(elem).find(':text').map(function(index,elem){return $(elem).val();});
        //the dates passwd in are y-m-d so we need to switch them around to display as d-m-y
        myStartDate = self._parse_date(myDateRange[0]);
        myEndDate = self._parse_date(myDateRange[1]);

        var myDateString = self._format_output(myStartDate, myEndDate);
        $(this).closest('.dr_row').find('.dr_text').html(myDateString);
    });

    $('#dr_add').live('click', function() {
        // get the start date and zero pad day and month
        var myStartDate = self._parse_date($("#id_start_datepicker").val(),'dd-mm-yy');
        var myEndDate = self._parse_date($("#id_end_datepicker").val(),'dd-mm-yy');

        if(myStartDate && myEndDate) {
            if (myStartDate <= myEndDate) {
                var in_list;
                in_list = false;
                self.element.find('.dr_text').each(function(){
                    if($(this).text() == self._format_output(myStartDate, myEndDate)){
                        in_list = true;
                    }
                });
                // TODO: find overlapping ranges
                if(in_list){
                    alert('The date range is already in the list.');
                } else {
                    self.element.append(self._cloneMore(myStartDate, myEndDate));
                }
            } else {
                alert('Please check the date range.');
            }
        } else {
            alert('Please select both start and end dates.');
        }
        return false;
      });

      $('#dr_del').live('click', function(){
        $('.dr_row.selected').each(function(){
          // Has the cb for deletion ?
          if($(this).find('input[type=checkbox]').length) {
            $(this).find('input[type=checkbox]').attr('checked', 'checked');
            $(this).hide('slow');
          } else {
            $(this).hide('slow', function(){
              $(this).remove();
            });
          }
        });
      });
    },

    _cloneMore:function(theStartDate, theEndDate){
        var total = $('#id_searchdaterange_set-TOTAL_FORMS').val();

        var tpl = [
        '<div class="dr_row">',
        '<div class="dr_input">',
            '<label for="id_searchdaterange_set-'+total+'-start_date">Start date:</label>',
            '<input type="text" id="id_searchdaterange_set-'+total+'-start_date" name="searchdaterange_set-'+total+'-start_date" value="'+this._format_date(theStartDate)+'">',
            '<label for="id_searchdaterange_set-'+total+'-end_date">End date:</label>',
            '<input type="text" id="id_searchdaterange_set-'+total+'-end_date" name="searchdaterange_set-'+total+'-end_date" value="'+this._format_date(theEndDate)+'">',
        '</div>',
        '<div class="dr_text" title="Click to select.">'+this._format_output(theStartDate, theEndDate)+'</div>',
        '</div>'].join('');

        //increase total number of forms
        total++;
        $('#id_searchdaterange_set-TOTAL_FORMS').val(total);
        $('#id_searchdaterange_set-INITIAL_FORMS').val(total);
        return tpl;
    },

    _format_date: function(theDate, theFormat) {
        if (theFormat===undefined) {
            theFormat = this.options.dateFormat;
        }
        return $.datepicker.formatDate(theFormat, theDate);
    },
    _parse_date: function(theDate, theFormat) {
        if (theFormat===undefined) {
            theFormat = this.options.dateFormat;
        }
        return $.datepicker.parseDate(theFormat, theDate);
    },
    _format_output: function(theStartDate, theEndDate){
        return this._format_date(theStartDate,'dd-mm-yy') + " : " + this._format_date(theEndDate,'dd-mm-yy');
    }
});
