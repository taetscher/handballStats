export function populateDropdownTS(tree){
    var keys = Object.keys(tree);
    var x;
    for (x in keys){
        var team = keys[x];
        var newO = document.createElement('OPTION');
        newO.setAttribute('href',"#");
        newO.addEventListener('click', function() {
            var selected = this.innerHTML;
            document.getElementById('dropdown_teams').innerHTML = selected
                        })
        newO.innerHTML = team;
        document.getElementById('teams').appendChild(newO);
    }
}