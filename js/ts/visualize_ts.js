import * as d3 from "https://unpkg.com/d3@5?module";
import {loadCSV} from '../load_csv.js';
import {whoAreWe} from '../us.js';
import {formatScore, formatTimestamp} from './format_csv.js'

export function visualizeTS(){
    //remove existing visualization
    $("#chart").html("");
    
    //build in an option to visualize everything on top of each other (see all games)
    
    //construct an url to the base data
    var ts_baseurl = "https://raw.githubusercontent.com/taetscher/handballStats/master/output_csv/gameProgressions/";
    var team = document.getElementById('dropdown_teams').innerHTML;
    var season = document.getElementById('dropdown_seasons').innerHTML;
    var stat = document.getElementById('dropdown_stats').innerHTML;
    var dataURL = ts_baseurl+team+"/"+season+"/"+stat;
    dataURL = encodeURI(dataURL)
    var title_pieces = stat.split(' ');
    //console.log(title_pieces)
    
    //load the data
    loadCSV(dataURL).then(function (data){
        //reverse the data so it makes sense
        var data = data.reverse();
        
        //format the data so it is plottable
        var x;
        for (x in data){
            //console.log(data[x])
        }
        
        //build in mechanism to check if home or away
        var us = whoAreWe();
        var homeAway = 0;
        var check = stat.toLowerCase().split(' ');
        if (us.includes(check[1])){
            homeAway = 1
        }
        
        // format the data
        data.forEach(function(d) {
            d.timestamp = formatTimestamp(d.timestamp)
            d.score = formatScore(d.score, homeAway)
            });
        
        // set the dimensions and margins of the graph
        var margin = {top: 80, right: 50, bottom: 80, left: 60};
        var width = parseInt(d3.select('#viz').style('width'), 10);
        width = width - margin.left - margin.right;
        var height = parseInt(d3.select('#viz').style('height'), 10);
        height = height - margin.top - margin.bottom;

        // set the ranges for svg element
        var x = d3.scaleLinear().range([0, width]);
        var y = d3.scaleLinear().range([height, 0]);
        
        // scale the range of the axes
        x.domain([d3.min(data, function(d){return d.timestamp-0.5}),
                 d3.max(data, function(d){return d.timestamp+0.5})]);
        y.domain([d3.min(data, function(d){return d.score-1}),
                 d3.max(data, function(d){return d.score+1})]);

        // define the area
        var area = d3.area()
            .x(function(d) { return x(d.timestamp); })
            .y0(y(0))
            .y1(function(d) { return y(d.score); });

        // append the svg obgect to the body of the page
        // appends a 'group' element to 'svg'
        // moves the 'group' element to the top left margin
        var svg = d3.select("#chart")
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
        
        // gridlines in x axis function
        function make_x_gridlines() {		
            return d3.axisBottom(x)
            .ticks()
            }

        // gridlines in y axis function
        function make_y_gridlines() {
            const yAxisTicks = y.ticks()
                .filter(tick => Number.isInteger(tick));            
            
            return d3.axisLeft(y)
            .tickValues(yAxisTicks)
            }
        
        // add the X gridlines
        svg.append("g")			
          .attr("class", "grid")
          .attr("transform", "translate(0," + height + ")")
          .call(make_x_gridlines()
              .tickSize(-height)
              .tickFormat("")
                )

        // add the Y gridlines
        svg.append("g")			
          .attr("class", "grid")
          .call(make_y_gridlines()
              .tickSize(-width)
              .tickFormat("")
                )

        // add the area
        svg.append("path")
            .data([data])
            .attr("class", "area")
            .attr("d", area);
        
        //add halftime line
        svg.append("g")
            .attr('class', 'halftime')
            .attr("transform", "translate("+ x(30) + ",0)")
            .append("line")
            .attr("y2", height);
        
        //add draw (as in score = 1/-0) line
        svg.append("g")
            .attr('class', 'draw')
            .attr("transform", "translate(0," + y(0) + ")")
            .append("line")
            .attr("x2", width);

        // add the X Axis
        svg.append("g")
            .attr('class', 'axes')
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // add the Y Axis
        svg.append("g")
            .attr('class', 'axes')
            .call(make_y_gridlines()
                 .tickFormat(d3.format('.0f')));
        
        // text label for the x axis
        svg.append("text")
            .attr('class', 'axes-label')
            .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top/1.4) + ")")
            .style("text-anchor", "middle")
            .text("Game Time [minutes]");
        
        // text label for the y axis
        svg.append("text")
            .attr('class', 'axes-label')
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", "0.8em")
            .style("text-anchor", "middle")
            .text("Goal Differential"); 
        
        // text label for the Title
        svg.append("text")
            .attr('class', 'chart-title')
            .attr("transform", "translate(" + (width/2) + " ," + (0-margin.top/2) + ")")
            .attr("text-anchor", "middle")   
            .text("Chart Title");
        
        
        

        });
    }