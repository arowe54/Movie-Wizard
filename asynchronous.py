import time

# Make parallel requests in python
import aiohttp
import asyncio

# TODO: Convert functions to asynchronous

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

def get_movies_by_list_ids(movies):

    url = "https://moviesdatabase.p.rapidapi.com/titles/x/titles-by-ids"

    querystring = {"idsList": movies}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    return response["results"]

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
    start_time = time.time()
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"list":"top_boxoffice_last_weekend_10"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()
        print("--- %s seconds ---" % (time.time() - start_time))
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


# Upcoming movies
def upcoming():
    start_time = time.time()
    url = "https://moviesdatabase.p.rapidapi.com/titles/x/upcoming"

    querystring = {"titleType":"movie","endYear":"2025","startYear":"2023"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()
        print("--- %s seconds ---" % (time.time() - start_time))
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
    
