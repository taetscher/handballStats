export function populateDropdownTS(tree, elementId){
    var keys = Object.keys(tree);
    var x;
    for (x in keys){
        var team = keys[x];
        var newA = document.createElement('li');
        newA.setAttribute('href',"#");
        newA.addEventListener('click', function() {
            var selected = this.innerHTML;
            console.log(selected);
            document.getElementById('dropdown_teams').innerHTML = selected
                        })
        newA.innerHTML = team;
        document.getElementById('teams').appendChild(newA);
    }
}