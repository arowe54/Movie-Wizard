const { JSDOM } = require( "jsdom" );
const { window } = new JSDOM( "" );
const $ = require( "jquery" )( window );


document.addEventListener("DOMContentLoaded", function() {
    // Maybe creating a "show" function would be more adaptable
    // When user clicks show password button
    document.getElementById("show_password").addEventListener("click", function() {
        // Save original style
        style = document.getElementById("original_pwd").getAttribute('style');
        console.log(style);

        // If its already hidden
        if (style == '-webkit-text-security: disc'){
            // Show password
            document.getElementById('original_pwd').setAttribute('style', '-webkit-text-security: none');
        }
        else {
            // Encrypt password
            document.getElementById('original_pwd').setAttribute('style', '-webkit-text-security: disc');
        }
    })

    // When user clicks update username
    $('#update_username').click(function() {
        // Append a form just below the change username button
        $('#update_username_form').html(`
            <p> Username: {{ username }} </p>
            <form name="change_username" action="/update_user" method="post">
                <p> New Username:
                    <input type="text" name="new_username" id="new_username" autocomplete="off">
                    <button type="submit">Submit</button>
                </p>
            </form>
            `
            );
    })

    // When user clicks update password
    $('#update_pwd').click(function() {
        // Append a form just below the change username button
        $('#update_pwd_form').html(`
            <p> Password: <span class="-webkit-text-security: disc" id="show_pwd2">{{ session["password"] }}</span> </p>
            <button>Show password</button>
            <form name="change_pwd" action="/update_user" method="post">
                <p> New Password:
                    <input type="password" name="new_pwd" id="new_pwd">
                    <button type="submit">Submit</button>
                </p>
            </form>
            `
            );
    })
})

/*
$(document).ready(function() {
    // Maybe creating a "show" function would be more adaptable
    // When user clicks show password button
    $('#show_password').click(function() {
        // Save original style
        style = $('#original_pwd').attr('style');

        // If its already hidden
        if (style == '-webkit-text-security: disc'){
            // Show password
            $('#original_pwd').attr('style', '-webkit-text-security: none');
        }
        else {
            // Encrypt password
            $('#original_pwd').attr('style', '-webkit-text-security: disc');
        }
    })

    // When user clicks update username
    $('#update_username').click(function() {
        // Append a form just below the change username button
        $('#update_username_form').html(`
            <p> Username: {{ username }} </p>
            <form name="change_username" action="/update_user" method="post">
                <p> New Username:
                    <input type="text" name="new_username" id="new_username" autocomplete="off">
                    <button type="submit">Submit</button>
                </p>
            </form>
            `
            );
    })

    // When user clicks update password
    $('#update_pwd').click(function() {
        // Append a form just below the change username button
        $('#update_pwd_form').html(`
            <p> Password: <span class="-webkit-text-security: disc" id="show_pwd2">{{ session["password"] }}</span> </p>
            <button>Show password</button>
            <form name="change_pwd" action="/update_user" method="post">
                <p> New Password:
                    <input type="password" name="new_pwd" id="new_pwd">
                    <button type="submit">Submit</button>
                </p>
            </form>
            `
            );
    })
})
*/

