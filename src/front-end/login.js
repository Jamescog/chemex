//hide some elements
$("#forgot").hide();
$("#signup").hide();
$("#account").hide();
$("#error").hide();

//validate email
$("#emailcheck").hide();
$("#email").blur(function () {
  let val = $(this).val();
  let exist = val.indexOf("@");
  if (exist === -1) {
    $("#emailcheck").text("Please enter valid email");
    $("#emailcheck").show();
  } else {
    $("#emailchek").hide();
  }
});

//validate password
$("#passcheck").hide();
$("#password").blur(function () {
  let val = $(this).val();
  if (val.length < 6) {
    $("#passcheck").text("Password is less than 6 character!");
    $("#passcheck").show();
  }
});

//make an AJAX call
$("#submit").click(function () {
  let loginInfo = {
    email: $("#email").val(),
    password: $("#password").val(),
  };

  const header = {
    "Content-Type": "application/json",
  };

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/api/v1/auth/login",
    headers: header,
    data: JSON.stringify(loginInfo),
    success: function (data) {
      let access = data.user.access;
      localStorage.setItem("Authorization", "Bearer " + access);
      $(location).attr("href", "post.html");
    },
    error: function (xhr) {
      let msg = xhr.responseJSON.msg;
      if (msg == "Wrong password") {
        $("#error").text(msg);
        $("#error").show();
        $("#forgot").show();
        $("#forgot").click(function () {
          window.location.href = "reset.html?email=" + $("#email").val();
        });
      } else if (msg === "No account with given email") {
        $("#submit").hide();
        $("#error").text(msg);
        $("#error").show();
        $("#signup").show();
      }
    },
  });
});
