function questionCount() {
    return document.getElementsByClassName('question').length;
}


function newAnswer(question_number, title, correct) {
    // adding answer
    let answer = document.createElement('LI');

    // title
    let answer_title = document.createElement('STRONG');
    answer_title.appendChild(document.createTextNode(title));
    answer.appendChild(answer_title);

    // correct
    let correct_button = document.createElement('BUTTON');
    correct_button.className = 'btn incorrect';
    correct_button.innerHTML = '&cross;';
    correct_button.style.backgroundColor = '#ecb0b5';
    answer.insertBefore(correct_button, answer_title);

    // changing the correctness
    correct_button.addEventListener('click', function() {
	if (correct_button.className == 'btn incorrect') {
	    correct_button.className = 'btn correct';
	    correct_button.innerHTML = '&check;';
	    correct_button.style.backgroundColor = '#c5ecb0';
	} else {
	    correct_button.className = 'btn incorrect';
	    correct_button.innerHTML = '&cross;';
	    correct_button.style.backgroundColor = '#ecb0b5';
	}
    });

    // changing to correct automatically
    if (correct) {
	correct_button.click()
    }

    // delete button
    let delete_button = document.createElement('BUTTON');
    delete_button.className = 'btn';
    delete_button.innerHTML = '&times;';
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
    question.id = questionCount();
    question.className = 'question';

    // title
    let question_title = document.createElement('STRONG');
    question_title.appendChild(document.createTextNode(title));
    question.appendChild(question_title);

    // delete button
    let delete_button = document.createElement('BUTTON');
    delete_button.className = 'btn';
    delete_button.innerHTML = '&times';
    question.appendChild(delete_button);

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
	    newAnswer(question.id, answer_title.value, false);
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

    // saving the test
    document.getElementById('save').addEventListener('click', function() {
	// general test info
	let test = {
	    questions: []
	}

	// questions
	let questions = document.getElementsByClassName('question');

	for (let i = 0; i < questions.length; i++) {
	    let question = {
		title: questions[i].childNodes[1].innerHTML,
		answers: []
	    }

	    // answers
	    let answers = document.getElementsByClassName(i)[0].childNodes;

	    for (let j = 0; j < answers.length - 1; j++) {
		let nodes = answers[j].childNodes;

		let answer = {
		    title: nodes[1].innerHTML,
		    correct: nodes[0].className == 'btn correct'
		}

		question.answers.push(answer);
	    }

	    test.questions.push(question);
	}

	// submitting
	document.getElementById('secret-input').value = JSON.stringify(test);
	document.getElementById('secret-button').click()
    });
});
