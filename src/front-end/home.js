$(document).ready(function () {
  // This function will be executed when the document is ready

  function createAnchorList(dictList) {
    // Clear the div with class searchresult
    $(".searchresult").empty();
    // Loop through the list of dictionaries
    for (let i = 0; i < dictList.length; i++) {
      // Get the current dictionary
      let dict = dictList[i];

      // Get the key and value of the dictionary
      let key = dict["key"];
      let value = dict["value"];

      // Create a new div with the text and attribute
      var newDiv = $("<div>", {
        text: value,
        "data-attribute": key,
      }).addClass("filtered");
      // Append the new div to the div with the class "searchresult"
      $(".searchresult").append(newDiv);
    }
  }
  // Send an AJAX GET request to the API server
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/api/v1/recent",
    success: function (response) {
      // Process the response from the server
      let cards = $(".content .card");
      let data = Object.values(response.msg);
      for (let i = 0; i < cards.length; i++) {
        let card = $(cards[i]);
        card.attr("postId", data[i].postId);
        card.find("h5").text(data[i].category);
        card.find("p").text(data[i].title);
        card.find("#duration").text(data[i].duration);
      }

      // Add a "Read More" button to each card when the user hovers over it
      $(".content .card").hover(
        function () {
          $(this)
            .find(".card-footer")
            .append(
              '<button class="btn btn-primary" id="Read">Read More</button>'
            );
        },
        function () {
          // Remove the button when the user moves the mouse away from the card
          $(this).find("#Read").remove();
        }
      );
    },
    error: function () {
      // This function will be executed if the request fails
      // Do something here
    },
  });

  // Add a click event handler for the "Read More" button
  $(document).on("click", "#Read", function () {
    let card = $(this).closest(".card");
    let postId = card.attr("postId");
    let userId = 2;
    window.location.href = "post.html?postId=" + postId + "&userId=" + userId;
  });

  $(".searchbar").one("focusin", function () {
    $.ajax({
      type: "GET",
      url: "http://127.0.0.1:5000/api/v1/search",
      success: function (response) {
        // get the response of the server
        let dictionary = response.msg;

        //add function that handle the searching
        function searchDictionary(string) {
          // Create an empty list to store the search results
          let searchResults = [];

          // Loop through all the keys in the dictionary
          for (let key in dictionary) {
            // Get the second value of the tuple (the search string)
            let searchString = dictionary[key][1];

            // Check if the search string contains the input string
            if (searchString.includes(string)) {
              // Add the key and the first value of the tuple to the search results list
              searchResults.push({
                key: key,
                value: dictionary[key][0],
              });
            }
          }

          // Return the list of search results
          return searchResults;
        }

        //bind event listner
        let keystrokeCount = 0;

        $(".searchbar").on("keydown", function () {
          // Increment the keystroke counter
          keystrokeCount++;

          // Get the input value
          let input = $(this).val();

          // Search the dictionary and display the results if the keystroke count is 3 or more
          if (input.length >= 3) {
            let searchDictionaryresult = searchDictionary(input);
            if (searchDictionaryresult.length > 0) {
              createAnchorList(searchDictionaryresult);
            } else {
              $(".searchresult").empty();
            }
          } else {
            $(".searchresult").empty();
          }
        });
      },
      error: function (error) {
        console.log(error.msg);
      },
    });
  });
  $(".redirect").click(function () {
    // get the text of the clicked menu item
    let text = $(this).text();

    // redirect to the category page and pass the text as a parameter
    window.location.href = `category.html?category=${text}`;
  });
});
