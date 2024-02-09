$(document).ready(function () {
    // Function to validate email format
    function validateEmail(email) {
        // Simple email format validation using a regular expression
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Function to display error messages with styling
    function displayError(message) {
        $('.messages').empty().append('<li class="error" style="color: red;">' + message + '</li>');
    }

    // Function to remove error messages
    function removeError() {
        $('.messages').empty();
    }

    // Event listener for email input
    $('input[name="email"]').on('input', function () {
        var email = $(this).val();
        removeError();
        if (email.trim() !== '' && !validateEmail(email)) {
            displayError('Invalid email format.');
        }
    });

    // Event listener for password input
    $('input[name="psw"]').on('input', function () {
        removeError();
    });

    // Event listener for form submission
    $('form').submit(function (event) {
        var email = $('input[name="email"]').val();

        // Reset error messages
        $('.messages').empty();

        // Validate email format
        if (!validateEmail(email)) {
            displayError('Invalid email format.');
            event.preventDefault();
        }
    });
});
