# Make parallel requests in python
import aiohttp
import asyncio

def get_all_info(movie_id):
    movie = {}

    # Get a request from a url with current parameters
    async def fetch(session, url, headers, querystring):
        async with session.get(url, headers=headers, params=querystring) as resp:
            result = await resp.json()
            result = result["results"]
            # Copy each key:value pair to the movie dict
            for key in result:
                if key not in movie:
                    movie[key] = result[key]
 
    async def main():
        async with aiohttp.ClientSession() as session:
            url = "https://moviesdatabase.p.rapidapi.com/titles/{}".format(movie_id)
            headers = {
                "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
                "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            }

            # get request 1
            querystring = {"info":"base_info"}
            await fetch(session, url, headers, querystring)

            # Get request 2 asynchronously
            querystring = {"info":"revenue_budget"}
            await fetch(session, url, headers, querystring)

            # etc...
            querystring = {"info":"awards"}
            await fetch(session, url, headers, querystring)

            querystring = {"info":"filmingLocations"}
            await fetch(session, url, headers, querystring)

            querystring = {"info":"soundtrack"}
            await fetch(session, url, headers, querystring)

            querystring = {"info":"countriesOfOrigin"}
            await fetch(session, url, headers, querystring)

            querystring = {"info":"spokenLanguages"}
            await fetch(session, url, headers, querystring)

            querystring = {"info":"moreLikeThisTitles"}
            await fetch(session, url, headers, querystring)

            
    asyncio.run(main())
    return movie
