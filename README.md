# CS50X Web Wizard
#### VIDEO DEMO: <url>
#### Description:
Welcome to Web Wizard
Have you every had trouble finding and picking the right movie? Web Wizard is just the right website for you.

This website uses Javascript, Python, and SQL to help users find and save movies of interest to them.
You can lookup movies by title, filter by genre, save movies you want to watch, and get random movies.

At first I looked towards the CS50 Finance problem set as inspiration to use a free online API to get data and display it through my project.
I decided to use MoviesDatabase by Adriano Massimo on RapidAPI, which he says has access to complete and updated data of over 9 million titles
with useful information about each movie. Plus, it is updated weekly.

It is called Web Wizard because the website speed and access to such a large variety of movies, as well as the ability for me to find movies that I wanted to watch,
made it feel like it was magic. Also, the screen is typically filled with posters that make the screen very colourful, and it looks like the result of a wizard 
doing a lot of magic. Also, I was filtering the genres in genres.html, I found that the best movies are the ones in myster, horror, adventure, and fantasy, which all
can be associated with Wizards.

To create a backbone of my project, I copied my CS50 Finance submission into a separate folder. This is because it uses a lot of similar features, while still adding
new ones.


Index:

Lookup:
  Table:
  
  Ajax:

Genres:
I noticed through the testing section of RapidApi for MoviesDatabase that you can filter movies by genre, as well as get a list of genres, each in their own request.
I completed this feature by creating a request for the genre and the 

movie.html:
As a final major feature, I implemented movie.html, which gets all the info about a certain movie based on its id. 
One problem I found was that in soundtrack, it would print the html of the comments to the screen (including anchor tags and divs) instead of the what was actually 
inside of the html. To fix this, I googled how to render html into a website as html and not as text, and found that I needed to filter the jinja using safe.

I noticed another feature on the RapidApi site where you can find similar movies using an "info": "moreLikeThis" querystring parameter, and decided to include that
feature into the movie.html page.

It was at this point that I realized that the website was taking way too long to load. The get_all_info(id) function had to work with so many requests, and it was also
taking too long to load my homepage. In order to add and test more features (which would requre booting up the site each time), I decided now would be a good time to
reduce the latency of the site. With a little bit of research of Stack Overflow, I discovered that instead of loading requests synchronously, I could do use asyncio
and aiohttp to complete several requests at the same time.
I installed both features on pip and imported them to my document for use. Before I started working on improving the latency, I timed the current speed of loading index.html
and movie.html by importing time, recording start_time = time.time() in the beginning of each function, and printing time.time() - start_time at the end for each.
I referred to the AIOHTTP docs (https://docs.aiohttp.org/en/stable/client_quickstart.html) to get each request using 'async with' syntax, and found that this improved
the wait time from 12-15 seconds, to 8-9 seconds. Wait-time was still long, and so I looked deeper into shortening it.
I found another website (https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html) where the user used a TaskGroup to do up to 10 000 requests
asynchronously in the same amount of time it was taking my website to do around 10 or so requests in the same amount of time, and after looking at the AIOHTTP docs 
again (https://docs.aiohttp.org/en/stable/http_request_lifecycle.html), I improved the loading time for movie.html from 8-9 seconds to 0.76 seconds (almost instant). 
Since all requests are asynchronous, it would not make sense to reduce wait times to lower than 0.7 on the other links (which mostly took around 0.7 s anyways).
In index.html, since it is typically the first screen to load when the user has already logged in, it normally has longer wait times than the others, and so I created 
another TaskGroup to fetch the results of both the 'upcoming movies' and 'top box office movies last weekend' request asynchronously. This reduced the wait time from
1.5 seconds to 0.7 seconds, as expected.

After converting my code to from sync to async (which takes up a lot more code space), I split my program files into more files and directories, including a 
'complete.py' for getting the info for movie.html, 'queries.py' for the other python functions, and 'helpers.py' for the most functions that don't include requests/queries.
I learned from a Stack Overflow post to create a blank __init__.py file to import those functions.

After implementing all details to movie.html, I added buttons on each movie card so the user can access more info about the movie by going to this route.
I want users to be able to search for specific movies from the search bar, so I made method of the form to get to this site 'GET'.


Watchlist:
Surprisingly, as I was testing and debugging this website, I found movies that I wanted to watch later (which I honestly was not actually expecting). 
As I was testing and debugging my website, I noticed a lot of interesting and colourful movie posters that I wanted to save to look at later (ex. look at watchlist screenshot). 
I also found the plots of some of these movies very interesting, too (ex. look at movie screenshots).
I noticed that as you go further back in time, the movies and plots get weirder and weirder. Lots of movies in the 80s and 90s escape the 'isAdult == false' filter and 
I can't do anything about it. Also, many movies have posters, titles, and plots that you simply cannot make up: nazis invading earth from the moon ('Iron Sky'), vaccines 
killing 5 billion people on earth ('Died Suddenly'), the documentary of Mozart told from his apparent murderer ('Amadeus'), a movie starring Ronald Reagan 
prosecuting KKK members (Storm Warning), and straight up satire ('Finding Jesus', instead of 'Finding Nemo').
Some beautiful movie posters include 'Annihilation', 'Spawn', 'Reign of Fire', 'Fear and Loathing in Las Vegas', 'Army of the Dead', and 'Blackbear.'

To create the watchlist feature, I constructed a table for and watchlist and included it in the database schema design. The watchlist table includes a primary key for 
the user id and a primary key for the movie id, since each user can only have a specific movie id once in their watchlist. I then added 'Iron Man' to the database, 
and later 'Annihilation.' I then created a basic watchlist.html file, a navbar in layout.html, and a route to go to watchlist, with methods 'GET' (for seeing watchlist)
and 'POST' (for updating watchlist). I created a function called get_watchlist() which uses a sql query to get a list of all of the movies in the user's watchlist by
their movie_id.
I then created a get_movies_by_list_ids(movies) function which utilizes the title/x/titles-by-ids request from MoviesDatabase to get information about a set of movies 
by their movie ids. Jinja was used to display the poster, id, release date, and title of the movie in a temporary table.


Pagination:
As I continued testing and debugging, I noticed I was not able to view the movies in my watchlist when it had 26 movies in it (possibly fewer earlier).
I thought this was a great time to implement a fusion of a Bootstrap carousel and card grid. I looked at the Bootstrap documentation for a carousel, and included the 
grid I created for search.html inside of the carousel-inner div.
One challenge I noted here was implementing the carousel indicators. The indicators would originally go inside the grid, and so after playing around with pagination and
navbars, I removed the carousel indicators (which could only be placed once), and replaced them with page navigation on both the top and and bottom. As I was testing 
the responsiveness of the design by minimizing the screen size, I noticed that I was not able to use the navbar on the top because of the left and right arrows, and 
since the carousel arrows were only placed on the top row anyways, I decided to remove them. I also noticed that the pages in the carousel only go from left-to-right,
one page at a time (which is typical for a carousel/slideshow), which was originally an unintended feature, but I kept it because it looks better anyways (the prev/left 
button still works).


Icons:
Lastly, I inserted Bootstrap Icons to my project to give a personal touch. 
To keep the 'magic' theme, I included a wizard hat for the logo, which was actually from 'Font-Awesome' fonts (suggested as an alternative to Bootstrap Icons on their site)
as well as a magic wand for finding a movie (Bootstrap Icon). In movie.html, I added a map for filming locations, a medal for movie awards, a globe for countries of
origin, a translate symbol for 'Languages Spoken', a stopwatch for runtime, and a music-note-list icon for soundtrack. I included a palette for the genres because 
when selecting from the list of genres, it is like using a paintbrush to select from a selection of paints on the palette. I included a rocket for the plot of the 
movie because it symbolizes adventure, and when you first start watching a movie, it is like you are lifting off into space to go to another world. I included a 
robot in the 'Revenue and Budget' section because this section typically has a large amount of numbers and dollar signs, and the robot looks like it is calculating 
something, just like how the finances department of a movie production team would do. I also found graph icons with arrows indicating directions, and so in the 
'Ratings' section, I included graph-down-arrow when the movie rating is going down, and graph-up-arrow when the rating is going up.
I included a bootstrap icon that looks like a drivers' license (called person-vcard) in the 'Credentials' section of profile.html because a drivers' license holds a 
lot of personal information about a person, and so it can be associated with the user's username and password. I included a wrench in the 'Update Credentials' section
because it is a tool used to modify things and the user is modifying their username or password.
I found a toggle icon that looks like a switch, and so I inserted it into a button in profile.html and included JavaScript so when the user clicks 'Show Password',
the switch toggles between off and on.    
I included a person icon beside the 'Profile' nav item in the top navbar, too.
To deal with the problem of movies not having a poster, I found a card-image Bootstrap icon, and unlike the other icons, I decided to implement it as a photo, which 
required I download it to my personal computer.

Finally, I reviewed and cleaned up all comments and spacing in each file. I found that js code that worked inside of script tags did not work in seperate js files,
so I just copied each script tag from the files that used js (genres, profile, search) into new js files in their own scripts folder for reference. In the future,
when I figure out how to fix that bug, I will.


Sign off:
For now this project is good, but in the future, after submitting, I plan to implement more features, including username/password validation, user preferences, and 
combining queries so users can filter by multiple 'info' key values in one result.

I finally want to end this README by saying none of this would be possible without the MoviesDatabase api from Adriano Massimo on RapidAPI (which I presume takes data 
from IMDB but it is not stated), as well as the many Stack Overflow posts which helped me through debugging and adding new features, as well as the Harvard CS50x Online
Introduction to Computer Science teaching staff.

