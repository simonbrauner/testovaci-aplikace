function newAnswer(question_number, title) {
    // adding answer
    let answer = document.createElement('LI');
    answer.appendChild(document.createTextNode(title));

    // correct??

    // delete button
    let delete_button = document.createElement('BUTTON');
    delete_button.className = 'btn';
    delete_button.innerHTML = '&times';
    answer.appendChild(delete_button);

    // deleting with the button
    delete_button.addEventListener('click', function() {
	answer.remove();
    });

    // appending to answers element
    let answers = document.getElementsByClassName(question_number)[0];
    answers.insertBefore(answer, answers.lastChild);
}


function newQuestion(title) {
    // question itself
    let question = document.createElement('LI');
    question.id = document.getElementsByClassName('question').length;
    question.className = 'question';

    // title
    let question_title = document.createElement('STRONG');
    question_title.appendChild(document.createTextNode(title));

    // delete button
    let delete_button = document.createElement('BUTTON');
    delete_button.className = 'btn';
    delete_button.innerHTML = '&times';
    question_title.appendChild(delete_button);

    // deleting
    delete_button.addEventListener('click', function() {
	let max_id = parseInt(question.id);
	question.remove();

	// moving indices of questions and answers
	let questions = document.getElementsByClassName('question');
	for (let i = max_id; i < questions.length; i++) {
	    let answers = document.getElementsByClassName(i + 1);
	    for (let j = 0; j < answers.length; j++) {
		answers[j].className -= 1;
	    }

	    questions[i].id -= 1;
	}
    });

    // adding node for answers
    let answers = document.createElement('UL');
    answers.className = question.id;

    // creating input and button for new answers
    let answer_title = document.createElement('INPUT');
    answer_title.type = 'text';
    answer_title.placeholder = 'Odpoved';
    answer_title.autocomplete = 'off';

    let answer_button = document.createElement('BUTTON');
    answer_button.className = 'btn btn-primary';
    answer_button.appendChild(document.createTextNode('Nova odpoved'));

    answer_button.addEventListener('click', function() {
	if (answer_title.value) {
	    newAnswer(question.id, answer_title.value);
	    answer_title.value = '';
	}
    });

    // appending to question
    let input = document.createElement('LI');
    input.appendChild(answer_title);
    input.appendChild(answer_button);
    answers.appendChild(input);

    question.appendChild(question_title);
    question.appendChild(answers);

    // appending to the document
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
