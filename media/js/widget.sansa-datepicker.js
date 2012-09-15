$.widget( "linfinity.sansa_datepicker", {
    // default options
    options: {
        dateFormat: 'd-m-yy',
        currentDate: new Date()
    },

    // the constructor
    _create: function() {
        var self=this;

        this.input_element = this.element.find('input');

        //update date_focus options from html5data
        var mydate_focus = this.element.data('date_focus');
        if (mydate_focus) {
            this.options.date_focus = mydate_focus;
        }

        //set default_date
        if (typeof(this.options.currentDate) === 'string') {
            this.current_date = this._parse_date(this.options.currentDate);
        } else {
            this.current_date = this.options.currentDate;
        }

        this.element.datepicker({
            minDate: new Date(1970, 1, 1),
            yearRange: "1972:+1",
            dateFormat: this.options.dateFormat,
            maxDate: '+1Y',
            changeMonth: true,
            changeYear: true,

            onChangeMonthYear: function(year, month, inst) {
                var newDate = null;
                if (self.options.date_focus === 'start') {
                    self._set_date(self._get_first_day_of_month(year, month));
                } else if (self.options.date_focus === 'end') {
                    self._set_date(self._get_last_day_of_month(year, month));
                } else {
                    //if date_focus is not set
                }
            },
            onSelect: function (theDate, inst) {
                self._set_date(self._parse_date(theDate));
            }
        });

        //update widget
        if (this.options.date_focus === 'start') {
            self._set_date(self._get_first_day_of_month(this.current_date.getFullYear(), this.current_date.getMonth()+1));
        } else if (this.options.date_focus === 'end') {
            self._set_date(self._get_last_day_of_month(this.current_date.getFullYear(), this.current_date.getMonth()+1));
        } else {
            //set current date
            this._set_date(this.current_date);
        }
    },

    _set_date: function(theDate) {
        this.current_date = theDate;

        this.element.datepicker('setDate', this.current_date);

        this.input_element.val(this._format_date(this.current_date));
    },

    _format_date: function(theDate) {
        return $.datepicker.formatDate(this.options.dateFormat, theDate);
    },
    _parse_date: function(theDate) {
        return $.datepicker.parseDate(this.options.dateFormat, theDate);
    },

    _get_first_day_of_month:function (year, month) {
        return this._parse_date("1-" + month + "-" + year);
    },
    _get_last_day_of_month:function(year, month){
        //calculate the last day of the month
        //see http://javascript.about.com/library/bllday.htm
        return new Date(year, month, 0);
    }
});
