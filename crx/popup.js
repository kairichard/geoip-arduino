(function(){
  var bkp = chrome.extension.getBackgroundPage()
  var netloc = document.getElementById("netloc");
  var lat = document.getElementById("lat");
  var lng = document.getElementById("lng");
  var data = chrome.extension.getBackgroundPage().response;
  netloc.innerHTML = data.netloc
  lat.innerHTML = data.lat
  lng.innerHTML = data.lng
})();
