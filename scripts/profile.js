$(document).ready(function() {
    // Show password when user clicks show password button
    function togglePassword(id) {
        style = $(id).attr('style');
        if (style == '-webkit-text-security: disc') {
            // Show password
            $(id).attr('style', '-webkit-text-security: none');
            // Show on icon
            text = 'Hide Password: <i class="bi bi-toggle-on"></i>';
            $(id).parent().next().html(text);
        }
        else {
            // Encrypt password
            $(id).attr('style', '-webkit-text-security: disc');
            // Show off icon
            text = 'Show Password: <i class="bi bi-toggle-off"></i>';
            $(id).parent().next().html(text);
        }
    }

    // Show/hide password when either 'show password' button is clicked
    $('#show_pwd').click(function() {
        togglePassword('#original_pwd');
    })
    $('#show_pwd2').click(function() {
        togglePassword('#original_pwd2')
    })

    // Hide both divs before they can be clicked
    $("#update_username_form").hide()
    $('#update_pwd_form').hide()

    // When user clicks update username
    $('#update_username').click(function() {
        // Show the 'change username' form
        $("#update_username_form").toggle()
    })

    // When user clicks update password
    $('#update_pwd').click(function() {
        // Show the 'change password' form
        $('#update_pwd_form').toggle()
    })
})
