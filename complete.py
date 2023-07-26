import time
# Make parallel requests in python
import aiohttp
import asyncio

def get_all_info(movie_id):
    start_time = time.time()
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
            # Must return a coroutine for it to be used as a task (currently not returning anything)
 
    async def main():
        async with aiohttp.ClientSession() as session:
            url = "https://moviesdatabase.p.rapidapi.com/titles/{}".format(movie_id)
            headers = {
                "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
                "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            }

            async with asyncio.TaskGroup() as group:
                # get request 1
                querystring = {"info":"base_info"}
                group.create_task(fetch(session, url, headers, querystring))

                # Get request 2 asynchronously
                querystring = {"info":"revenue_budget"}
                group.create_task(fetch(session, url, headers, querystring))

                # etc...
                querystring = {"info":"awards"}
                group.create_task(fetch(session, url, headers, querystring))

                querystring = {"info":"filmingLocations"}
                group.create_task(fetch(session, url, headers, querystring))

                querystring = {"info":"soundtrack"}
                group.create_task(fetch(session, url, headers, querystring))

                querystring = {"info":"countriesOfOrigin"}
                group.create_task(fetch(session, url, headers, querystring))

                querystring = {"info":"spokenLanguages"}
                group.create_task(fetch(session, url, headers, querystring))

                querystring = {"info":"moreLikeThisTitles"}
                group.create_task(fetch(session, url, headers, querystring))

            
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
    return movie

