var svgWidth = 800;
var svgHeight = 600;
>>>>>>> e056713e70f3a0e914e8849b9af43f6540e899a4
var svgMargin = {

};

var svgPadding = {

};

function linePlot(state){
    d3.json(`/api/annual_summary/${state}`).then(function (data){
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
    
    d3.json(`/api/monthly_data/${state}`).then(function(data){
        const monthly_data = {
            months: [],
            monthlyCounts: []
        };

        data.forEach(function(d){
            monthly_data.months.push(d.months);
            monthly_data.monthlyCounts.push(d.month_count);
        });
        
        var months = monthly_data.months;
        var monthlyCounts = monthly_data.monthlyCounts;

        console.log(months);
        console.log(monthlyCounts);

        var data = [
            {
                x: months,
                y: monthlyCounts,
                name: "Tornado frequency by Month",
                type: 'bar'
            }
        ];

        var layout = {
            title: {
                text: "Months of Year"
            },
            margin: svgMargin,
            padding: svgPadding,
            width: svgWidth,
            height: svgHeight,
            xaxis: {
                tickmode: "linear"
                // tick0: months[0],
                // dtick: 3,
            }
        };
    
        Plotly.newPlot("monthlyBar", data, layout);
    });
};

function lineCharts(state) {
    d3.json(`/api/tornado_data/${state}`).then(function(data) {
        console.log(data)
        
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
            widths.push(tornado["width_yards"])
            fatalities.push(tornado["fatalities"])
            miles.push(tornado["miles_traveled"])
        });

        console.log(years)

       
        
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

function init(){
    var state = "all";
    linePlot(state);
    barChart(state);
    lineCharts(state);
};

init();

function optionChangedState(selection){
    var state = selection;
    console.log(state)
    linePlot(state);
    barChart(state);
    lineCharts(state);
};
