export function listfiles(dir){
    
    $.ajax({
    url: dir,
    success: function(data){
     console.log(data)
     $(data).find("a:contains(.png)").each(function(){
        // will loop through and append elements to div
        //var div = document.getElementById('listOfFiles')
        //var link = $(this).attr("href");
        //var img = document.createElement('img')
        //img.src = link
        //img.setAttribute('alt', link);
        //div.appendChild(img)
        console.log(".." + link);
        var parsed = JSON.parse(data)
        console.log(parsed);
     });
    }
    });
 
}