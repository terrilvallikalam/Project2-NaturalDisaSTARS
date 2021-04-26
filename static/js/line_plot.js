var svgWidth = 600;
var svgHeight = 400;
var svgMargin = {

}

var svgPadding = {

}

function linePlot(){
    d3.json("/api/annual_summary").then(function (data){
        console.log(data);
        d3.select("linePlot").selectAll("svg")
            .attr("viewBox", `0, 0, ${svgWidth}, ${svgHeight}`)
        const tornadoData = {
            years: [],
            tornSum: [],
            injuries: [],
            fatalities: []
        };

        data.forEach(d => {
            tornadoData.years.push(d.year);
            tornadoData.tornSum.push(d.tornado_sum);
            tornadoData.injuries.push(d.injuries);
            tornadoData.fatalities.push(d.fatalities);
        });

        var years = tornadoData.years;
        var tornadoSum = tornadoData.tornSum;
        var injuries = tornadoData.injuries;
        var fatalities = tornadoData.fatalities;

        console.log(years[0]);

        var tornados = {
            x: years,
            y: tornadoSum,
            name: "Tornados",
            type: 'scatter'
        };
        
        var injuries = {
            x: years,
            y: injuries,
            name: "Injuries",
            type: 'scatter'
        };

        var fatalities= {
            x: years,
            y: fatalities,
            name: "Fatalities",
            type: 'scatter'
        };

        var layout = {
            title: {
                text: "Annual Totals"
            },
            margin: svgMargin,
            padding: svgPadding,
            width: svgWidth,
            height: svgHeight,
            xaxis: {
                tickmode: "linear",
                tick0: years[0],
                dtick: 9,
            }
        };
        
        var data = [tornados, injuries, fatalities];
        
        Plotly.newPlot('linePlot', data, layout);
    });
};

linePlot();