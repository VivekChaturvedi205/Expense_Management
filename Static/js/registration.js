$(document).ready(function () {
    // Function to validate password length
    function validatePasswordLength(password) {
        return password.length >= 8;
    }

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

    // Retrieve user type from the hidden element
    var userType = $('#user_type').text().trim();

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
        var password = $(this).val();
        removeError();
        if (password.trim() !== '' && !validatePasswordLength(password)) {
            displayError('Password should be at least 8 characters long.');
        }
    });

    // Event listener for form submission
    $('form').submit(function (event) {
        var password = $('input[name="psw"]').val();
        var confirmPassword = $('input[name="psw1"]').val();
        var email = $('input[name="email"]').val();

        // Reset error messages
        $('.messages').empty();

        // Validate password length based on user type
        if (userType === 'admin' && !validatePasswordLength(password)) {
            displayError('Admin password should be at least 8 characters long.');
            event.preventDefault();
        }

        // Validate email format
        if (!validateEmail(email)) {
            displayError('Invalid email format.');
            event.preventDefault();
        }

        // Validate password match
        if (password !== confirmPassword) {
            displayError('Passwords do not match.');
            event.preventDefault();
        }
    });
});


function goBack() {
    window.history.back();
}