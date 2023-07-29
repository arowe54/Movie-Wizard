genre = $('#genre_selected').val();
console.log(genre);

function get_movies(genre, page) {
    // Movies
    var movies = {};

    // Ajax
    const data = null;
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    // Do this once the request is sent
    xhr.addEventListener('readystatechange', function () {
        if (this.readyState === this.DONE) {
            console.log("\n\n\n");
            const resp = JSON.parse(this.response);
            const results = resp["results"];
            console.log(results);

            


        }
    });
    
    // Prepare request
    xhr.open('GET', "https://moviesdatabase.p.rapidapi.com/titles?genre=" + String(genre) + "&titleType=movie&page=" + String(page));
    xhr.setRequestHeader('X-RapidAPI-Key', '515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e');
    xhr.setRequestHeader('X-RapidAPI-Host', 'moviesdatabase.p.rapidapi.com');
    // Send Request
    xhr.send(data);
}

get_movies(genre, 1);