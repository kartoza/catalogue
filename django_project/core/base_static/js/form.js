$(document).ready(function () {

    var passwordMessage = '<div class="alert alert-info password-message" role="alert">' +
            'Password must contain at least six characters, including: <ul>' +
        '<li> lower case letter </li>' +
        '<li> upper case letter </li>'+
        '<li> numeric character </li></ul>'+
        '</div>';
    $(passwordMessage).insertBefore('#id_password1');
});
