function getDate() {
  return getDate4DB();
};

function getLastGeoLocation() {
  return loadLocalVar("geolocation");
}

function getDate4DB() {
  var date = new Date();
  var year  = date.getFullYear();
  var month = date.getUTCMonth();
  var day   = date.getUTCDate();
  var hours = date.getUTCHours();
  var min = date.getUTCMinutes();
  var sec = date.getUTCSeconds();
  var millsec = date.getUTCMilliseconds();
  return year+"/"+month+"/"+day+" "+hours+":"+min+":"+sec+"."+millsec;
}

function getLoginGeolocation() {
	//alert("hello world");
  retrieveLocation(insertPosition);
};

//This is called from Submit Form
function getCurrentGeolocation() {
	//alert("hello world in getcurrent");
  retrieveLocation(insertFormPosition);
};

function setFormLocation() {
	//alert("hello world in setform");
  retrieveLocation(insertFormPosition);
};

function retrieveLocation(pCallback) {
    if (navigator.geolocation) {
	//alert("hello world in navigate");
        navigator.geolocation.getCurrentPosition(pCallback);
	//alert( navigator.geolocation.getCurrentPosition(pCallback));
    } else {
	alert("hello universe");
        console.log("Geolocation is not supported by this browser.");
    }
};

function createGeoLocation(pPosition) {
	//alert("hello world in create now");
	//alert(pPosition.coords.latitude + " " + pPosition.coords.longitude);
  return pPosition.coords.latitude+" "+ pPosition.coords.longitude;
};

function insertFormPosition(pPosition) {
  //var vGeoLocation = document.getElementById("currentGeolocation").value;
	//alert("hello world in insert");
  var vGeoLocation = createGeoLocation(pPosition);
  write2value("app_geolocation",vGeoLocation);
  write2value("response_geolocation",vGeoLocation);
  write2value("feedback_geolocation",vGeoLocation);
  write4name2value("geolocation",vGeoLocation);
  saveGeoLocation2LocalStorage(vGeoLocation);
};

function saveGeoLocation2LocalStorage(pGeoLocation) {
  saveLocalVar("geolocation",pGeoLocation);
}


function insertPosition(pPosition) {
	//alert("please say hello alert");
    //var x = document.getElementById("outputgeo");
    //x.innerHTML = "Latitude: " + position.coords.latitude +
    //"<br>Longitude: " + position.coords.longitude;
    //alert("Latitude: "+pPosition.coords.latitude+" Longitude: " + pPosition.coords.longitude);
    //var vGeoLocation = pPosition.coords.latitude+" "+ pPosition.coords.longitude;
    var vGeoLocation= createGeoLocation(pPosition);
    //document.getElementById("currentGeolocation").value = "hello world";
	document.getElementById("geoField").value = vGeoLocation;
	
	//alert("hello world in insertposition");
    //saveLocalVar("geolocation",vGeoLocation);
};

