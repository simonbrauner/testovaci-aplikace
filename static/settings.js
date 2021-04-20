function setTestLink(id, link) {
    let test_link = document.getElementById('test-link');

    let link_string = window.location.href.split('settings')[0];
    link_string += 'test/' + id + '/' + link;

    test_link.innerHTML = link_string;
    test_link.href = link_string;
}


document.addEventListener('DOMContentLoaded', function() {
    // loading test from JSON
    let file_input = document.getElementById('file-input');
    file_input.addEventListener('change', function() {
	let reader = new FileReader();
	reader.onload = function() {
	    document.getElementById('test-json').value = reader.result;
	};
	reader.readAsText(file_input.files[0]);
    });

    // and saving after clicking the button
    document.getElementById('visible-submit').addEventListener('click', function() {
	document.getElementById('hidden-submit').click();
    });
});
