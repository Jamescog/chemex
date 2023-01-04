$(document).ready(function () {
  $("#upload").submit(function (event) {
    event.preventDefault();

    let title = $("#tutorial-title").val();
    let description = $("#tutorial-description").val();
    let file = $("#tutorial-file")[0].files[0];
    var selectedOption = $("#course option:selected").val();
    let formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("file", file);
    formData.append("category", selectedOption);

    $.ajax({
      url: "http://127.0.0.1:5000/api/v1/create",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        console.log(response);
      },
      error: function (xhr) {
        let msg = xhr.responseJSON.msg;
        console.log(msg);
      },
    });
  });
});
