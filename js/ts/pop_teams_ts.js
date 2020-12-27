export function populateDropdownTS(tree, elementId){
    var keys = Object.keys(tree);
    var x;
    for (x in keys){
        var team = keys[x];
        document.getElementById(elementId).innerHTML += "<option href='#' value=\"" + team + "\">" + team + "</option>"
    }
}