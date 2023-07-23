import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def get_genres():
    import requests

    url = "https://moviesdatabase.p.rapidapi.com/titles/utils/genres"

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    return response["results"]


# Function returns another function
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(title):
    """Look up movies with exact title."""
    
    url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/{}".format(title)

    querystring = {"exact":"true","titleType":"movie"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    # Query API
    try:
        response = requests.get(url, headers=headers, params=querystring)

        # response["results"] is a list of dictionaries, each item is a movie
        response = response.json()
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
    

def random_movies():
    url = "https://moviesdatabase.p.rapidapi.com/titles/random"

    querystring = {"list":"most_pop_movies"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    # Maybe seed it so you can access previous pages (if possible)
    return response["results"]


# Top 10 movies in box office last weekend
def top_box_last_weekend():
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"list":"top_boxoffice_last_weekend_10"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    return response["results"]


# Upcoming movies
def upcoming():
    url = "https://moviesdatabase.p.rapidapi.com/titles/x/upcoming"

    querystring = {"titleType":"movie","endYear":"2025","startYear":"2023"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


# ex. 1234.56 -> $1,234.56
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"