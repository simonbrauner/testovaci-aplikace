/*
Testovací aplikace
Šimon Brauner
26.4.2021

index.js

Accessing public tests from main page.
*/


document.addEventListener('DOMContentLoaded', function() {
    // redirect to test
    let redirect_button = document.getElementById('test-redirect');
    if (redirect_button) {
	redirect_button.addEventListener('click', function() {
	    let test_id = document.getElementById('test-id').value;

	    if (test_id) {
		window.location = '../test/' + test_id;
	    }
	});
    }
});
