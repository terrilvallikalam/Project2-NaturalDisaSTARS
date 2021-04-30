var svgWidth = 600;
var svgHeight = 400;
var svgMargin = {

};

var svgPadding = {

};

function linePlot(state){
    d3.json(`/api/annual_summary/${state}`).then(function (data){
        console.log(data);
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

function barChart(state){
    d3.json(`/api/losses/${state}`).then(function(data){
        const tornadoDamage = {
            years: [],
            losses: []
        };

        data.forEach(function(d){
            tornadoDamage.years.push(d.year);
            tornadoDamage.losses.push(d.losses);
        });
        
        var years = tornadoDamage.years;
        var losses = tornadoDamage.losses;

        var data = [
            {
              x: years,
              y: losses,
              name: "losses in millions",
              type: 'bar'
            }
          ];

          var layout = {
            title: {
                text: "Damages by Year"
            },
            margin: svgMargin,
            padding: svgPadding,
            width: svgWidth,
            height: svgHeight,
            xaxis: {
                tickmode: "linear",
                tick0: years[0],
                dtick: 3,
            }
        };

        Plotly.newPlot("loss-bar", data, layout);
    });
};

function init(){
    var state = "all";
    linePlot(state);
    barChart(state);
};

init();

function optionChangedState(selection){
    var state = selection;
    console.log(state)
    linePlot(state);
    barChart(state);
};
