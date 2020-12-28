import {loadCSV} from '../load_csv.js'

export function visualizeTS(){
    
    //build in an option to visualize everything on top of each other (see all games)
    
    //construct an url to the base data
    var ts_baseurl = "https://raw.githubusercontent.com/taetscher/handballStats/master/output_csv/progress_data/";
    var team = document.getElementById('dropdown_teams').innerHTML;
    var season = document.getElementById('dropdown_seasons').innerHTML;
    var stat = document.getElementById('dropdown_stats').innerHTML;
    var dataURL = ts_baseurl+team+"/"+season+"/"+stat;
    dataURL = encodeURI(dataURL)
    console.log(dataURL)
    
    //load the data
    loadCSV(dataURL).then(function (data){
        
        //here comes the visualization stuff
    }
        );
}