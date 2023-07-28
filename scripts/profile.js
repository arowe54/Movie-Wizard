// Maybe copy each script in each html file to their own js files for references and just don't link to them (bc not possible)
$(document).ready(function() {
    // Function doesn't work, but jquery below does?
    // Show password when user clicks show password button
    function togglePassword(id) {
        style = $(id).attr('style');
        if (style == '-webkit-text-security: disc') {
            // Show password
            $(id).attr('style', '-webkit-text-security: none')
        }
        else {
            // Encrypt password
            $(id).attr('style', '-webkit-text-security: disc')
        }
    }

    // Run showPassword on the two buttons
    $('#show_pwd').click(function() {
        togglePassword('#original_pwd')
    })
    $('#show_pwd2').click(function() {
        togglePassword('#original_pwd2')
    })

    // Hide both divs before they can be clicked
    $("#update_username_form").hide()
    $('#update_pwd_form').hide()

    // When user clicks update username
    $('#update_username').click(function() {
        $("#update_username_form").toggle()
    })

    // When user clicks update password
    $('#update_pwd').click(function() {
        // Append a form just below the change username button
        $('#update_pwd_form').toggle()
    })
})