d3.json("http://127.0.0.1:5000/api/tornado_data_years").then(function(year){
    // console.log(year)
    selectYear = d3.select("select.sel-year")
    selectYear.selectAll("option")
        .data(year.year[0])
        .enter()
        .append("option")
        .text(function(d) {
            return d;
        })
});

d3.json("http://127.0.0.1:5000/api/tornado_data_state").then(function(state){
    // console.log(state)
    var selectState = d3.select("select.sel-state");
    selectState.selectAll("option")
        .data(state["abbr"])
        .enter()
        .append("option")
        .attr("value", function(d){
            return d})
        .data(state["state_name"])
        .text(function(d) {
            return d;
        })
});

$(document).ready(function() {
    $(".sel-year").select2({
    placeholder: "Select Year",
    allowClear: true,
    width: 'resolve'
    });
});

$(document).ready(function() {
    $(".sel-state").select2({
    placeholder: "Select State",
    allowClear: true,
    width: 'resolve'
    });
});