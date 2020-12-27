import {getTree} from '../get_tree.js'
import {populateDropdownTS} from './pop_teams_ts.js'
import {populateSeasons} from './pop_seasons_ts.js'


var teams = getTree("https://api.github.com/repos/taetscher/handballStats/git/trees/f6a0ab9b96267c9eeadef0690d80dbe42f7fa5a1");
populateDropdownTS(teams);
var t_drop = document.getElementById('teams');


var team = document.getElementById('teams');
team.addEventListener('click', function(){
    var selected = document.getElementById('dropdown_teams').innerHTML;
    var links = getTree(teams[selected]);
    populateSeasons(links)

})