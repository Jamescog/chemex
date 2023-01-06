$(document).ready(function () {
  $("#form1").submit(function () {
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
      data: formData,
      contentType: false,
      processData: false,
      success: function (response) {
        console.log(response);
      },
      error: function (error) {
        alert("error");
      },
    });
  });
});
