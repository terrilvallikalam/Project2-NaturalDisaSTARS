d3.json("http://127.0.0.1:5000/api/tornado_data_state").then(function(state){
    console.log(state)
    var selectState = d3.select("select.sel-state");
    selectState.selectAll("option")
        .data(state["abbr"])
        .enter()
        .insert("option")
        .attr("value", function(d){
            return d})
        .data(state["state_name"])
        .text(function(d) {
            return d;
        })
});

$(document).ready(function() {
    $(".sel-state").select2({
    placeholder: "Select State",
    allowClear: true,
    width: 'resolve'
    });
});