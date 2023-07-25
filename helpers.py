import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps

def all_of_movie(movie_id):
    """Get all of the info about a specific movie"""
    url = "https://moviesdatabase.p.rapidapi.com/titles/{}".format(movie_id)
    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    movie = {}
    # Query for base_info
    querystring = {"info":"base_info"}
    base_info = requests.get(url, headers=headers, params=querystring)
    base_info = base_info.json()
    base_info = base_info["results"]
    for key in base_info:
        # If it has not already been recorded
        if key not in movie:
            # Record it
            movie[key] = base_info[key]


    # revenue_budget
    querystring = {"info":"revenue_budget"}
    rev_budget = requests.get(url, headers=headers, params=querystring)
    rev_budget = rev_budget.json()
    rev_budget = rev_budget["results"]
    for key in rev_budget:
        if key not in movie:
            movie[key] = rev_budget[key]

    # awards
    querystring = {"info":"awards"}
    awards = requests.get(url, headers=headers, params=querystring)
    awards = awards.json()
    awards = awards["results"]
    for key in awards:
        if key not in movie:
            movie[key] = awards[key]

    # filmingLocations
    querystring = {"info":"filmingLocations"}
    filming_locations = requests.get(url, headers=headers, params=querystring)
    filming_locations = filming_locations.json()
    movie["filming_locations"] = filming_locations["results"]["filmingLocations"]

    # Soundtrack
    querystring = {"info":"soundtrack"}
    soundtrack = requests.get(url, headers=headers, params=querystring)
    soundtrack = soundtrack.json()
    movie["soundtrack"] = soundtrack["results"]["soundtrack"]["edges"]


    # countriesOfOrigin (maybe add flag icons)
    querystring = {"info":"countriesOfOrigin"}
    countries = requests.get(url, headers=headers, params=querystring)
    countries = countries.json()
    movie["countriesOfOrigin"] = countries["results"]["countriesOfOrigin"]["countries"]


    # Spoken Languages
    querystring = {"info":"spokenLanguages"}
    langs = requests.get(url, headers=headers, params=querystring)
    langs = langs.json()
    movie["languages"] = langs["results"]["spokenLanguages"]["spokenLanguages"]

    # moreLikeThisTitles (just get a list of ids)
    querystring = {"info":"moreLikeThisTitles"}
    similar = requests.get(url, headers=headers, params=querystring)
    similar = similar.json()
    movie["moreLikeThisTitles"] = similar["results"]["moreLikeThisTitles"]["edges"]


    return movie

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
    """Get a list of all genres"""
    url = "https://moviesdatabase.p.rapidapi.com/titles/utils/genres"

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


def get_movies_by_genre(genre):
    """Get 10 movies in a certain genre"""
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"genre": genre,"titleType":"movie"}

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
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


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