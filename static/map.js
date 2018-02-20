// Ajax call to update the Data

function updateMarkers() {
    $.get("/coffee-info.json",postMarkers);
    console.log("Finished sending AJAX Request");
}

$('#map').on('click', updateMarkers)



// // this function creates the map and centers it
// function initMap() {
//   var coffeeShop = {lat:37.8272, lng:-122.2913}
//   var map = new google.maps.Map(document.getElementById('map'), {
//     zoom: 13,
//     center : coffeeShop
//   });
// }

//this function only creates markers. Takes val(an object) as param
function createMarkers(val) {
  var myLatLng = val
  var marker = new google.maps.Marker({
    map: map,
    draggable: true,
    animation: google.maps.Animation.DROP,
    position: myLatLng
  });
  marker.addListener('click', toggleBounce);
}

// this function calls the createMarker function
function postMarkers(result) {
  var data = result

    $.each(data, function(idx, val) {
        createMarkers(val)
    });
}

function toggleBounce() {
  if (marker.getAnimation() !== null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
};
