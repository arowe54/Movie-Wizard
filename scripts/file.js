const sqlite3 = require('sqlite3').verbose();
// Open a database connection
let db = new sqlite3.Database('./db/movies.db');

function addToWatchlist(user_id, movie_id) {
    params = [user_id, movie_id, user_id]
    db.run("INSERT INTO watchlist(user_id, movie_id) VALUES (?, ?) WHERE user_id = ?;", params, function(err) {
        // Print message if couldn't update table
        if (err) {
            return console.error(err.message);
        }
    });
}

function removeFromWatchlist(user_id, movie_id) {
    params = [user_id, movie_id]
    db.run("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?;", params, function(err) {
        if (err) {
            return console.error(err.message);
        }
    });
}

// Close database connection
db.close();