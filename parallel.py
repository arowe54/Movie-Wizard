# Make parallel requests in python
import aiohttp
import asyncio

def get_all_info(movie_id):
    # Get a request from a url with current parameters
    async def fetch(session, url, headers, querystring):
        async with session.get(url, headers=headers, params=querystring) as resp:
            # Only get the text of the request for now
            return await resp.text()
        
    async def main():
        async with aiohttp.ClientSession() as session:
            url = "https://moviesdatabase.p.rapidapi.com/titles/{}".format(movie_id)
            headers = {
                "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
                "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            }
            movie = {}
            
            # get request 1
            querystring = {"info":"base_info"}
            base_info = fetch(session, url, headers, querystring)
            print(base_info)
            print()

            # Get request 2 asynchronously
            q2 = {"info":"revenue_budget"}
            rev_budget = fetch(session, url, headers, q2)
            print(rev_budget)
            print()

    asyncio.run(main())
