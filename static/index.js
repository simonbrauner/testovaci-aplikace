document.addEventListener('DOMContentLoaded', function() {

    // redirect to test
    document.getElementById('test-redirect').addEventListener('click', function() {
	let test_id = document.getElementById('test-id').value;

	if (test_id) {
	    window.location = '../test/' + test_id;
	}
    });
});
