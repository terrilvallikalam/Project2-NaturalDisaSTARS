var myMap = L.map("map", {
    center: [39, -97],
    zoom: 2
  });
  
  // Adding the tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(myMap);
  
  // function changeGradient( {
  //   const gradient = [
  //     "rgba(0, 255, 255, 0)",
  //     "rgba(0, 255, 255, 1)",
  //     "rgba(0, 191, 255, 1)",
  //     "rgba(0, 127, 255, 1)",
  //     "rgba(0, 63, 255, 1)",
  //     "rgba(0, 0, 255, 1)",
  //     "rgba(0, 0, 223, 1)",
  //     "rgba(0, 0, 191, 1)",
  //     "rgba(0, 0, 159, 1)",
  //     "rgba(0, 0, 127, 1)",
  //     "rgba(63, 0, 91, 1)",
  //     "rgba(127, 0, 63, 1)",
  //     "rgba(191, 0, 31, 1)",
  //     "rgba(255, 0, 0, 1)",
  //   ];
  //   myMap.set("gradient", myMap.get("gradient") ? null : gradient);
  // }).addTo(myMap);

  d3.json("/api/tornado_data").then(function(response) {
  
    console.log(response);

    // var latitude = d3.map(response, function(d){return d.latitude;}).keys()
    // var longitude = d3.map(response, function(d){return d.longitude;}).keys()
    // var tornado_num = d3.map(response, function(d){return d.index;}).keys()

    // console.log(tornado_num, latitude, longitude)

    // var combined = latitude.map((element, i) => element.concat(longitude[i]));

    // console.log(combined);

  
    var location = [];
    var tornado_list = [];
  
    for (var i = 0; i < response.length; i++) {

        var latitude = response[i].latitude
        var longitude = response[i].longitude
        var tornado_num = response[i].index

        // console.log(latitude, longitude)

        location.push([latitude, longitude]);
        tornado_list.push(tornado_num);

    };

    console.log(location);

    var tornado = {tornado_list, location}

    console.log(tornado)

    // L.marker(tornado.location)
    //     .addTo(myMap);

    function createMarkers(response) {

      // Pull the "stations" property from response.data.
      var lat = response[i].latitude
      var long = response[i].longitude
      var tornado_n = response[i].index
      loc.push([latitude, longitude]);
      tornado_total.push(tornado_num);

    
      // Initialize an array to hold bike markers.
      var tornadoMarkers = [];
    
      // Loop through the stations array.
      for (var index = 0; index < tornado_total.length; index++) {
        var tornado = tornado_total[index];
    
        // For each station, create a marker, and bind a popup with the station's name.
        var tornadoMarker = L.marker([lat, lon])
          .bindPopup("<h3>" + loc + "<h3><h3>" + tornado + "</h3>");
    
        // Add the marker to the bikeMarkers array.
        tornadoMarkers.push(tornadoMarker);
        createMap(L.layerGroup(tornadoMarkers));
      }}

    var heat = L.heatLayer(location, {
      radius: 20,
      blur: 3,
      //colorscale: "Earth"
    }).addTo(myMap);
  
  });