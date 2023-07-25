var user_id = document.getElementByID('user_id').innerHTML;


$(document).ready(function(){
    // Open database connection
    const sqlite3 = require('sqlite3').verbose();
    let db = new sqlite3.Database('./movies.db', (err) => {
        if (err) {
            console.error(err.message);
          }
          console.log('Connected to the movies database.');
    });

    // Close database connection
    db.close();

    // every time the checkbox is clicked
    $(".form-check-input").click(function() {
        // Save the movie id
        var movie_id = $(this).val();
        
        
          
        // If the checkbox is already checked (being unchecked)
        if (this.checked){
            // Remove movie from watchlist
            params = [user_id, movie_id]
            db.run("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?", params, function(err) {
                if (err) {
                    return console.error(err.message);
                }
            });
        }
        // If it was unchecked (now checked)
        else {
            // Add movie to database
            ids = [user_id, movie_id, user_id];
            db.run("INSERT INTO watchlist(user_id, movie_id) VALUES (?, ?) WHERE user_id = ?", ids, function(err) {
                // Print message if couldn't update table
                if (err) {
                    return console.error(err.message);
                }
            });
        }
        
    })
})





/*
const sqlite3 = require('sqlite3').verbose();
// Open a database connection
let db = new sqlite3.Database('./db/movies.db');

const movie_id = document.getElementByID('user_id').value;
const user_id = document.getElementByID('movie_id').value;

function addToWatchlist() {
    params = [user_id, movie_id, user_id]
    db.run("INSERT INTO watchlist(user_id, movie_id) VALUES (?, ?) WHERE user_id = ?;", params, function(err) {
        // Print message if couldn't update table
        if (err) {
            return console.error(err.message);
        }
    });
}

function removeFromWatchlist() {
    params = [user_id, movie_id]
    db.run("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?;", params, function(err) {
        if (err) {
            return console.error(err.message);
        }
    });
}

// Close database connection
db.close();
*/