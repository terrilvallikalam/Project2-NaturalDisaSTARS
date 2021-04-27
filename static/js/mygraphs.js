// function buildCharts() {
function init(){
    var year = d3.select("select.sel-year").node().value;
    var state = d3.select("select.sel-state").node().value;
    bubbleChart(year, state);
};

function optionChangedYear(selection){
    var year = parseInt(selection);
    var state = undefined;
    chartOptions(year, state);
};

function optionChangedState(selection){
    var state = selection;
    var year = undefined;
    chartOptions(year, state);
};

function chartOptions(year, state){
    var Iyear = year;
    var Istate = state;
    if (Iyear === undefined) {
        Iyear = parseInt(d3.select("select.sel-year").node().value);
    }
    if (Istate === undefined) {
        Istate = d3.select("select.sel-state").node().value;
    }
    bubbleChart(Iyear,Istate);
};

function bubbleChart(selYear, selState) {
    d3.json("/api/tornado_data").then(function(data) {
        console.log(data[0]);
        console.log(selYear);
        console.log(selState);
                
        var yearFilter = data.filter(d=>d.year === selYear);
        console.log(yearFilter);
        var yrStateFilter = yearFilter.filter(d=>d.state == selState);
        
        console.log(yrStateFilter);

        var tornadoNums = [];
        var years = [];
        var magnitudes = [];
        var states = [];
        var widths = [];
        var fatalities = [];
        var miles = [];

        data.forEach(tornado => {
            tornadoNums.push(tornado["tornado_num"])
            years.push(tornado["year"])
            magnitudes.push(tornado["magnitude"])
            states.push(tornado["state"])
            miles.push(tornado["miles_traveled"])
            fatalities.push(tornado["fatalities"])
            widths.push(tornado["width_yards"])
        });

        // Bubble Chart
        var traceBubble = [{
            x: years,
            y: miles,
            text: states,
            mode: 'markers',
            marker: {
                size: miles,
                color: tornadoNums,
                colorscale: "Earth",
            }
        }];

        var layoutBubble = {
            xaxis: {
                title: {
                    text: "Miles Traveled"},
                },
            width: 600,
            height: 400
        };
        Plotly.newPlot("bubble", traceBubble, layoutBubble);

        // Scatter Plot
        var traceScatter = {
            x: magnitudes,
            y: fatalities,
            mode: 'markers',
            type: 'scatter'
        };

        var layoutScatter = {
            xaxis: {
                title: {
                    text: "Tornado Magnitude vs. Fatalities"},
                }
        };

        // Plotly.newPlot("scatter", [traceScatter], layoutScatter);
    });
};

init();
bubbleChart();
