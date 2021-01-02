export async function getURL(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    var result = await xmlHttp.responseText
    return JSON.parse(result);

};


export async function getTree(theUrl){
    var response = await getURL(theUrl);
    var x = 0;
    var links = {};
    for (x in response['tree']) {
        var path = response['tree'][x]['path'];
        links[path]= response['tree'][x]['url']
    }
    return links
};