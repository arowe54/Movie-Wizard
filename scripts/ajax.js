// Create new AJAX object
var ajax = new XMLHttpRequest();

// When page is loaded
ajax.onreadystatechange = function() {
    if (ajax.readyState == 4 && ajax.status == 200){
        // Do stuff   
    }
}

