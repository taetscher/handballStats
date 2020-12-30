export function addCheckbox(player) { 
            var myDiv = document.getElementById("checkboxes");
    
            var boxDiv = document.createElement('a')
            boxDiv.className = 'checkbox';
              
            // creating checkbox element 
            var checkbox = document.createElement('input'); 
              
            // Assigning the attributes 
            // to created checkbox 
            checkbox.type = "checkbox"; 
            checkbox.name = "name"; 
            checkbox.value = "value";
            checkbox.className = 'checkbox_box';
            checkbox.id = "checkbox_"+player; 
              
            // creating label for checkbox 
            var label = document.createElement('label'); 
              
            // assigning attributes for  
            // the created label tag  
            label.htmlFor = "id"; 
              
            // appending the created text to  
            // the created label tag  
            label.appendChild(document.createTextNode(player)); 
              
            // appending the checkbox 
            // and label to div 
            boxDiv.appendChild(checkbox); 
            boxDiv.appendChild(label); 
            
            myDiv.appendChild(boxDiv);
        } 