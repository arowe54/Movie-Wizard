# CS50X Web Wizard
#### VIDEO DEMO: <url>
#### Description:
Welcome to Web Wizard

<p class="lead">Have you every had trouble finding and picking the right movie? Web Wizard is just the right website for you.

This website uses Javascript, Python, and SQL to help users find and save movies of interest to them.
You can lookup movies by title, filter by genre, save movies you want to watch, and get random movies.</p>

At first I looked towards the CS50 Finance problem set as inspiration to use a free online API to get data and display it through my project.
I decided to use <a href="https://rapidapi.com/SAdrian/api/moviesdatabase/">MoviesDatabase</a> by Adriano Massimo on RapidAPI, which he says has access to complete and updated data of over 9 million titleswith useful information about each movie. The site also shows how to run each request in multiple languages (ex. python, javascript) and in multiple ways (ex. for js: jQuery vs Fetch). Plus, it is updated weekly.
To access the API, I created an account on RapidAPI and linked to my github account.

Name:

It is called Web Wizard because the name sounds cool and the ability of the website to get a large selection of movies seemingly out of nowhere and pick a movie out for me quickly makes it feel like magic.  Also, as I was filtering the genres in genres.html, I found that the best movies are the ones in mystery, horror, adventure, and fantasy, which all can be associated with Wizards.

To create the backbone of my project, I copied my CS50 Finance submission into a separate folder. This is because it uses a lot of similar features (ex. sessions, after_request, usd, etc...), while still adding new ones.


Database Schema Diagram

At first, I created a diagram to visualize how the user data would be collected and manipulated in sqlite3.
I created a table for users, which includes a primary key for the 'id' of the user that autoincrements, their 'username', and the hash of their password.
The 'watchlist' table contains a column of the user_id, and a column for the movie_id of the movie in their watchlist. Both are primary keys, since each user can only have one movie with the same movie_id. The user_id is a foreign key that references the id column of the user table.
I used this as a basis to create the movies.db

layout.html:

At first I created layout.html, which holds the main navbar that you see at the top of each website, with a nav-brand logo, a search bar, and a nav-item for each page to navigate to within the site. When the user minimizes the screen, the top navbar collapses, and the user can press the button on the top right to un-collapse it.


Login/Register:

I based my design for the login (login.html) and register (register.html) pages on the CS50 Finance assignment and the <a href="https://getbootstrap.com/docs/5.3/examples/sign-in/">Sign-in</a> example from the Bootstrap website. 
When the user registers, it sends a form to /register in app.py. It checks to see if the username has already been taken, and if it is not, then their password is hashed using a generate_password_hash(password) function, and their user info is saved into the 'users' table in sqlite3. 
When the user logs in, they submit a form to /login in app.py. It checks if their username exists, and hashes their password to see whether their password hash is correct.
If the user does not pass validation, an error message is displayed saying what they did wrong (based on the memegen from CS50 Finance in apology.html).
When the user registers and/or logs in, their password is saved into a session variable after validation so it can be accessed in the profile.html section.


Index:

The first thing I decided to do was get and show the upcoming movies and top box office movies from last weekend on the home page of the site.
This was done by creating a abstracting them into a function for get_upcoming() and a function for get_top_box()*.
get_upcoming() used a request with the url: titles/x/upcoming, as well as parameters for the titleType (always movie), starting in 2023 and ending in 2026, and sort by year increasing. 
get_top_box() used a standard request for /titles and selects titles from the list: "top_boxoffice_last_weekend_10".

<small>*Note: these 2 functions were later combined into 1 function with 2 requests (index_queries(x)) using asyncio and aiohttp (see Asyncio section)</small>

Sometimes a user might not like the results that they see, and so I implemented a "randomize" button that randomizes the upcoming movies that the user sees. It does this by using the random python module to generate a random int from 1 to 9 (because this request only shows 9 pages), and then it passes that number through the function to display the results for that page in upcoming movies (ex. pg 5).

After reviewing the  <a href="https://getbootstrap.com/docs/5.3/examples/album/#">Album</a> example on Bootstrap, I decided to create a Jumbotron in index.html to hold the Logo, a lead paragraph, and a button to get a movie.
One challenge was being very redundant with jinja if-else statements because some features were not in all movies (ex. primaryImage, plot), while others were (ex. id, title).

At first, I displayed the results in a table for each request, with each table having a column for the poster, a column for the ids and title, and a column for the release date. The ids were only for testing purposes, and were later removed.
I then used <a href="https://getbootstrap.com/docs/5.3/components/card/#grid-cards">Grid Cards</a> from Bootstrap with the row-cols-sm-5 class to display 2 rows of 5 movies (10 results) on my Dell laptop, with each movie displayed in a <a href="https://getbootstrap.com/docs/5.3/components/card/#content-types">Card</a>.

Responsive Design:
The grid of movies changes to show 5 rows with 2 columns of movies in each row when the webpage is minimized to a smaller viewport (row-cols-2).


Lookup:

At first, I created a /search route and a lookup(title) function that sends a request to an API for a specific movie based on its title, and then displays the results using Jinja, which is similar to the lookup feature in CS50 Finance.

The results were displayed in a grid of cards similar to index, except with 3 per row so the user can see the poster better, while also being able to see a large proportion of the results without having to scroll down.
I experimented using horizontal cards with one movie per row, but found that it either looked too small when it was 1 per row, or when it was too large, the sizing ratio of poster-to-movie-info was too large.
When the user uses a small screen, it displays only one movie per row.

Ajax search.html:

After this, I decided to use ajax and jQuery to update the search responses as the user types each key into the search bar of that page. This was becasue it is a cool feature and becasue it can get annoying when you enter a title and it shows no movie found. I also added a feature where it outputs the number of results to the top of the page.
The page is separated into 'new_results' and 'original_results' divs. 
When the user presses a key into the search bar, the program uses jQuery to hide the 'original_results' (random movies), gets a request for the movie from the title via ajax, and displays the results in a grid of cards (3 per row). 
In Ajax, in order to show the result of the request, an empty div is created and the response's 'results' value is saved. Then it loops over each movie in the result, converts it to a card using template literals, and appends the card to the div. 
Once it is done iterating, it changes the html of the 'new_results' div to this resulting div using jQuery.

One challenge faced was that every time a user pressed a key, it would save the value of the input as the title it was before the key was pressed, so I had to append the key pressed to the title in the search request.


Genres:

When visiting the /genres route in app.py, it completes a request for the list of genres using get_genres() and uses jinja to display all of them in a dropdown in genres.html. After testing, some genres (ex. News, Game-Show, etc...) were removed because they didn't show results.
When the user selects a genre from the dropdown, it sends a form via GET to the /genres route, which sends a request for titles filtered by that genre using a get_movies_by_genre(genre) function, and displays those results to the screen in a 5x2 grid (like index.html). 
get_movies_by_genre(genre) sends a request to the url /x/random with a query parameter for the genre of the movies. The movies are random each time because I found that when it uses the /titles url which is not random, it gets the same movies from the late 1800s each time, and it is better for the user to have more variety.
This is also why I implemented a 'get more movies' button where the user sends the request again to get more random movies in that genre. I find this is suprisingly effective and I have actually found a lot of movies that I would like to watch through the random buttons.


movie.html:

movie.html gets all the info about a certain movie based on its id. 
All cards include a 'more info' button in the footer, that, when clicked, goes to a /movie route through GET, which calls a get_all_info(movie) function that returns all available information about the movie in a dictionary. 
To find all the possible info on the movie (<a href="https://rapidapi.com/SAdrian/api/moviesdatabase/details">up to 58 keys</a>), I had to create an empty dictionary, send multiple requests to the same url with different values for the "info" parameter (ex."base_info", "revenue_and_budget", "awards", "filmingLocations", etc...), iterate through the result of each request and save each key-value pair to the saved dictionary. Jinja then displays those results to the screen in movie.html.
On the bottom of movie.html, I implemented the 'moreLikeThis' feature, which displays similar movies in a <a href="https://getbootstrap.com/docs/5.3/components/card/#card-groups">card group</a>, which I learned from the Bootstrap website.

One problem I found was that in soundtrack, it would print the html of the comments to the screen (including anchor tags and divs) instead of the what was actually inside of the html. To fix this, I used the 'safe' jinja filter.


Asyncio:

It was at this point that I realized that the website was taking way too long to load. This was because of the get_all_info(id) and home page functions had to recieve multiple requests for the page to finish loading. In order to add and test more features (which would requre booting up the site each time), I had to reduce the latency of the site by loading each request asynchronously. I discovered through Stack Overflow I could use asyncio and aiohttp to complete several requests at the same time. I installed both features with pip and imported them.
Before I started working on improving the latency, I timed the current speed of loading index.html and movie.html. I temporarily recorded each time in an 'extra.txt' file by importing time, recording start_time = time.time() in the beginning of each route, and printing time.time() - start_time at the end.
I referred to the <a href="https://docs.aiohttp.org/en/stable/client_quickstart.html">AIOHTTP docs</a> to get each request using 'async with' syntax, and found that this improved the wait time from 12-15 seconds, to 8-9 seconds, which was still too long.
I found <a href="https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html">another website</a> where the user used a TaskGroup and fetch() to do up to 10 000 requests asynchronously in the same amount of time it was taking my website to do around 10 or so requests in the same amount of time. After looking at the AIOHTTP docs <a href="https://docs.aiohttp.org/en/stable/http_request_lifecycle.html">again</a>, I implemented a TaskGroup using fetch() and improved the loading time for movie.html from 8-9 seconds to 0.76 seconds <b>(almost instant)</b>. 
Since all requests are asynchronous, it would not make sense to reduce wait times to lower than 0.7 on the other links (which mostly took around a second anyways).
In index.html, it took longer to load because it used two requests, and it was also typically the first screen to load. I created another TaskGroup to fetch the results of both the 'upcoming movies' and 'top box office movies last weekend' request asynchronously, which reduced the wait time from 1.5 seconds to 0.7 seconds, as expected.

File Structure:

At this point my helpers.py function was very long, so I moved it into a helpers folder (with a blank __init__.py file), and split helpers.py into complete.py (for 'get_all_info(movie)' in movie.html), requests.py (for the functions containing requests), and helpers.py (for the functions that don't include requests; ex. secToMin(seconds) and usd).
I should note that I included all JavaScript from each html file into a 'scripts' folder, but none of it has worked after importing it into each html file and deleting the pre-existing js in that file, so I have kept each js inside the scripts and just kept the scripts folder for reference.


Watchlist:

Surprisingly, as I was testing and debugging this website, I found movies that I wanted to watch later (which I honestly was not expecting). 
As I tested and debugged my website, I noticed a lot of interesting and colourful movie posters that I wanted to save to look at later. 
I also found the plots of some of these movies very interesting, too.
I noticed that as you go further back in time, the movies and plots get weirder and weirder. Lots of movies in the 80s and 90s escape the 'isAdult == false' filter and I can't do anything about it. 
Also, many movies have posters, titles, and plots that you simply cannot make up: nazis invading earth from the moon (<a href="http://127.0.0.1:5000/movie?movie_id=tt1034314">'Iron Sky'</a>), vaccines killing 5 billion people on earth (<a href="http://127.0.0.1:5000/movie?movie_id=tt23810972">'Died Suddenly'</a>), a movie starring Ronald Reagan prosecuting KKK members (<a href="http://127.0.0.1:5000/movie?movie_id=tt0044075">Storm Warning</a>), and straight up satire (<a href="http://127.0.0.1:5000/movie?movie_id=tt12981810">'Finding Jesus'</a>, instead of 'Finding Nemo').
I also noticed a benefit of this website is you can get a much better view of the poster and plot on a laptop screen, as compared to a TV wih Netflix.
Some cool movie posters include <a href="http://127.0.0.1:5000/movie?movie_id=tt2798920">'Annihilation'</a>, <a href="http://127.0.0.1:5000/movie?movie_id=tt0120177">'Spawn'</a>, <a href="http://127.0.0.1:5000/movie?movie_id=tt0253556">'Reign of Fire'</a>, <a href="http://127.0.0.1:5000/movie?movie_id=tt0120669">'Fear and Loathing in Las Vegas'</a>, <a href="http://127.0.0.1:5000/movie?movie_id=tt0993840">'Army of the Dead'</a>, and <a href="http://127.0.0.1:5000/movie?movie_id=tt9601220">'Blackbear'</a>.

**Note: Movie links can only be accessed through the flask server.

I then created a watchlist.html file, a navbar in layout.html, and a route to go to watchlist, with methods 'GET' (for seeing watchlist) and 'POST' (for updating watchlist). 
I then added 'Iron Man' to the database, and later 'Annihilation', for testing.
I created a function called get_watchlist() in requests.py which uses a sql query to get a list of all of the movies in the user's watchlist by their movie_id. I then created a get_movies_by_list_ids(movies) function which utilizes the title/x/titles-by-ids request from MoviesDatabase to get information about a set of movies by their movie ids. Jinja was used to display the poster, id, release date, and title of the movie in a temporary table.

I then created a checkbox form where the user can update their watchlist.
I used the get_watchlist() function and a jinja loop to check if the current movie id is not in the list of movie ids in the watchlist.
If the movie is not in the watchlist, it adds an empty check box. When the user clicks the box, the 'onchange' attribute submits a from with the movie id to POST in the /watchlist route, and a sqlite3 query inserts the movie id into the watchlist corresponding to that user's id.
Return redirect(request.referrer) returns the user back to the page where they updated the movie to the watchlist, where the checkbox is automatically checked.
The website automatically checks the box each time the movie is in the watchlist, and when the user unchecks the checkbox, it submits another form via POST to the /watchlist route that deletes the row in watchlist with the movie id and user id. This means that whenever a movie is in the watchlist, it is checked, and when it is not, it is unchecked.

The checkbox is used in movies.html, but in index.html, genres.html, and search.html, the button switches from 'Add to Watchlist' to 'Remove from Watchlist' instead, because it is more aesthetically pleasing. Also, in watchlist.html, only a 'remove from watchlist' button is used.


Pagination:

As I continued testing and debugging, I noticed I was not able to view the movies in my watchlist when it had 26 movies in it (possibly fewer earlier).
I thought this was a great time to implement a fusion of a Bootstrap carousel and card grid to show several pages of the watchlist. I looked at the Bootstrap documentation for a carousel, and included the grid I created for search.html inside of the carousel-inner div.
One challenge I noted here was implementing the carousel indicators. The indicators would originally go inside the grid, and so after playing around with pagination and navbars, I removed the carousel indicators (which could only be placed once), and replaced them with page navigation buttons on both the top and bottom. I removed the typical left and right slide show arrows from the carousel because I was not able to uncollapse the navbar when the screen was minimized, and because the arrows were only in the first row of movies, which did not look good.
The page navigation buttons only go from left to right, one page at a time (which is typical for a slide show), but the left/prev button still works.


Profile:

After this, I decided to add profile.html and a /profile route where the user can access and change their username and password.
The user accesses their username through a sqlite3 query and displays it through jinja. The user accesses their passsord by accessing a session variable, which is passed as a jinja variable.
At first, each of the passwords are hidden by using a style="-webkit-text-security: disc" in a span tag.
profile.html uses jQuery functions so that when a person clicks the 'show password' button, it passes the id of that button through a function that checks its style, and changes 'disc' to 'none' in order to show the password, and 'none' to 'disc' to hide the password.
The username can change their username or password by clicking the 'change username' or 'change password' buttons, which toggle a div for each form. When the user submits the new username or password, it passes it through POST in the /profile route and validates it the same way that register.html does. Then, it returns profile.html.

Icons:

Lastly, I inserted <a href="https://icons.getbootstrap.com/">Bootstrap Icons</a> to my project to give a personal touch. 
To keep the 'magic' theme, I included a wizard hat for the logo, which was actually from 'Font-Awesome' fonts (suggested as an alternative to Bootstrap Icons on their site) as well as a magic wand for finding a movie (Bootstrap Icon). 
In movie.html, I added a map for filming locations, a medal for movie awards, a globe for countries of origin, a translate symbol for 'Languages Spoken', a stopwatch for runtime, and a music-note-list icon for soundtrack. I included a palette for the genres because when selecting from the list of genres, it is like using a paintbrush to select from a selection of paints on the palette. I included a rocket for the plot of the movie because it symbolizes adventure, and when you first start watching a movie, it is like you are lifting off into space to go to another world. I included a robot in the 'Revenue and Budget' section because this section typically has a large amount of numbers and dollar signs, and the robot looks like it is calculating something, just like how the finances department of a movie production team would do. I also found graph icons with arrows indicating directions, and so in the 'Ratings' section, I included graph-down-arrow when the movie rating is going down, and graph-up-arrow when the rating is going up.
I included a bootstrap icon that looks like a drivers' license (called person-vcard) in the 'Credentials' section of profile.html because a drivers' license holds a lot of personal information about a person, and so it can be associated with the user's username and password. I included a wrench in the 'Update Credentials' section because it is a tool used to modify things and the user is modifying their username or password. I found a toggle icon that looks like a switch, and so I inserted it into a button in profile.html and included JavaScript so when the user clicks 'Show Password', the switch toggles between off and on.    
I included a person icon beside the 'Profile' nav item in the top navbar, too.
To deal with the problem of movies not having a poster, I found a card-image Bootstrap icon, and unlike the other icons, I decided to implement it as a photo, which required I download it to my personal computer.

Finally, I reviewed and cleaned up all comments and spacing in each file. I found that js code that worked inside of script tags did not work in seperate js files, so I just copied each script tag from the files that used js (genres, profile, search) into new js files in their own scripts folder for reference. In the future, when I figure out how to fix that bug, I will.


Sign off:
For now this project is good, but in the future, after submitting, I plan to implement more features, including username/password validation, user preferences, and combining queries so users can filter by multiple 'info' key values in one result.

I finally want to end this README by saying none of this would be possible without the MoviesDatabase api from Adriano Massimo on RapidAPI (which I presume takes data from IMDB but it is not stated), as well as the many Stack Overflow posts which helped me through debugging and adding new features, as well as the Harvard CS50x Online Introduction to Computer Science teaching staff.

