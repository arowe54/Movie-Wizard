import time
import requests
import aiohttp
import asyncio
from cs50 import SQL

# TODO: Convert functions to asynchronous

def get_genres():
    """Get a list of all genres"""
    start_time = time.time()
    url = "https://moviesdatabase.p.rapidapi.com/titles/utils/genres"

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response = response.json()
        print("--- %s seconds ---" % (time.time() - start_time))
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

def get_movies_by_list_ids(movies):
    start_time = time.time()
    url = "https://moviesdatabase.p.rapidapi.com/titles/x/titles-by-ids"

    querystring = {"idsList": movies}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print("--- %s seconds ---" % (time.time() - start_time))
    return response["results"]

def get_movies_by_genre(genre):
    """Get 10 movies in a certain genre"""
    start_time = time.time()
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    querystring = {"genre": genre,"titleType":"movie"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    # Query API
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()
        print("--- %s seconds ---" % (time.time() - start_time))
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def get_watchlist(id):
    # Configure CS50 Library to use SQLite database
    db = SQL("sqlite:///movies.db")
    # Get movies in watchlist
    watchlist = []
    rows = db.execute("SELECT movie_id FROM watchlist WHERE user_id=?;", id)
    for movie in rows:
        watchlist.append(movie["movie_id"])
    
    return watchlist


def index_queries():
    # Searches for upcoming movies and top boxoffice movies last weekend asynchronously
    start_time = time.time()
    lists = []

    async def fetch(session, url, querystring):
        headers = {
            "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
        }
        async with session.get(url, headers=headers, params=querystring) as resp:
            result = await resp.json()
            lists.append(result["results"])    


    async def main():
        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as group:
                # Upcoming movies
                url = "https://moviesdatabase.p.rapidapi.com/titles/x/upcoming"
                querystring = {"titleType":"movie","endYear":"2025","startYear":"2023"}
                group.create_task(fetch(session, url, querystring))

                # Top boxoffice movies last weekend
                url = "https://moviesdatabase.p.rapidapi.com/titles"
                querystring = {"list":"top_boxoffice_last_weekend_10"}
                group.create_task(fetch(session, url, querystring))

    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
    return lists


def lookup(title):
    """Look up movies with exact title."""
    start_time = time.time()
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
        print("--- %s seconds ---" % (time.time() - start_time))
        return response["results"]
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
    

def random_movies():
    start_time = time.time()
    url = "https://moviesdatabase.p.rapidapi.com/titles/random"

    querystring = {"list":"most_pop_movies"}

    headers = {
        "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print("--- %s seconds ---" % (time.time() - start_time))
    # Maybe seed it so you can access previous pages (if possible)
    return response["results"]

    