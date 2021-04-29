var myMap = L.map("map", {
    center: [39, -97],
    zoom: 2
  });
  
  // Adding the tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(myMap);
  
  
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


    var heat = L.heatLayer(location, {
      radius: 20,
      blur: 3
    }).addTo(myMap);
  
  });