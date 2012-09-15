$.widget( "linfinity.sansa_datepicker", {
    // default options
    options: {
        date_focus: 'start'
    },

/*
        $("#%(id)s-widget").datepicker({
        minDate: new Date(1970, 1, 1),
        yearRange: "1972:+1",
        dateFormat: 'dd-m-yy',
        maxDate: '+1Y',
        changeMonth: true,
        changeYear: true,
        onChangeMonthYear: function(year, month, inst) {
            debugger;
            myId = "%(id)s";
            if ( myId.substring(0,8) == "id_start")
            {
            $("#%(id)s-widget").datepicker("setDate", "01-" + month + "-" + year);
            }
            else if ( myId.substring(0,6) == "id_end")
            {
            //calculate the last day of the month
            //see http://javascript.about.com/library/bllday.htm
            var myLastDay = new Date(year, month, 0).getDate();
            $("#%(id)s-widget").datepicker("setDate",
                myLastDay + "-" + month + "-" + year);
            }
            // returns a js date object
            var myDate = $("#%(id)s-widget").datepicker("getDate");
            var myDay = myDate.getDate();
            if ( myDay < 10 ) //zero pad the day
            {
            myDay = "0" + myDay;
            }
            //+1 below because js months start at 0
            var myMonth = myDate.getMonth() + 1;
            if ( myMonth < 10 ) //zero pad the day
            {
            myMonth = "0" + myMonth;
            }
            var myYear  = myDate.getFullYear();
            var myTextDate = myDay + "-" + myMonth + "-" + myYear;
            $('#%(id)s').val( myTextDate );
        },
        onSelect: function( theDate, inst)
            {
            check_search_dates();
            $('#%(id)s').val( theDate );
            }
        %(defaultDatePropery)s
        });
    $("#%(id)s-widget").datepicker("setDate", "%(defaultDate)s");
*/
    // the constructor
    _create: function() {
        var self=this;

        //update options from html5data
        var mydate_focus = this.element.data('date_focus');
        if (mydate_focus) {
            this.options.date_focus = mydate_focus;
        }

        var myDatePicker = this.element.datepicker({
        minDate: new Date(1970, 1, 1),
        yearRange: "1972:+1",
        dateFormat: 'dd-m-yy',
        maxDate: '+1Y',
        changeMonth: true,
        changeYear: true,

        onChangeMonthYear: function(year, month, inst) {
            if (self.options.date_focus === 'start') {
                myDatePicker.datepicker("setDate", "01-" + month + "-" + year);
            } else if (self.options.date_focus === 'end') {
                //calculate the last day of the month
                //see http://javascript.about.com/library/bllday.htm
                var myLastDay = new Date(year, month, 0).getDate();
                myDatePicker.datepicker("setDate", myLastDay + "-" + month + "-" + year);
            } else {
                //if date_focus is not set
            }
        }
        });

    }

});