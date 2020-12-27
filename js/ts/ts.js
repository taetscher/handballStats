import {getTree} from '../get_tree.js'
import {populateDropdownTS} from './pop_teams_ts.js'
import {populateSeasons} from './pop_seasons_ts.js'
import {populateStats} from './pop_stats_ts.js'
import {visualizeTS} from './visualize_ts.js'

document.getElementById("dropdown_stats").style.visibility= "hidden" ;

//populate the team selection dropdown
var teams = getTree("https://api.github.com/repos/taetscher/handballStats/git/trees/f6a0ab9b96267c9eeadef0690d80dbe42f7fa5a1");
populateDropdownTS(teams);

//populate the season selection dropdown
var team = document.getElementById('teams');
team.addEventListener('click', function(){
    var selected = document.getElementById('dropdown_teams').innerHTML;
    var seasons = getTree(teams[selected]);
    //store this link in a div (with class: hidden for css zindex -1000)
    populateSeasons(seasons);

    
    //populate the stat selection dropdown
    var season = document.getElementById('seasons');
    season.addEventListener('click', function(){
        var selected = document.getElementById('dropdown_seasons').innerHTML;
        //load this link from a hidden div
        var stats = getTree(seasons[selected]);
        //store this link in a hidden div
        console.log(stats)
        populateStats(stats);
        document.getElementById("dropdown_stats").style.visibility= "visible" ;
        team.addEventListener('click', function(){
                document.getElementById("dropdown_stats").style.visibility= "hidden" ;
            })
        })
    })

//get the choice of document
var choice = document.getElementById('stats');
choice.addEventListener('click', function(){
        var filename = document.getElementById('dropdown_stats').innerHTML;
        console.log(filename)
        
        //get final treeURL from hidden div to get the correct file
        var statsURL;
    
        //initiate the display of data via d3.js
        visualizeTS(filename,statsURL)
    })

