// SANSA-EO Catalogue - DatePicker widget

// Contact : lkleyn@sansa.org.za

// .. note:: This program is the property of the South African National Space
//    Agency (SANSA) and may not be redistributed without expresse permission.
//    This program may include code which is the intellectual property of
//    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
//    license to use any code contained herein which is the intellectual property
//    of Linfiniti Consulting CC.


// __author__ = 'dodobasic@gmail.com'
// __version__ = '0.1'
// __date__ = '01/10/2012'
// __copyright__ = 'South African National Space Agency'

// Options:
// - dateFormat (optional)
//      - define JQuery date widget date format
//      - http://docs.jquery.com/UI/Datepicker/formatDate

$.widget( "linfinity.sansa_daterangecontainer", {
    // default options
    options: {
        dateFormat: 'yy-mm-dd'
    },

    // the constructor
    _create: function() {
        // total number of dates in daterangecontainer
        this.datecount = 0;
        var self=this;
        this.input_element = this.element.find('input');

        this.element.find('.dr_row').live('click', function(){
            $(this).toggleClass('selected');
        });

        //Initial fill of dr_text - when modifysearch view is loaded
        this.element.find('.dr_row .dr_input').each(function(index, elem){
            //extract date range from the formset
            var myDateRange = $(elem).find(':text').map(function(index,elem){return $(elem).val();});
            //parse the dates
            myStartDate = self._parse_date(myDateRange[0]);
            myEndDate = self._parse_date(myDateRange[1]);

            var myDateString = self._format_output(myStartDate, myEndDate);
            $(this).closest('.dr_row').find('.dr_text').html(myDateString);

            //increase datecount
            self.datecount++;
        });

        //setup events
        this._setup_events();
        this._check_date_count();
    },

    _setup_events: function () {
        var self=this;
        $('#dr_add').live('click', function() {
            // get the dates from datepickers and parse them
            var myStartDate = self._parse_date($("#id_start_datepicker").val(),'dd-mm-yy');
            var myEndDate = self._parse_date($("#id_end_datepicker").val(),'dd-mm-yy');

            if(myStartDate && myEndDate) {
                // basic checks for date range
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
                        self.datecount++;
                        self._check_date_count();
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
            self.element.find('.dr_row.selected').each(function(){
                // if an row has checkbox it means it was fetched from the database
                if ($(this).find('input[type=checkbox]').length) {
                    $(this).find('input[type=checkbox]').attr('checked', 'checked');
                    $(this).hide('slow');
                } else {
                    // not fetched from the database, added by web app
                    $(this).hide('slow', function(){
                        $(this).remove();
                    });
                }
                //decrease datecount
                self.datecount--;
            });
            self._check_date_count();
        });
    },

    _check_date_count: function () {
        //check the current datecount
        if (this.datecount === 0) {
            //disable remove button
            $('#dr_del img').attr('src','/media/images/selector-remove.gif');
        } else if (this.datecount > 0) {
            //enable remove button
            $('#dr_del img').attr('src','/media/images/selector-remove-active.gif');
        } else {
            throw "datecount less then 0";
        }
    },

    _cloneMore:function(theStartDate, theEndDate){
        var total = $('#id_searchdaterange_set-TOTAL_FORMS').val();
        // prepare template
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
        //format date container date output
        return this._format_date(theStartDate,'dd-mm-yy') + " : " + this._format_date(theEndDate,'dd-mm-yy');
    }
});
