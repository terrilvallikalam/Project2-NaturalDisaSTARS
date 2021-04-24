// function buildCharts() {
    d3.json("/api/tornado_data").then(function(data) {
        console.log(data[0]);

        var tornadoNums = [];
        var years = [];
        var magnitudes = [];
        var states = [];
        var widths = [];
        var fatalities = [];

        data.forEach(tornado => {
            tornadoNums.push(tornado["tornado_num"])
            years.push(tornado["year"])
            magnitudes.push(tornado["magnitude"])
            states.push(tornado["state"])
            widths.push(tornado["miles_traveled"])
            fatalities.push(tornado["fatalities"])
        });

        // Bubble Chart
        var traceBubble = [{
            x: tornadoNums,
            y: widths,
            text: states,
            mode: 'markers',
            marker: {
                size: width,
                colorscale: "Earth",
            }
        }];
        var layoutBubble = {
            xaxis: {
                title: {
                    text: "Miles Traveled"},
                }
        };
        Plotly.newPlot("bubble", traceBubble,layoutBubble);

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

        Plotly.newPlot("scatter", traceScatter, layoutScatter);
    });