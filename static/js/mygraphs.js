// New Code
// function buildCharts() {
console.log(l)
    function init(){
        var state = 'all'
        // var state = d3.select("select.sel-state").node().value;
        bubbleChart(state);
    };
    function optionChangedState(selection){
        var state = selection;
        bubbleChart(state)
    };

    function bubbleChart(state) {
        d3.json(`/api/tornado_data/${state}`).then(function(data) {

            var tornadoNums = [];
            var years = [];
            var magnitudes = [];
            var states = [];
            var widths = [];
            var fatalities = [];
            var miles = [];
            console.log=(data)
            data.forEach(tornado => {
                tornadoNums.push(tornado["tornado_num"])
                years.push(tornado["year"])
                magnitudes.push(tornado["magnitude"])
                states.push(tornado["state"])
                widths.push(tornado["width_yards"])
                fatalities.push(tornado["fatalities"])
                miles.push(tornado["miles_traveled"])
            });
            
            // Line chart
            // Average tornado magnitude per state over time
            var magData = [{
            type: 'scatter',
            x: years,
            y: magnitudes,
            mode: 'lines+markers',
            transforms: [{
                    type: 'aggregate',
                    groups: years,
                    aggregations: [
                    {target: 'y', func: 'avg', enabled: true},
                    ]
                }]
            }]
            magLayout = {
            title: '<b>Average Tornado Magnitude</b>',
            xaxis: {title: 'Years'},
            yaxis: {title: 'Magnitude'},
            height: 600,
            width: 900,
            updatemenus: [{
                    x: 0.85,
                    y: 1.15,
                    xref: 'paper',
                    yref: 'paper',
                    yanchor: 'top',
                    active: 0,
                    showactive: false,
            }]
            }
            Plotly.newPlot('myBarChart', magData, magLayout)

            // Line Chart
            // Average length in miles of tornadoes per state over time
            var mileData = [{
            type: 'scatter',
            x: years,
            y: miles,
            mode: 'lines+markers',
            transforms: [{
                    type: 'aggregate',
                    groups: years,
                    aggregations: [
                    {target: 'y', func: 'avg', enabled: true},
                    ]
                }]
            }]
            mileLayout = {
            title: '<b>Average Tornado Length (Miles)</b>',
            xaxis: {title: 'Years'},
            yaxis: {title: 'Length (Miles)'},
            height: 600,
            width: 900,
            updatemenus: [{
                    x: 0.85,
                    y: 1.15,
                    xref: 'paper',
                    yref: 'paper',
                    yanchor: 'top',
                    active: 0,
                    showactive: false,
            }]
            }
            Plotly.newPlot('tornscatter', mileData, mileLayout)
        });
    };
    init();
    bubbleChart();




    // Bubble Chart
            // var avgMagnitudes = magnitudes.avg;
            // var traceBubble = [{
            //     x: years,
            //     y: magnitudes,
            //     text: states,
            //     mode: 'markers',
            //     // transforms: [{
            //     //     type: 'aggregate',
            //     //     groups: years,
            //     //     aggregations: [
            //     //     {target: 'y', func: 'avg', enabled: true},
            //     //     ]
            //     // }],
            //     marker: {
            //         size: avgMagnitudes,
            //         color: states,
            //         colorscale: "Earth",
            //     }
            // }];
            // var layoutBubble = {
            //     xaxis: {
            //         title: {
            //            text: "Miles Traveled"},
            //         },
            //     width: 900,
            //     height: 600
            // };
            // Plotly.newPlot("myBarChart", traceBubble, layoutBubble);

            // var avgMagnitudes = magnitudes.avg;
            // var avgMiles = miles.avg;


            // var traceBar = {
            //     x: years,
            //     y: avgMiles,
            //     name: "Average Miles Traveled",
            //     type: "bar"
            // };

            // var traceLine = {
            //     x: years,
            //     y: avgMagnitudes,
            //     name: "Average Tornado Magnitudes",
            //     type: "bar"
            // };
            
            // var dataCombo = [traceBar, traceLine];

            // var dataLayout = {barmode: 'group'};

            // Plotly.newPlot('myBarChart', dataCombo, dataLayout);