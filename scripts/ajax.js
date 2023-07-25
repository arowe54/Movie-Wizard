const sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database('./db/movies.db');


const user_id = document.getElementByID('user_id').innerHTML;


function addToWatchlist(event){
    // Create new AJAX object
    var ajax = new XMLHttpRequest();

    trigger = event.

    // When page is loaded
    ajax.onreadystatechange = function() {
        if (ajax.readyState == 4 && ajax.status == 200){
            $(document).ready(function(){
                // every time the checkbox is clicked
                $('.form-check-input').click(function(event){
                    // Save the movie id
                    // Update the database
                    // If it is being checked
                        // Add movie to database
                        ids = [user_id, movie_id, user_id];
                        db.run("INSERT INTO watchlist(user_id, movie_id) VALUES (?, ?) WHERE user_id = ?", ids, function(err) {
                            // Print message if couldn't update table
                            if (err) {
                                return console.error(err.message);
                            }
                        });
                    // If it is being unchecked
                        // Remove movie from database
                })
            })
            // Update database
            
        }
    }
}

