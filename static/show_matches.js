// This function alerts a user when a successful Match has been made
function successfulMatch() {
  $("#successful_match").html("<p>You are now matched</p>")
}

// this function sends the data the server with an ajax calls
function sendUserMatch(evt) {
  evt.preventDefault();
  console.log("sendUserMatch")

  var buttonInputs = {
    // gets the value attribute from the button
    "user_match": ($(this).attr("value"))
  };
  // ajax request to post the input to the server
  $.post("/show_matches", buttonInputs, successfulMatch);
}
// event listener for the match button class

$('.match_button').click(sendUserMatch)
