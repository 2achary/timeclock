var url_host = '';
var data_type_json = 'json';
var listShown = false;
var userShown = false;

$( document ).ready(function(){
    $(".view_stats").hide();
    $(".users").hide();
    $("#user-form").hide();
})

hideListViews = function(){
    $(".view_stats").hide();
    $("#table").hide();
}

showListViews = function(){
    $(".view_stats").show();
    $("#table").show();
}

hideUserViews = function(){
    $(".users").hide();
    $("#user-form").hide();
}

showUserViews = function(){
    $(".users").show();
    $("#user-form").show()
}


$("#user-button").on("click", function(){

    if (userShown){
        hideUserViews();
        userShown = false;
    } else {
        hideListViews();
        $(".users").show();
        userShown = true;
    }

});

$("#create_user").on("click", function(){
    $(".users").hide();
    $("#user-form").show();
});

$("#list-options").on("click", function(){
    if (listShown) {
        hideListViews();
        listShown = false;
    } else {
        hideUserViews();
        $(".view_stats").show();
        listShown = true;
    }

})

//$("#register_user").on("click", function(){
//    $.ajax({
//        url: 'http://127.0.0.1:5000/register',
//        method: "GET",
//        data: {
//            "username": $("#username").val(),
//            "email": $("#email").val(),
//            "password": $("#password").val(),
//            "verify_password": $("#verify_password").val()
//        },
//        dataType: data_type_json,
//        success: function(data) {
//            if (data.processed) {
//                $("#form-feedback").append(data.response);
//            } else {
//                $("#form-feedback").append(data.errors[0]);
//            }
//        }
//    })
//});

$( "#total-time-today" ).on("click", function() {
    $idNumber = $("#user_id").val()
    if (!$idNumber) {
        $("#feedback").html("Please enter ID Number");
        return
    }
    $.ajax({
        url: url_host + 'total_time_today',
        data: {"user_id": $idNumber},
        dataType: data_type_json,
        success: function(data) {
            $("#table").hide();
            $("#feedback").html("Total hours today: " + data.response.msg);
        },
    });
});


$("#clockin").on("click", function() {
    $idNumber = $("#user_id").val()
    if (!$idNumber) {
        $("#feedback").html("Please enter ID Number");
        return
    }
    $.ajax({
        url: 'in',
        dataType: data_type_json,
        data: {"user_id": $idNumber},
        success: function(data) {
            console.log(data);
            if (data.processed == false) {
                $("#feedback").html("Already clocked in")
            } else {
                var inTime = new Date(data.response.ts);
                var message = "Clocked in at ";
                message += inTime.toLocaleTimeString({timeZone:['America/Chicago']});
                $("#feedback").html(message);
            }
        },
    });
});


$("#clockout").on("click", function() {
    $idNumber = $("#user_id").val()
    if (!$idNumber) {
        $("#feedback").html("Please enter ID Number");
        return
    }
    $.ajax({
        url: url_host + 'out',
        dataType: data_type_json,
        data: {"user_id": $idNumber},
        success: function(data) {
            if (data.processed == false) {
                $("#feedback").html("Not clocked in")
            } else {
                var inTime = new Date(data.response.ts);
                var message = "Clocked out at ";
                message += inTime.toLocaleTimeString({timeZone:['America/Chicago']});
                $("#feedback").html(message);
            }
        },
    });
});


$("#total-time-this-week").on("click", function() {
    $idNumber = $("#user_id").val()
    if (!$idNumber) {
        $("#feedback").html("Please enter ID Number");
        return
    }
    $.ajax({
        url: url_host + 'total_time_this_week',
        data: {"user_id": $idNumber},
        dataType: data_type_json,
        success: function(data) {
            var res = data.response.msg;
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
    $idNumber = $("#user_id").val()
    if (!$idNumber) {
        $("#feedback").html("Please enter ID Number");
        return
    }
    $.ajax({
        url: url_host + 'list_entries',
        dataType: data_type_json,
        data: {"user_id": $idNumber},
        success: function(data) {
            if (data.processed == false){
                console.log("it's false!!!");
                $('#table').show();
                $("#table").append("<tr><td>No entries for today yet.</td></tr>");
                return
            }
            var res = data.response;
            $("#table").show();
            $("#edit-area").hide();
            myTable = $("#table");

            var entryRows = "<tr><th>in</th><th>out</th></tr>";
            for (var i=0; i<res.length; i++) {
                var myObj = res[i];
                console.log(myObj);
                var row = "<tr>" ;

                var inTime = new Date(myObj.in);
                var inTimeLocal = inTime.toLocaleTimeString({timeZone:['America/Chicago']});
                row += "<td>" + inTimeLocal + "</td>";
                if (myObj.out == null){
                    row += "<td></td>"
                } else {
                    var outTime = new Date(myObj.out);
                    var outTimeLocal = outTime.toLocaleTimeString({timeZone:['America/Chicago']});
                    row += "<td>" + outTimeLocal + "</td>";
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

