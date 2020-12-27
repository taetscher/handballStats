import {getTree} from '../get_tree.js'
import {populateDropdownTS} from './pop_teams_ts.js'
import {populateSeasonsTS} from './pop_seasons_ts.js'


var teams = getTree("https://api.github.com/repos/taetscher/handballStats/git/trees/f6a0ab9b96267c9eeadef0690d80dbe42f7fa5a1");

populateDropdownTS(teams,'teams');
var t_drop = document.getElementById('teams');



var tree = getTree("https://api.github.com/repos/taetscher/handballStats/git/trees/7d6246d6ae5e448e760cd985eb7a7d5461fe6698");




