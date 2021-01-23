$(document).ready(function () {

  // calendar
  var date = new Date();
  var days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
  var months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL",
    "AUG", "SEP", "OCT", "NOV", "DEC"];
  var val = days[date.getDay()] + ", " + months[date.getMonth()] + " " + date.getDate();
  var val2 = date.getHours() + ":" + date.getMinutes();
  $("#date").text(val);
  $("#time").text(val2);
  console.log(val)

  // $(".show_li").click(function() {
  //     window.location = $(this).find("a").attr("href"); 
  //     return false;
  // });

  //  function validateMail() {
  // console.log("Inside email validation...")
  //   var email = document.getElementById("email").value;
  //   var regx = /([a-z][0-9][A-Z]\.-]+)@([a-z][0-9][A-Z]\.\-]+).([a-z]{2,20})$/;

  //    if (regx.test(email) == 0) {
  //    document.getElementById("email_lbl").innerHTML = "Invalid";
  //  }
  // }

  // function validation() {
  //   var name = document.getElementById("name").value;
  //   var email = document.getElementById("email").value;
  //   var password = document.getElementById("password").value;

  //   if (name == ""){
  //     document.getElementById('name_lbl').innerHTML = "Please Enter Valid Name";
  //     return false;
  //   }

  //   if (email == ""){
  //     document.getElementById('email_lbl').innerHTML = "Please Enter Valid Name";
  //     return false;
  //   }

  //   if (password == ""){
  //     document.getElementById('password_lbl').innerHTML = "Please Enter Valid Name";
  //     return false;
  //   }
  // }


  // about us and contact us scrolling
  function scrollToAnchor(aid){
    var aTag = $("a[name='"+ aid +"']");
    $('html,body').animate({scrollTop: aTag.offset().top},'slow');
}

$("#about").click(function() {

   scrollToAnchor('#footer-head');
});

}); 
