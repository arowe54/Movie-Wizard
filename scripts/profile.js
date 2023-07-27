$(document).ready(function() {
    // When user clicks show password button
    $('show_password').click(function() {
        // Save original style
        style = $('original_pwd').attr('style');
        console.log(style)

        // If its already hidden
        if (style == '-webkit-text-security: disc'){
            // Show the password
            $('original_pwd').attr('style', '-webkit-text-security: none');
        }
        else {
            // Hide the password
            $('original_pwd').attr('style', '-webkit-text-security: disc');
        }
    })
})