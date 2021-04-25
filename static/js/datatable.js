d3.json("/api/tornado_data").then(function(data) {
    console.log(data[0]);

    $(document).ready(function() {
        $('#dataTable').DataTable();
      });

    var tbody = d3.select("tbody");

// Display the entire dataset as default
    data.forEach(function(report) {
        //console.log(report.state);

        var row = tbody.append('tr');

        Object.entries(report).forEach(function([key, value]) {
            //console.log(key, value);
            var cell = row.append('td');
            cell.text(value);
        });
    });

});