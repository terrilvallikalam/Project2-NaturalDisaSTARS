function buildCharts() {
    d3.csv("Resources/tornado_clean.csv").then(data =>{
        console.log(data[0]);

        var tornadoNums = [];
        var years = [];
        var magnitudes = [];
        var states = [];


        data.forEach(tornado => {
            tornadoNums.push(tornado["tornado_num"])
            years.push(tornado["year"])
            magnitudes.push(tornado["magnitude"])
            states.push(tornado["state"])
        });
        // console.log(tornadoNums);

        // Bubble Chart
        var traceBubble = [{
            x: years,
            y: tornadoNums,
            text: states,
            mode: 'markers',
            marker: {
                size: magnitudes,
                colorscale: "Earth",
            }
        }];

        var layoutBubble = {
            xaxis: {
                title: {
                    text: "Magnitude"},
                }
        };

        Plotly.newPlot("bubble", traceBubble,layoutBubble);


    })

}

buildCharts();

