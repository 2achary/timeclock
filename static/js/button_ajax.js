var url_host = '';
var data_type_json = 'json';

$( "#total-time-today" ).on("click", function() {
    $.ajax({
        url: url_host + 'total_time_today',
        dataType: data_type_json,
        success: function(data) {
            $("#table").hide();
            $("#feedback").html(data.msg);
        },
    });
});


$("#clockin").on("click", function() {
   $.ajax({
        url: url_host + 'in',
        dataType: data_type_json,
        success: function(data) {
            console.log(data.msg);
            if (data.msg == false) {
                $("#feedback").html("Already clocked in")
            } else {
                var inTime = new Date(data.msg);
                var message = "Clocked in at ";
                message += inTime.toLocaleTimeString({timeZone:['America/Chicago']});
                $("#feedback").html(message);
            }
        },
    });
});


$("#clockout").on("click", function() {
   $.ajax({
        url: url_host + 'out',
        dataType: data_type_json,
        success: function(data) {
            if (data.msg == false) {
                $("#feedback").html("Not clocked in")
            } else {
                var inTime = new Date(data.msg);
                var message = "Clocked out at ";
                message += inTime.toLocaleTimeString({timeZone:['America/Chicago']});
                $("#feedback").html(message);
            }
        },
    });
});


$("#total-time-this-week").on("click", function() {

    $.ajax({
        url: url_host + 'total_time_this_week',
        dataType: data_type_json,
        success: function(data) {
            var res = data;
            $('#table').show();
            $('#edit-area').hide();
            myTable = $("#table");
            var entryRows = "<tr><th>Day</th><th>Hours</th></tr>";

            var weekdayList = [
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday'
            ];

            for (var i=0; i<weekdayList.length; i++) {

                var row = "<tr>" ;

                if (weekdayList[i] in res) {
                    row += "<td>" + weekdayList[i] + "</td>";
                    row += "<td>" + res[weekdayList[i]] + "</td>";
                } else {
                    row += "<td>" + weekdayList[i] + "</td>";
                    row += "<td>0</td>";
                }
                row += "</tr>";
                entryRows += row;

            }
            $("#feedback").html(res.message);
            myTable.html(entryRows);
        },
    });
});

$( "#list-entries" ).bind( "click", function() {
    $.ajax({
        url: url_host + 'list_entries',
        dataType: data_type_json,
        success: function(data) {
            var res = data;
            $('#table').show();
            $('#edit-area').hide();
            myTable = $("#table");

            var entryRows = "<tr><th>in</th><th>out</th></tr>";
            for (var i=0; i<res.length; i++) {
                var myObj = res[i];
                console.log(myObj);
                var row = "<tr>" ;

                row += "<td>" + myObj.in + "</td>";
                if (myObj.out == null){
                    row += "<td></td>"
                } else {
                    row += "<td>" + myObj.out + "</td>";
                }

                row += "</tr>";
                entryRows += row;
            }
            myTable.html(entryRows);
        },
    });
});

//$( "#edit" ).bind( "click", function() {
//    var request = new XMLHttpRequest();
//    request.onreadystatechange = function () {
//
//        if(request.readyState === 4 && request.status === 200) {
//            var res = JSON.parse(request.responseText);
//            $('#table').hide();
//            $('#edit-area').show();
//        }
//    };
//  request.open('GET', 'http://localhost:5000/list_entries');
//  request.send();
//});
//
//$('#date-picker').change(function(){
//    date_string = $('#date-picker').val();
//    $.ajax({
//        url:'http://localhost:5000/select_day',
//        data: {day:date_string},
//        method: "POST"
//    }).done(function(data){
//        $("#edit-area").append(data)
//    });
//});

