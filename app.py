import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import date

from helpers import apology, login_required, lookup, usd

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
@login_required
def index():
    """Home Page"""
    return render_template("layout.html")


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route through a form
    if request.method == "POST":
        # If username is blank
        if not request.form.get("username"):
            return apology("Please Enter a Username and Password")
        # Save username
        username = request.form.get("username")
        # If username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)
        if len(rows) > 0:
            return apology("Username already exists")

        # If user didn't input a password
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Please enter a password in both password fields")
        # If passwords do not match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match. Please reenter password")
        # Save password
        password = request.form.get("password")

        # Insert new user into users
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(?,?);", username, hash)

        users = db.execute("SELECT * FROM users;")
        print(users)

        # Log the user in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # User reached route through clicking a link
    else:
        return render_template("register.html")
