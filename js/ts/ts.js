import * as d3 from "https://unpkg.com/d3@5?module";
import {getTree} from '../get_tree.js'
import {populateDropdownTS} from './pop_teams_ts.js'
import {populateSeasons} from './pop_seasons_ts.js'
import {populateStats} from './pop_stats_ts.js'
import {visualizeTS} from './visualize_ts.js'
import {addHiddenScript} from '../add_hidden_script.js'

document.getElementById("dropdown_stats").style.visibility= "hidden";

window.addEventListener('resize', visualizeTS);

//add hidden scripts to store JSON data
addHiddenScript('seasons_dict');
addHiddenScript('stats_dict');

//populate the team selection dropdown
var teams = getTree("https://api.github.com/repos/taetscher/handballStats/git/trees/f6a0ab9b96267c9eeadef0690d80dbe42f7fa5a1");
populateDropdownTS(teams);

//populate the season selection dropdown
var team = document.getElementById('teams');
team.addEventListener('click', function(){
    var selected = document.getElementById('dropdown_teams').innerHTML;
    var seasons = getTree(teams[selected]);    
    document.getElementById('seasons_dict').innerHTML = JSON.stringify(seasons);
    populateSeasons(seasons);
    })
    
//populate the stat selection dropdown
var season = document.getElementById('seasons');
season.addEventListener('click', function(){
    var seasons = JSON.parse(document.getElementById('seasons_dict').innerHTML);
    var selected = document.getElementById('dropdown_seasons').innerHTML;
    var stats = getTree(seasons[selected]);
    document.getElementById('stats_dict').innerHTML = JSON.stringify(stats);
    populateStats(stats);
    document.getElementById("dropdown_stats").style.visibility= "visible" ;
    team.addEventListener('click', function(){
            document.getElementById("dropdown_stats").style.visibility= "hidden" ;
        })
    })


//get the choice of document
var choice = document.getElementById('stats');
choice.addEventListener('click', function(){
        //initiate the display of data via d3.js
        visualizeTS()
    })


