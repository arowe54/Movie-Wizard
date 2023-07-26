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


"""
# Execute all requests in parallel
def x_all_of_movie(movie_id):
    url = "https://moviesdatabase.p.rapidapi.com/titles/{}".format(movie_id)
    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    movie = {}
    q1 = {"info": "base_info", "revenue_budget", "awards"}
    q2 = {"info": "revenue_budget"}
    ##q3 = {"info": "awards"}
    ##queries = [q1, q2, q3]

    try:
        response = requests.get(url, headers=headers, params=q1)
        response = response.json()
        print()
        response = response["results"]
        print(response)
        print()
        for key in response:
            if key not in movie:
                movie[key] = response[key]
        return movie
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

"""