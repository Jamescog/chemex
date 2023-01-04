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

  // get recent posts from the server
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/api/v1/recent",
    success: function (response) {
      // This function will be executed if the request succeeds
      let obj = Object.values(response.msg);

      // Loop through all cards and add postId attribute
      let num = 0;
      $(".card").each(function () {
        let postId = obj[num].postId;
        $(this).attr("postId", postId);
        num += 1;
      });

      // Loop through all the cards and fill the category
      num = 0;
      $(".card h5").each(function () {
        let category = obj[num].category;
        $(this).text(category);
        num += 1;
      });

      // Loop through all the cards and fill the title
      num = 0;
      $(".card p").each(function () {
        let desc = obj[num].title;
        $(this).text(desc);
        num += 1;
      });

      // Loop through all the cards and fill the time
      num = 0;
      $(".card #duration").each(function () {
        let duraton = obj[num].duration;
        $(this).text(duraton);
        num += 1;
      });

      // Add a "Read More" button to the card when the user hovers over it
      $(".card").hover(
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
      // do something
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
        $(".searchbar").on("keyup", function () {
          // Get the input value
          let input = $(this).val();

          // Store the input value in a variable or data structure
          if (input.length > 3) {
            let searchDictionaryresult = searchDictionary(input);
            if (searchDictionaryresult.length > 0) {
              createAnchorList(searchDictionaryresult);
            }
          }
        });
      },
      error: function (error) {
        console.log(error.msg);
      },
    });
  });
  // var list = [
  //   [
  //     $("<a>", { href: "url1", text: "link1" }),
  //     $("<a>", { href: "url2", text: "link2" }),
  //   ],
  //   [
  //     $("<a>", { href: "url3", text: "link3" }),
  //     $("<a>", { href: "url4", text: "link4" }),
  //   ],
  // ];

  // $(".searchresult").click(function () {
  //   // Loop through the list of lists
  //   $.each(list, function (index, sublist) {
  //     // Create a div element to hold the sublist of anchor elements
  //     var div = $("<div>");

  //     // Loop through the sublist of anchor elements
  //     $.each(sublist, function (index, element) {
  //       // Append the anchor element to the div element
  //       div.append(element);
  //     });

  //     // Append the div element to the searchresult div
  //     $(".searchresult").append(div);
  //   });
  // });
});
