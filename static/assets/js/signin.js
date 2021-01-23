
$(document).ready(function(){


    //login and signup
    $(".login-form").hide();

// $(".login").css("background", "none");

$(".login").click(function(){
  $(".signup-form").hide();
  $(".login-form").show();
  $(".signup").css("background", "none");
  $(".login").css("background", "#fff");
});

$(".signup").click(function(){
  $(".signup-form").show();
  $(".login-form").hide();
  $(".login").css("background", "none");
  $(".signup").css("background", "#fff");
});

$(".btn").click(function(){
  $(".input").val("");
});
  });