<script>
    $('document').ready(function () {

        // When the user types in anything to the search form (change from any key to a character)
        $('#search_form input[type="search"]').on( "keypress", function ( event ) {

            // Temporarily erase default result
            $('#first_results').hide();
            $('#num_results').html("Results: ");

            // Save the title
            var title = $('#search_form input[type="search"]').val();
            title = title + event.key;

            // Prepare Ajax request
            const settings = {
            async: true,
            crossDomain: true,
            url: 'https://moviesdatabase.p.rapidapi.com/titles/search/title/' + String(title) + '?exact=true&titleType=movie',
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': '515955a8bbmsh7bacf3e7bb3ed33p1ef576jsna2431a83680e',
                'X-RapidAPI-Host': 'moviesdatabase.p.rapidapi.com'
            }
            };
            // Send request
            $.ajax(settings).done(function (response) {
                // Create an temporary div
                temp_div = $('<div class="row row-cols-3" id="temp_div"></div>');

                var resp = response.results;
                // Update the number of results
                $('#num_results').html("Results: " + resp.length);

                // For each movie
                for (let i = 0; i < resp.length; i++) {
                    // Create a card

                    let movie = resp[i];

                    // Create card image
                    if (resp[i].primaryImage) {
                        card_img = '<img src="' + movie.primaryImage.url + '" class="card-img-top w-100" alt="' + movie.primaryImage.caption.plainText + '">';
                    }
                    else {
                        card_img = '<img src="../static/card-image.svg" class="card-img-top w-100" alt="Bootstrap">';
                    } 

                    // card title
                    let card_title = '<h5 class="card-title">' + movie.titleText.text + '</h5>';

                    // runtime
                    let date = 'NA';
                    if (movie.releaseDate) {
                        date = movie.releaseDate.day + '/' + movie.releaseDate.month + '/' + movie.releaseDate.year;
                    }
                    let card_text = `
                            <p class="card-text"><small class="text-body-secondary">
                                ` + date + `
                            </small></p>`;

                    // more_info button
                    let more_info_form = `
                        <form action="/movie" method="get" id="movie.id" >
                            <input type="hidden" name="movie_id" value="` + movie.id + `">
                            <button type="submit" class="btn btn-outline-primary">More info</button>
                        </form>
                    `;

                    // Get movies in watchlist
                    let watchlist = $('#watchlist_movies').html();
                    let id = movie.id;
                    let update_watch_form = '';
                    // Get the correct watchlist form
                    if (watchlist.includes(id)) {
                        update_watch_form = `
                            <form name="removeWatch" id="removeWatch" action="/watchlist" method="post">
                                <input type="hidden" name="movie_id" value=` + String(id) + `">
                                <input type="hidden" name="action" id="action" value="remove">
                                <button type="submit" class="btn btn-outline-primary" onclick="this.form.submit()">Remove from Watchlist</button>  
                            </form>
                        `;
                    }
                    else {
                        update_watch_form = `
                            <form name="addWatch" id="addWatch" action="/watchlist" method="post">
                                <input type="hidden" name="movie_id" value="` + String(id) + `">
                                <input type="hidden" name="action" id="action" value="add">
                                <button type="submit" class="btn btn-outline-primary" onclick="this.form.submit()" {{"disabled" if not session["user_id"] }}>Add to Watchlist</button>
                            </form>
                        `;
                    }

                    // Format the card to append later
                    let card = `
                    <div class="col card">
                        ` + card_img + `
                        <div class="card-body"> 
                            ` + card_title + card_text + `
                        </div>

                        <div class="card-footer">
                            <div class="btn-group" role="group" aria-label="Advanced movie options">
                                <!--Click button and it goes to more info about the movie-->
                                ` + more_info_form + `
                                <!--Update Watchlist-->
                                ` + update_watch_form + `
                            </div>
                        </div>
                    </div>`;

                    // Append card to the temporary div
                    temp_div.append(card);
                }
                // Change the html of the page to this temporary div
                $('#new_results').html( temp_div );
                // Show results
                $('#new_results').show();
            });                
        })
    })
</script>