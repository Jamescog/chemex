$(document).ready(function () {
  $("#titleError").hide();
  let accessToken = localStorage.getItem("Authorization");

  $("#form1").submit(function (event) {
    event.preventDefault(); // prevent the form from submitting
    const title = $("#tutorial-title").val();
    const description = $("#tutorial-description").val();
    const file = $("#tutorial-file").prop("files")[0];
    const selectedOption = $("#course option:selected").val();
    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("file", file);
    formData.append("category", selectedOption);

    $.ajax({
      url: "http://127.0.0.1:5000/api/v1/create",
      type: "POST",
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", accessToken);
      },
      data: formData,
      contentType: false,
      processData: false,
      success: function (response) {
        console.log(response);
      },
      error: function (error) {
        console.log(error.responseJSON);
        if (error.responseJSON.msg == "Error saving post to database") {
          $("#titleError").show();
        } else if (error.responseJSON.msg == "Token has expired") {
          alert("Your login has expired");
          window.location =
            "/login?next=" + encodeURIComponent(window.location);
        }
      },
    });
  });
});
