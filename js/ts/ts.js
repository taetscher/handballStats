import {getTree} from '../get_tree.js'
import {populateDropdownTS} from './pop_teams_ts.js'
import {populateSeasons} from './pop_seasons_ts.js'
import {populateStats} from './pop_stats_ts.js'

document.getElementById("dropdown_stats").style.visibility= "hidden" ;

var teams = getTree("https://api.github.com/repos/taetscher/handballStats/git/trees/f6a0ab9b96267c9eeadef0690d80dbe42f7fa5a1");
populateDropdownTS(teams);


var team = document.getElementById('teams');
team.addEventListener('click', function(){
    var selected = document.getElementById('dropdown_teams').innerHTML;
    var seasons = getTree(teams[selected]);
    populateSeasons(seasons);
    
    
    var season = document.getElementById('seasons');
    season.addEventListener('click', function(){
        var selected = document.getElementById('dropdown_seasons').innerHTML;
        var stats = getTree(seasons[selected]);
        populateStats(stats);
        document.getElementById("dropdown_stats").style.visibility= "visible" ;
        team.addEventListener('click', function(){
            document.getElementById("dropdown_stats").style.visibility= "hidden" ;
            })
        console.log(stats)
        })
    })



