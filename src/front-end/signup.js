//form submission
$("form").submit(function (e) {
  let formInput = {
    firstName: $("#firstName").val(),
    lastName: $("#lastName").val(),
    username: $("#username").val(),
    email: $("#email").val(),
    password: $("#password").val(),
    nickname: $("#secretQuestion1").val(),
    city: $("#secretQuestion2").val(),
    teacher: "#secretQuestion3",
  };
  let header = {
    "Content-Type": "application/json",
  };

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/api/v1/auth/signup",
    headers: header,
    data: JSON.stringify(formInput),
    success: function (data) {
      window.location.replace("login.html");
    },
    error: function (xhr) {
      let msg = xhr.responseJSON.msg;
      if (msg == "Username is already taken") {
        $("#takenuser").text(msg);
        $("#takenemail").hide();
      } else if (msg == "Email is already in use") {
        $("#takenemail").text(msg);
        $("#takenuser").hide();
      }
    },
  });
  e.preventDefault();
});

//cofrim passwod event handler
$("#cfrm").keydown(function () {
  let orginal = $("#password").val();
  if ($("#cfrm").val() !== orginal) {
    $("#samepass").text("Password don't match");
  } else {
    $("#samepass").hide();
  }
});
