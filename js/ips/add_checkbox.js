export function addCheckbox(player) { 
        var myDiv = document.getElementById("checkboxes");

        var boxDiv = document.createElement('a')
        boxDiv.className = 'checkbox';

        // creating checkbox element 
        var checkbox = document.createElement('input'); 

        // Assigning the attributes 
        // to created checkbox 
        checkbox.type = "checkbox"; 
        checkbox.className = 'checkbox_box';
        checkbox.id = "checkbox_"+player; 
        checkbox.checked = true;

        // creating label for checkbox 
        var label = document.createElement('label');
        label.id = 'label_' + player

        // appending the created text to  
        // the created label tag  
        label.appendChild(document.createTextNode(player.replaceAll('_', ' '))); 

        // appending the checkbox 
        // and label to a-tag
        boxDiv.appendChild(checkbox); 
        boxDiv.appendChild(label); 

        //appending a-tag to div
        myDiv.appendChild(boxDiv);
        
        //connect checkboxes with lines
        d3.select("#checkbox_"+player).on('change', function(){
            
                            var state = d3.select(this).property('checked')
                            
                            if (state == false){
                                d3.select('#' + player + '_line')
                                .attr('opacity', 0)
                            }else{
                                d3.select('#' + player + '_line')
                                .attr('opacity', 1)
                            }
            })
                            
                            
                            
    } 