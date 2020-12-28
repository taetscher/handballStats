import * as d3 from "https://unpkg.com/d3@5?module";

export function loadCSV(dataURL){
    var data = d3.csv(dataURL);
    return data
};