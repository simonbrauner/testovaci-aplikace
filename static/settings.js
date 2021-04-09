document.addEventListener('DOMContentLoaded', function() {
    // loading test from JSON
    let file_input = document.getElementById('file-input');
    file_input.addEventListener('change', function(event) {
	let reader = new FileReader();
	reader.onload = function() {
	    document.getElementById('test-json').value = reader.result;
	}
	reader.readAsText(file_input.files[0]);
    });

    // and saving after clicking the button
    document.getElementById('visible-submit').addEventListener('click', function() {
	document.getElementById('hidden-submit').click();
    });
});
