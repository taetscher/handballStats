import {getTree} from '../get_tree.js'
import {populateDropdownTS} from './pop_teams_ts.js'
import {populateSeasons} from './pop_seasons_ts.js'
import {populateStats} from './pop_stats_ts.js'
import {visualizeTS} from './visualize_ts.js'
import {addHiddenScript} from '../add_hidden_script.js'

document.getElementById("dropdown_stats").style.visibility= "hidden";

//every time the window is resized, draw again
window.addEventListener('resize', visualizeTS);

//add hidden scripts to store JSON data
addHiddenScript('seasons_dict');
addHiddenScript('stats_dict');

//populate the team selection dropdown
var treeAtMaster = "https://api.github.com/repos/taetscher/handballStats/git/trees/master"
var basetree = getTree(treeAtMaster)
var output_csv = getTree(basetree.output_csv)
var teams = getTree(output_csv.gameProgressions)
populateDropdownTS(teams)

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


