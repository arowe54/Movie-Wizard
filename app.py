import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from random import randint

from helpers.helpers import apology, login_required, secToMin, usd
from helpers.complete import get_all_info
from helpers.queries import get_genres, get_movies_by_list_ids, get_movies_by_genre, get_watchlist, lookup, random_movies, index_queries

# Configure application
app = Flask(__name__)

# Custom filters
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["secToMin"] = secToMin

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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Home Page"""
    # Generate homepage movies
    if request.method == "POST":
        # If user wants random upcoming movies
        x = randint(1, 9)
        # Go to a random page from upcoming movies
        home_movies = index_queries(x)
    else:
        home_movies = index_queries(2)
    
    # Get watchlist and user id if user logged in
    try:
        user_id = session["user_id"]
        watchlist = get_watchlist(user_id)
    except (KeyError):
        user_id = None
        watchlist = None
 
    return render_template("index.html", upcoming=home_movies["upcoming"], box_10=home_movies["top_box"], movies_in_watchlist=watchlist, id=user_id)


@app.route("/genres")
def genres():
    """Get Movies in each genre"""
    # Get list of each genre
    genres = get_genres()
    # Filter genres
    genres = [genre for genre in genres if genre not in ("Adult", "Game-Show", "News", "Reality-TV", "Short", "Talk-Show")]

    # Get genre selected by the user
    genre = request.args.get("genre")
    # Find and save movies in that genre to a list of dictionaries
    movies_in_genre = None
    if genre != None:
        movies_in_genre = get_movies_by_genre(genre)
    
    # Get movies in watchlist
    try:
        watchlist = get_watchlist(session["user_id"])
    except (KeyError):
        watchlist = None
    
    return render_template("genres.html", genres=genres, movies=movies_in_genre, genre_selected=genre, watchlist=watchlist)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any prev user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember user info
        session["user_id"] = rows[0]["id"]
        session["password"] = password
        # Redirect user to home page
        return redirect("/")
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

    try:
        user_id = session["user_id"]
        watchlist = get_watchlist(user_id)
    except (KeyError):
        watchlist = None

    return render_template("movie.html", movie=movie, movies_in_watchlist=watchlist)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Get profile information"""

    # If user is updating their credentials
    id = session["user_id"]
    # If the user is changing their username
    if request.form.get("new_username"):
        new_username = request.form.get("new_username")
        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?;", new_username)
        if len(rows) > 0:
            return apology("ERROR: Username already exists")

        # Update saved username to new username
        db.execute("UPDATE users SET username = ? WHERE id = ?;", str(new_username), id)
        username = new_username
    else:
        # Save current username
        user = db.execute("SELECT username FROM users WHERE id = ?;", id)
        username = user[0]["username"]

    # If the user is changing their password
    if request.form.get("new_pwd"):
        # Save new password
        new_password = request.form.get("new_pwd")
        session["password"] = new_password
        new_hash = generate_password_hash(new_password)
        # Update hash to new password hash
        db.execute("UPDATE users SET hash = ? WHERE id = ?;", new_hash, id)
    
    # Save password
    password = session["password"]

    return render_template("profile.html", username=username, pwd=password)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure user entered a username
        if not request.form.get("username"):
            return apology("Please Enter a Username and Password")
        username = request.form.get("username")
        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(rows) > 0:
            return apology("Username already exists")

        # Ensure user entered a password
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
        session["password"] = password

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
    else:
        movies = random_movies()    
    
    # If the movie is not in the database
    if not movies:
        return apology("That exact movie title cannot be found in the database")
    
    # Get watchlist and user id
    try:
        user_id = session["user_id"]
        watchlist = get_watchlist(user_id)
    except (KeyError):
        user_id = None
        watchlist = None
    
    return render_template("search.html", movies=movies, movies_in_watchlist=watchlist, id=user_id)


@app.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():
    user_id = session["user_id"]
    # If user is updating their watchlist
    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        action = request.form.get("action")

        # If checking the box
        if action == 'add':
            # Add movie id to watchlist
            db.execute("INSERT INTO watchlist(user_id, movie_id) VALUES (?, ?);", user_id, movie_id)
        # If unchecking the box
        elif action == 'remove':
            # Remove movie id from watchlist
            db.execute("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?;", user_id, movie_id)

        # Return to the page you submitted the form
        return redirect(request.referrer)
    # If user wants to access their watchlist
    else:
        watchlist = get_watchlist(user_id)

        # Split the watchlist into lists/pages with 9 movies per page
        pages_of_ids = []
        pg = []
        pg_num = 0
        i = 0
        for id in watchlist:
            pg.append(id)
            j += 1
            # Save the page when there is 9 movies or the last movie is being checked
            if len(pg) == 9 or i == len(watchlist):
                pages_of_ids.append(pg)
                pg_num += 1
                pg = []
        
        # Get the number of pages
        num_pages = len(pages_of_ids)

        movies = []
        # Iterate through each page of movie ids
        for page in pages_of_ids:
            # Get a page of movies based on these ids, and append them to a new list of movies
            movies.append(get_movies_by_list_ids(page))

        return render_template("watchlist.html", movies_in_watchlist=watchlist, num_pages=num_pages, pages=movies)