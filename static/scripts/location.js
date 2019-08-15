var x = document.getElementById("content");
var submitImage = document.querySelector(".submit-pic");
var imageForm = document.querySelector("#role-form");
var position = getLocation();

function sendPosition(data){
    $.ajax({
        url: '/',
        type: "POST",
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json; charset=UTF-8",
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });  
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(getPosition);
} else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function getPosition(position) {
  var longitude = position.coords.longitude; 
  var latitude = position.coords.latitude;
  data = { 
      longitude: longitude,
      latitude: latitude
  }
  sendPosition(data); 
  return data;
}

