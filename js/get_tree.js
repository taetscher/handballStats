export function getURL(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, 0); // false for synchronous request
    xmlHttp.send( null );
    var result = xmlHttp.responseText
    return JSON.parse(result);
};


export function getTree(theUrl){
    var response = getURL(theUrl);
    var x = 0;
    var links = {};
    for (x in response['tree']) {
        var path = response['tree'][x]['path'];
        links[path]= response['tree'][x]['url']
    }
    return links
};