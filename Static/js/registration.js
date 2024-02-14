$(document).ready(function () {
    function validatePasswordLength(password) {
        return password.length >= 8;
    }

    function validateEmail(email) {
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    function displayError(message) {
        $('.messages').empty().append('<li class="error" style="color: red;">' + message + '</li>');
    }
    function removeError() {
        $('.messages').empty();
    }
    var userType = $('#user_type').text().trim();
    $('input[name="email"]').on('input', function () {
        var email = $(this).val();
        removeError();
        if (email.trim() !== '' && !validateEmail(email)) {
            displayError('Invalid email format.');
        }
    });
    $('input[name="psw"]').on('input', function () {
        var password = $(this).val();
        removeError();
        if (password.trim() !== '' && !validatePasswordLength(password)) {
            displayError('Password should be at least 8 characters long.');
        }
    });
    $('form').submit(function (event) {
        var password = $('input[name="psw"]').val();
        var confirmPassword = $('input[name="psw1"]').val();
        var email = $('input[name="email"]').val();
        $('.messages').empty();
        if (userType === 'admin' && !validatePasswordLength(password)) {
            displayError('Admin password should be at least 8 characters long.');
            event.preventDefault();
        }
        if (!validateEmail(email)) {
            displayError('Invalid email format.');
            event.preventDefault();
        }

        if (password !== confirmPassword) {
            displayError('Passwords do not match.');
            event.preventDefault();
        }
    });
});


function goBack() {
    window.history.back();
}