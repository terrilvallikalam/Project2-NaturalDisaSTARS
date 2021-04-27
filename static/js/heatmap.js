var myMap = L.map("map", {
    center: [39, -97],
    zoom: 3
  });
  
  // Adding the tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(myMap);
  
  
  d3.json("/api/tornado_data").then(function(response) {
  
    console.log(response);

    var latitude = d3.map(response, function(d){return d.latitude;}).keys()
    var longitude = d3.map(response, function(d){return d.longitude;}).keys()
    var tornado_num = d3.map(response, function(d){return d.index;}).keys()

    console.log(tornado_num, latitude, longitude)

    // var combined = latitude.map((element, i) => element.concat(longitude[i]));

    // console.log(combined);

  
    var location = [];
  
    for (var i = 0; i < response.length; i++) {

        if (i === 'undefined') 

        latitude.drop([i]),
        longitude.drop([i])
        
        else {
        location.push([latitude[i], longitude[i]]);
        }

        var tornado = response[i];

    };

    location = location.slice(0, 374);

    console.log(location);

    // var tornado = {tornado_num, location}

    // console.log(tornado)

    // L.marker(tornado.location)
    //     .addTo(myMap);


    var heat = L.heatLayer(location, {
      radius: 30,
      blur: 5
    }).addTo(myMap);
  
  });