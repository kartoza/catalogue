function checkUrlAndInput() {
    const urlContains = window.location.href.includes('edit/?next=/add_order/');
    const firstNameInput = document.getElementById('id_first_name');

    if (urlContains && firstNameInput && firstNameInput.value.trim() === '') {
        document.getElementById("error-msg").style.display = 'block'
        return true;
    }

    console.log('Condition not met.');
    return false;
}

// Example usage
checkUrlAndInput();
