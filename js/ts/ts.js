import {getTree} from '../get_tree.js'
import {populateDropdownTS} from './pop_teams_ts.js'


var teams = getTree("https://api.github.com/repos/taetscher/handballStats/git/trees/f6a0ab9b96267c9eeadef0690d80dbe42f7fa5a1");

populateDropdownTS(teams,'teams');






