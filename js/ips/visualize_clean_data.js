export function vizClean(data){
    
    console.log('clean')
    //console.log(data)
    
    //set up title
    var team = document.getElementById('dropdown_teams').innerHTML;
    var season = document.getElementById('dropdown_seasons').innerHTML;
    var stat = document.getElementById('dropdown_stats').innerHTML;
    var title = stat + " (" + team + ", " + season + ")";

    
    // set the dimensions and margins of the graph
    var margin = {top: 80, right: 50, bottom: 120, left: 60};
    var width = parseInt(d3.select('#viz').style('width'), 10);
    width = width - margin.left - margin.right;
    var height = parseInt(d3.select('#viz').style('height'), 10);
    height = height - margin.top - margin.bottom;
    
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
    
    //loop through the data a first time to get ranges for y axis
    var stat_minima = [];
    var stat_maxima = [];
    var q;
    for (n=0; n < data.length; n++ ){
        //convert the data
        var player = data[n].SPIELER;
        
        //convert statistics to numbers
        var statistics_r = Object.values(data[n]);
        statistics_r.shift()
        for (e in statistics_r){
            statistics_r[e] = Number(statistics_r[e])
        }
        
        stat_minima.push(d3.min(statistics_r))
        stat_maxima.push(d3.max(statistics_r))
    }
    
    var stat_min = d3.min(stat_minima);
    var stat_max = d3.max(stat_maxima);
    
    //append paths to the graph for each player individually
    var n;
    for (n=0; n < data.length; n++ ){
        
        //convert the data
        var player = data[n].SPIELER;
        
        //convert dates to actual dates
        var dates = Object.keys(data[n]);
        dates.shift()
        var e;
        for (e in dates){
            dates[e] = d3.timeParse("%y_%m_%d")(dates[e])
        }
        
        //convert statistics to numbers
        var statistics = Object.values(data[n]);
        statistics.shift()
        for (e in statistics){
            statistics[e] = Number(statistics[e])
        }
        
        //set up array for d3.line
        var xy = [];
        for(var i=0;i<dates.length;i++){
           xy.push({x:dates[i],y:statistics[i]});
        }

        //set ranges
        var x = d3.scaleTime()
            .domain(d3.extent(xy, function(d) { return d.x; }))
            .range([0, width]);
        var y = d3.scaleLinear()
            .domain([stat_min, stat_max])
            .range([height, 0]);
        
        // only on the first one, append the gridlines
        if (n==0){
            // gridlines in x axis function
            function make_x_gridlines() {		
                return d3.axisBottom(x).ticks(dates.length).tickValues(dates)
                }
            // gridlines in y axis function
            function make_y_gridlines() {
                const yAxisTicks = y.ticks().filter(tick => Number.isInteger(tick)); 
                return d3.axisLeft(y).tickValues(yAxisTicks)
                } 
            // add the X gridlines
            svg.append("g")			
                .attr("class", "grid_ips")
                .attr("transform", "translate(0," + height + ")")
                .call(make_x_gridlines()
                    .ticks()
                    .tickSize(-height)
                    .tickFormat("")
                    )
            // add the Y gridlines
            svg.append("g")			
                .attr("class", "grid_ips")
                .call(make_y_gridlines()
                    .tickSize(-width)
                    .tickFormat("")
                    )
        }
        
        //set up random color
        var color = '#'+Math.floor(Math.random() * Math.pow(2,32) ^ 0xffffff).toString(16).substr(-6);
        
        // Add the line
        svg.append("path")
          .datum(xy)
          .attr('class', 'player_stat')
          .attr("fill", "none")
          .attr("stroke", color)
          .attr("d", d3.line()
            .x(function(d) { return x(d.x) })
            .y(function(d) { return y(d.y) })
            )
        
        // only on the last one, append the axes
        if (n==data.length -1){
                // gridlines in y axis function
                function make_y_gridlines() {
                    const yAxisTicks = y.ticks().filter(tick => Number.isInteger(tick)); 
                    return d3.axisLeft(y).tickValues(yAxisTicks)
                } 

                //append x-axis
                svg.append("g")
                    .attr('class', 'axes')
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisBottom(x)
                          .tickValues(dates)
                          .tickFormat(d3.timeFormat('%d.%m.%y')))
                    .selectAll("text")
                        .attr('class', 'x_ticks_ips')
                        .style("text-anchor", "end")
                        .attr("dx", "-.8em")
                        .attr("dy", ".15em")
                        .attr("transform", "rotate(-65)");
            
                //append y-axis
                svg.append("g")
                    .attr('class', 'axes')
                    .call(make_y_gridlines()
                        .tickFormat(d3.format('.0f')));    
        }
    } 
}