import * as d3 from "https://unpkg.com/d3@5?module";

export function vizClean(data){
    
    console.log('clean')
    
    //set up title
    var team = document.getElementById('dropdown_teams').innerHTML;
    var season = document.getElementById('dropdown_seasons').innerHTML;
    var stat = document.getElementById('dropdown_stats').innerHTML;
    var title = stat + " (" + team + ", " + season + ")";

    
    // set the dimensions and margins of the graph
    var margin = {top: 80, right: 50, bottom: 80, left: 60};
    var width = parseInt(d3.select('#viz').style('width'), 10);
    width = width - margin.left - margin.right;
    var height = parseInt(d3.select('#viz').style('height'), 10);
    height = height - margin.top - margin.bottom;
    
    var x = d3.scaleLinear()
          .domain(d3.extent(data, d => d.year))
          .range([0, width]);
    var y = d3.scaleLinear()
          .domain([0, 1])
          .range([height, 0]);
    
    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select('#chart')
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
    
    //append paths to the graph for each player individually
    var n;
    for (n=0; n < data.length; n++ ){
        
        //convert the data
        var player = data[n].SPIELER;
        var dates = Object.keys(data[n]);
        dates.shift()
        var statistics = Object.values(data[n]);
        statistics.shift()
        
        //convert dates to actual dates (use d3.parsedate)
        //convert statistics to numbers
        
        //then go on an use them on the graph

        
        var line = d3.line()
         .x(d => x(dates))
         .y(d => y(statistics));
        
        
        const path = svg.append("g")
                      .selectAll(".total")
                      .data(data[n])
                      .enter()
                      .append("path")
                      .attr("id", data[n].SPIELER)
                      .attr("fill", "none")
                      .attr("stroke", "purple")
                      .attr("mix-blend-mode", "multiply")
                      .attr("stroke-width", 1)
                      .attr("stroke-linejoin", "round")
                      .attr("d", line(data[n]));
    }
    
    
    
    
    
    
    
    
}