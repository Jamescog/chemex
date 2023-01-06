$(document).ready(function () {
  $("#reset").submit(function (event) {
    event.preventDefault();
    let formInput = {
      nickname: $("#secretQuestion1").val(),
      city: $("#secretQuestion2").val(),
      teacher: $("#secretQuestion3").val(),
      email: "emanuel@gmail.com",
    };

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:5000/api/v1/auth/reset/check",
      data: JSON.stringify(formInput),
      contentType: "application/json",
      success: function (response) {
        window.location.href = "change_password.html?email=" + response.old;
      },
      error: function (error) {
        alert(error.responseJSON.msg);
        window.location.href = "index.html";
      },
    });
  });
});
