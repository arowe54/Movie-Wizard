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

// Might need to make the functions update the database and page asynchronously