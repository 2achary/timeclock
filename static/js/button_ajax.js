$( "#total-time-today" ).bind( "click", function() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {

        if(request.readyState === 4 && request.status === 200) {
            var res = request.responseText;
            $('#table').hide();
            document.getElementById( "feedback" ).innerHTML = res;
        }
    };
    request.open('GET', 'http://localhost:5000/total_time_today');
    request.send();
});

$( "#clockin" ).bind( "click", function() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {

        if(request.readyState === 4 && request.status === 200) {
            var alertMessage = request.responseText;
            document.getElementById("feedback").innerHTML = alertMessage;
        }
    };
    request.open('GET', 'http://localhost:5000/in');
    request.send();
});

$( "#clockout" ).bind( "click", function() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {

        if(request.readyState === 4 && request.status === 200) {
            var alertMessage = request.responseText;
            document.getElementById("feedback").innerHTML = alertMessage;
        }
    };
    request.open('GET', 'http://localhost:5000/out');
    request.send();
});

$("#total-time-this-week").bind( "click", function() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {

        if(request.readyState === 4 && request.status === 200) {
            var res = JSON.parse(request.responseText);
            $('#table').show();
            myTable = document.getElementById("table");
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
            myTable.innerHTML = entryRows;
        }
    };
  request.open('GET', 'http://localhost:5000/total_time_this_week');
  request.send();
});

$( "#list-entries" ).bind( "click", function() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {

        if(request.readyState === 4 && request.status === 200) {
            var res = JSON.parse(request.responseText);
            $('#table').show();
            myTable = document.getElementById("table");

            var entryRows = "<tr><th>in</th><th>out</th></tr>";
            for (var i=0; i<res.length; i++) {
                var myObj = res[i];
                console.log(myObj);
                var row = "<tr>" ;

                row += "<td>" + myObj.in + "</td>";
                row += "<td>" + myObj.out + "</td>";

                row += "</tr>";
                entryRows += row;

            }
        myTable.innerHTML = entryRows
        }
    };
  request.open('GET', 'http://localhost:5000/list_entries');
  request.send();
});

$( "#edit" ).bind( "click", function() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {

        if(request.readyState === 4 && request.status === 200) {
            var res = JSON.parse(request.responseText);
            $('#table').hide();
        }
    };
  request.open('GET', 'http://localhost:5000/list_entries');
  request.send();
});

$('#date-picker').change(function(){
    console.log($('#date-picker').val());
});