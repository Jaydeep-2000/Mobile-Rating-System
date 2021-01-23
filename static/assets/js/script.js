$(document).ready(function () {

    // calendar
    var date = new Date();
    var days = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
      var months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL",
        "AUG", "SEP", "OCT", "NOV", "DEC"];
      var val = days[date.getDay()] + ", " + months[date.getMonth()] + " " + date.getDate();
      var val2 = date.getHours()+":"+date.getMinutes();
      $("#date").text(val);
      $("#time").text(val2);
      console.log(val)


  });
