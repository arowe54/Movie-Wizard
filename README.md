# Movie Wizard
#### VIDEO DEMO: https://youtu.be/9cXNRzNFBAU
#### Description:
Welcome to Movie Wizard

<p class="lead">Have you every had trouble finding and picking the right movie? Movie Wizard is just the right website for you.

This website uses Javascript, Ajax, Python (Flask, asyncio/aiohttp), HTML, CSS, Jinja, and SQL to help users find and save movies of interest to them.
You can lookup movies by title, filter by genre, save movies you want to watch, and get random movies.</p>

This website is inspired by the CS 50 Finance problem set and the <a href="https://rapidapi.com/SAdrian/api/moviesdatabase/">MoviesDatabase</a> by Adriano Massimo on RapidAPI, which, provides complete and updated data for over 9 million titles ( movies, series and episodes) and 11 million actors / crew and cast members.

Name:

It is called Movie Wizard because the name sounds cool and the ability of the website to get a large selection of movies seemingly out of nowhere and pick a movie out for me quickly makes it feel like magic.

`movies.db` contains a table for the users and a table for the movies in each user's watchlist.

The html pages are all in templates, the javascript is in scripts and each html file, CSS in static, python in helpers, and the main code in app.py

In helpers, complete.py is the query for `movie.html`, requests.py are the functions for the requests, and helpers.py are the extra helper functions.

layout.html:

`layout.html` holds the main navbar and footer or each page entered on the site. This was create using Bootstrap.

both `login.html` and `register.html` are standard login and register pages create using Bootstrap and Flask.
Inspiration: <a href="https://getbootstrap.com/docs/5.3/examples/sign-in/">Sign-in</a> example from the Bootstrap website. 

Validation:
When the user registers, it sends a form to /register in app.py. It checks to see if the username has already been taken, and if it is not, then their password is hashed using a `generate_password_hash(password)` function, and their user info is saved into the 'users' table in sqlite3. 
When the user logs in, they submit a form to /login in app.py. It checks if their username exists, and hashes their password to see whether their password hash is correct.

If the user does not pass validation, an error message is displayed saying what they did wrong (based on the memegen from CS50 Finance in `apology.html`).
When the user registers and/or logs in, their password is saved into a session variable after validation so it can be accessed in the `profile.html` section.


`index.html` is the homepage. It gets and displays random upcoming movies and the 'Top 10 Box Office Movies Last Weekend." 

It does this by using a function with asyncio and aiohttp (in helpers/complete.py) to asynchronously call requests to the MoviesDatabaseAPI, and then using Jinja and Bootstrap to display the movies to the webpage.

It also includes a 'randomize' button, since some movies in 'upcoming' get passed the isAdult = false filter. The gets a random int from 1 to 9 and selects that page number from the request (ex. page 6 of upcoming movies).

Inspiration: <a href="https://getbootstrap.com/docs/5.3/examples/album/#">Album</a> example on Bootstrap


Responsive Design:
The grid of movies is originally displayed in 2 rows of 5, but when the screen is minimized or used on smaller viewports, it changes to show 5 rows with 2 columns of movies in each row.

`search.html`

When you want to search for a movie, the site asynchronoulsy updates to display the search results in a 3 col grid each time the user lets go of the key to a character in their search.

When the user lets go of the key, the site uses Ajax and jQuery to send a request for the exact title to the MoviesDatabaseAPI, and once it is recieved, it updates the movie results on the screen using Jinja syntax.

When the user presses enter in the searchbar to search for their title, the site uses Jinja and Flask to send their search to a `lookup(title)` function in helpers/requests.py, and then updates the screen using Jinja.

The results are displayed in 3 movies per row, and when the user minimizes the screen, it displays 1 movie per row.


`genres.html`

When visiting genres.html, the site goes to the /genres route in app.py, completes a request for the list of genres using `get_genres()`, and displays them in a dropdown.
Some genres (ex. News, Game-Show, etc...) were removed because they didn't show results.

When the user selects a genre from the dropdown, it sends a form via GET to the /genres route, which sends a request for titles filtered by that genre using a `get_movies_by_genre(genre)` function, and displays those results to the screen like in `index.html`.

Each request shows random movies in the genre, and the 'get random movies' button sends the request again.


`movie.html` gets all the info about a certain movie based on its id. 

All cards include a 'more info' button in the footer that, when clicked, goes to the /movie route through GET, which calls a get_all_info(movie) function that returns all available information about the movie in a dictionary. 

To find all the possible info on the movie (<a href="https://rapidapi.com/SAdrian/api/moviesdatabase/details">up to 58 keys</a>), I had to send multiple requests to the same url asynchronously using asyncio and aiohttp and save each key-value pair to a dictionary. Jinja then displays those results to the screen in `movie.html`.
On the bottom of `movie.html`, it displays similar movies in a <a href="https://getbootstrap.com/docs/5.3/components/card/#card-groups">card group</a>.

Switching from synchronous to asynchronous in this section cut down loading time from 15 seconds to 0.75 seconds.

Inspiration:
- <a href="https://docs.aiohttp.org/en/stable/client_quickstart.html">AIOHTTP docs 1</a> and <a href="https://docs.aiohttp.org/en/stable/http_request_lifecycle.html">AIOHTTP docs 2</a>
- <a href="https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html">another website</a> where the user used a TaskGroup and fetch() to do up to 10 000 requests asynchronously in the same amount of time it was taking my website to do around 10


Watchlist:

Users can add (or remove) movies to a watchlist using a checkbox (movies.html), or by clicking 'Add to Watchlist' or 'Remove from Watchlist'. These send requests using POST to update the user's watchlist and then return the user back to whichever page they sent the request from, except with the watchlist updated (ex. showing 'Remove' instead of 'Add')

In watchlist.html, the movies are displayed using a mix of a carousel and card grid in Bootstrap with some minor changes.


`profile.html` displays the user's username and password using jQuery, CSS, and sqlite3 queries.

Lastly, I inserted <a href="https://icons.getbootstrap.com/">Bootstrap Icons</a> to my project to give a personal touch. 

In the future, I would like to test more username/password validation, user preferences, and combining queries so users can filter search results.

P.S.
The video for the demo is on 2.5 speed.
