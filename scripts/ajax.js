const sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database('./db/movies.db');


const movie_id = document.getElementByID('user_id').value;
const user_id = document.getElementByID('movie_id').value;


function addToWatchlist(){
    // Create new AJAX object
    var ajax = new XMLHttpRequest():

    // When page is loaded
    ajax.onreadystatechange = function() {
        if (ajax.readyState == 4 && ajax.status == 200){
            // Update database
            ids = [user_id, movie_id, user_id]
            db.run("INSERT INTO watchlist(user_id, movie_id) VALUES (?, ?) WHERE user_id = ?", ids, function(err) {
                // Print message if couldn't update table
                if (err) {
                    return console.error(err.message);
                }
            });
            // Possibly update the checkbox? (probably not because flask will refresh with access to watchlist anyways?)
        }
    }
}