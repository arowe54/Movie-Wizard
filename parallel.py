# Make parallel requests in python
import aiohttp
import asyncio

def get_all_info(movie_id)
    async def main():
        async with aiohttp.ClientSession() as session:
            url = "https://moviesdatabase.p.rapidapi.com/titles/{}".format(movie_id)
            headers = {
                "X-RapidAPI-Key": "515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e",
                "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            }
            # get request 1
            querystring = {"info":"base_info"}
            async with session.get(url, headers=headers, params=querystring) as resp:
                # Response to query 1
                print(resp.status)
                print(await resp.text())
                print(await resp.json())
            # Get request 2 asynchronously
            

    asyncio.run(main())
