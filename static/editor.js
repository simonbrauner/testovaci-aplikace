function newQuestion(title) {
    let question = document.createElement('LI');
    question.id = document.getElementsByClassName('question').length;
    question.className = 'question';
    question.appendChild(document.createTextNode(title));

    document.getElementById('questions').appendChild(question);
}

document.addEventListener('DOMContentLoaded', function() {
    // creating question
    document.getElementById('new-question').addEventListener('click', function() {
	let title = document.getElementById('question-title').value;
	if (title) {
	    newQuestion(title);
	    document.getElementById('question-title').value = '';
	}
    });
});
