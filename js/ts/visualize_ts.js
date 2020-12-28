import * as d3 from "https://unpkg.com/d3@5?module";
import {loadCSV} from '../load_csv.js';
import {whoAreWe} from '../us.js';
import {formatScore, formatTimestamp} from './format_csv.js'

export function visualizeTS(){
    
    //build in an option to visualize everything on top of each other (see all games)
    
    //construct an url to the base data
    var ts_baseurl = "https://raw.githubusercontent.com/taetscher/handballStats/master/output_csv/gameProgressions/";
    var team = document.getElementById('dropdown_teams').innerHTML;
    var season = document.getElementById('dropdown_seasons').innerHTML;
    var stat = document.getElementById('dropdown_stats').innerHTML;
    var dataURL = ts_baseurl+team+"/"+season+"/"+stat;
    dataURL = encodeURI(dataURL)
    //console.log(dataURL)
    
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
        console.log(data)
        
        // set the dimensions and margins of the graph
        var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 1500 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

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
            return d3.axisLeft(y)
            .ticks()
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
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // add the Y Axis
        svg.append("g")
            .call(d3.axisLeft(y));

        });

        
        
        
        
        
        
        
    }