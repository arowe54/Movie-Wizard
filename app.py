import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import date

from helpers import apology, login_required, usd
from queries import get_genres, get_movies_by_list_ids, get_movies_by_genre, get_watchlist, lookup, random_movies, index_queries
from complete import get_all_info

# Configure application
app = Flask(__name__)

# Custom filter (format values as US dollars)
app.jinja_env.filters["usd"] = usd

# Configure session to use the local filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movies.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Home Page"""
    home = index_queries()

    user_id = session["user_id"]

    # Get movies in watchlist
    watchlist = get_watchlist(user_id)

    return render_template("index.html", upcoming=home[0], box_10=home[1], movies_in_watchlist=watchlist, id=user_id)


@app.route("/genres")
def genres():
    """Get Movies in each genre"""
    # Get list of each genre
    genres = get_genres()
    
    # Get genre selected by the user
    genre = request.args.get("genre")

    # Find and save movies in that genre to a list of dictionaries
    movies_in_genre = None
    if genre != None:
        movies_in_genre = get_movies_by_genre(genre)
    
    # Get movies in watchlist
    id = session["user_id"]
    watchlist = get_watchlist(id)
    
    # Send to genres.html
    return render_template("genres.html", genres=genres, movies=movies_in_genre, genre_selected=genre, watchlist=watchlist)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/movie")
def movie():
    """Get information on a specific movie"""
    id = request.args.get("movie_id")
    movie = get_all_info(id)

    watchlist = get_watchlist(session["user_id"])

    return render_template("movie.html", movie=movie, movies_in_watchlist=watchlist)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Check if username is blank
        if not request.form.get("username"):
            return apology("Please Enter a Username and Password")
        # Save username
        username = request.form.get("username")
        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(rows) > 0:
            return apology("Username already exists")

        # Check if user didn't input a password
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Please enter a password in both password fields")
        # Check if passwords do not match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match. Please reenter password")
        # Save password
        password = request.form.get("password")

        # Insert new user into users
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(?,?);", username, hash)
        # Log the user in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/search")
def search():
    """User searched for a movie"""
    movies = None
    # If the user searched for a movie by title
    if request.args.get("title"):
        # Lookup movie from title
        title = request.args.get("title")
        movies = lookup(title)

    # If user searched for a random movie
    else:
        movies = random_movies()    
    
    if not movies:
        return apology("That movie is not in the database")
    
    user_id = session["user_id"]

    # Get movies in watchlist
    watchlist = get_watchlist(user_id)
    
    # Display result
    return render_template("search.html", movies=movies, movies_in_watchlist=watchlist, id=user_id)
    
@app.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():
    user_id = session["user_id"]
    if request.method == "POST":
        # Update Database
        # movie_id = request.form.get('data-value')
        # movie_id = str(movie_id)

        action = request.form.get('value')
        action = str(action)
        # If checking the box
        if action == 'add':
            # Add movie id to watchlist
            db.execute("INSERT INTO watchlist(user_id, movie_id) VALUES (?, ?);", user_id, movie_id)
        # If unchecking the box
        elif action == 'remove':
            # Remove movie id from watchlist
            db.execute("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?;", user_id, movie_id)

        # Return back to the page you submitted the form
        return redirect(request.referrer)
    else:
        watchlist = get_watchlist(user_id)
        # Get all movies with this list of ids (max 10 currently, can add pages, and so more movies later on)
        movies = get_movies_by_list_ids(watchlist)

        return render_template("watchlist.html", movies=movies, movies_in_watchlist=watchlist)