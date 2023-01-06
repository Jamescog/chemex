const params = new URLSearchParams(window.location.search);
const category = params.get("category");
$.ajax({
  url: "http://127.0.0.1:5000/api/v1/category/" + category,
  type: "GET",
  contentType: "application/json",
  success: function (response) {
    $("#type").text(category);
    let res = Object.values(response);
    $.each(res, function (index, tutorial) {
      // Append a card element to the div with class "container"
      $(".container").append(
        `<div class="card mb-3">
           <div class="card-body">
             <h3 class="card-title">${tutorial.title}</h3>
             <p class="card-text">Author: ${tutorial.author}</p>
             <p class="card-text">Time Created: ${tutorial.duration}</p>
             <p class="card-text">${tutorial.description}</p>
             <button class="btn btn-primary" data-id="${tutorial.id}">Read More</button>
           </div>
         </div>`
      );

      // Attach a click event handler to the button
      $(".btn").on("click", function () {
        // Get the tutorial ID from the button's data-id attribute
        var tutorialId = $(this).data("id");
        // Redirect to the "post.html" page with the tutorial ID as a parameter
        window.location.href = "post.html?postId=" + tutorialId;
      });
    });
  },
  error: function (error) {
    alert("error");
  },
});
