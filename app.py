from flask import request, session
from flask import render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from json import loads
from random import shuffle

from config import app, db
from model import User, Test, Question, Answer, Submit, Response
from tools import create_test_link
from tools import clear_test, delete_test
from tools import login_required, creator_only


@app.route('/test/<int:test_id>/<string:link>', methods=['GET', 'POST'])
def test_without_login(test_id, link):
    test = Test.query.filter_by(id=test_id).first()

    if not test or link != test.link or not test.private_access:
        return 'Špatný odkaz na test.'

    if request.method == 'GET':
        questions = test.questions.copy()

        shuffle(questions)
        questions = questions[:test.parts]

        # creating anonymous user
        user = User()
        submit = Submit(test=test, taker=user)

        for question in questions:
            submit.responses.append(Response(question_id=question.id))

        db.session.add(user)
        db.session.add(submit)
        db.session.commit()

        # remembering user
        session['anonymous-id'] = user.id

        return render_template('test_without_login.html',
                               user=user, test=test,
                               questions=questions, link=link)

    # saving results
    if not test.solution or 'anonymous-id' not in session:
        return 'Test byl vyplňen.'

    user = User.query.filter_by(id=session['anonymous-id']).first()

    # forgetting
    session.clear()

    name = request.form.get('name')

    if name:
        user.name = name

        db.session.add(user)
        db.session.commit()

    submit = Submit.query.filter_by(test=test, taker=user).first()

    score = 0

    for response in submit.responses:
        answer_id = request.form.get(str(response.question_id))

        if answer_id:
            answer = Answer.query.filter_by(id=answer_id).first()

            if answer.correct:
                score += 1

            response.answer = answer

    submit.score = score

    db.session.add(submit)
    db.session.commit()

    responses = submit.responses

    # NOT available
    return render_template('solution.html', test=test,
                           submit=submit, responses=responses)


@app.route('/test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def test(test_id):
    user = User.query.filter_by(id=session['id']).first()
    test = Test.query.filter_by(id=test_id).first()

    submit = Submit.query.filter_by(test=test, taker=user).first()

    if not test.access and user.id != test.creator_id:
        return redirect('/')

    if request.method == 'GET':
        if not submit:
            # generating test
            questions = test.questions.copy()

            if not questions:
                return redirect('/')

            shuffle(questions)
            questions = questions[:test.parts]

            if user.id != test.creator_id:
                submit = Submit(test=test, taker=user)

                for question in questions:
                    submit.responses.append(Response(question_id=question.id))

                db.session.add(submit)
                db.session.commit()

            return render_template('test.html', user=user,
                                   test=test, questions=questions)

        if submit.score is None:
            # test was generated but not finished
            questions = [response.question for response in submit.responses]

            return render_template('test.html', user=user,
                                   test=test, questions=questions)

        else:
            # test finished and showing solution
            return redirect(f'/solution/{test_id}')

    # saving results
    score = 0

    for response in submit.responses:
        answer_id = request.form.get(str(response.question_id))

        if answer_id:
            answer = Answer.query.filter_by(id=answer_id).first()

            if answer.correct:
                score += 1

            response.answer = answer

    submit.score = score

    db.session.add(submit)
    db.session.commit()

    return redirect(f'/test/{test_id}')


@app.route('/solution/<int:test_id>')
@login_required
def solution(test_id):
    user = User.query.filter_by(id=session['id']).first()
    test = Test.query.filter_by(id=test_id).first()
    submit = Submit.query.filter_by(test=test, taker=user).first()

    if not submit or submit.score is None:
        return redirect('/')

    responses = submit.responses

    return render_template('solution.html', test=test,
                           submit=submit, responses=responses)


"""
creator side
"""


@app.route('/editor/<int:test_id>', methods=['GET', 'POST'])
@creator_only
def editor(test_id):
    test = Test.query.filter_by(id=test_id).first()

    if request.method == 'GET':
        return render_template('editor.html', test=test)

    # saving test
    test_json = request.form.get('test-json')
    if not test_json:
        return redirect('/tests')

    clear_test(test)

    test_dict = loads(test_json)

    for question_dict in test_dict['questions']:
        question = Question(name=question_dict['title'])

        for answer_dict in question_dict['answers']:
            question.answers.append(Answer(name=answer_dict['title'],
                                           correct=answer_dict['correct']))

        test.questions.append(question)

    if test.parts == 0 or test.parts > len(test_dict['questions']):
        test.parts = len(test_dict['questions'])

    db.session.add(test)
    db.session.commit()

    return redirect('/tests')


@app.route('/settings/<int:test_id>', methods=['GET', 'POST'])
@creator_only
def settings(test_id):
    test = Test.query.filter_by(id=test_id).first()

    if request.method == 'GET':
        questions = test.questions

        return render_template('settings.html', test=test,
                               questions=questions)

    # saving settings
    parts = request.form.get('parts')
    solution = False
    access = False
    private_access = False

    if parts:
        try:
            parts = int(parts)

            assert parts > 0
            assert parts <= len(test.questions)

            test.parts = parts

        except ValueError:
            return redirect(f'/settings/{test_id}')

        except AssertionError:
            return redirect(f'/settings/{test_id}')

    if bool(request.form.get('solution')) != test.solution:
        test.solution = not test.solution
        solution = True

    if bool(request.form.get('access')) != test.access:
        test.access = not test.access
        access = True

        # deleting unfinished submits
        if not test.access:
            change = False

            submits = Submit.query.filter_by(test=test).all()

            for submit in submits:
                if submit.score is None:
                    change = True

                    for response in submit.responses:
                        db.session.delete(response)

                    db.session.delete(submit)

            if change:
                db.session.commit()

    if bool(request.form.get('private-access')) != test.private_access:
        test.private_access = not test.private_access
        private_access = True

        if not test.link:
            test.link = create_test_link()

        # deleting useless accounts
        if not test.private_access:
            change = False

            submits = Submit.query.filter_by(test=test).all()

            for submit in submits:
                if submit.taker.name is None:
                    change = True

                    for response in submit.responses:
                        db.session.delete(response)

                    taker = submit.taker

                    db.session.delete(submit)
                    db.session.delete(taker)

            if change:
                db.session.commit()

    if any([parts, solution, access, private_access]):
        db.session.add(test)
        db.session.commit()

    return redirect('/tests')


@app.route('/delete/<int:test_id>', methods=['GET', 'POST'])
@creator_only
def delete(test_id):
    test = test = Test.query.filter_by(id=test_id).first()

    count = len([x for x in test.submits if x.score])

    if request.method == 'GET':
        return render_template('delete.html', test=test, count=count)

    delete_test(test)

    return redirect('/')


@app.route('/results/<int:test_id>')
@creator_only
def results(test_id):
    test = Test.query.filter_by(id=test_id).first()
    submits = sorted(test.submits, reverse=True,
                     key=lambda x: (x.score is not None, x.score))

    return render_template('results.html', test=test,
                           submits=submits)


"""
navigation
"""


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.filter_by(id=session['id']).first()
    tests = Test.query.filter_by(access=True).all()

    available = [x for x in tests
                 if not Submit.query.filter_by(test=x, taker=user).first()
                 and x.creator != user]

    if request.method == 'GET':
        return render_template('index.html', available=available)

    # creating new test
    name = request.form.get('name')

    if not name:
        return render_template('index.html', available=available,
                               error='Chybí jméno testu.')

    if Test.query.filter_by(name=name).first():
        return render_template('index.html', available=available,
                               error='Test s takovým jménem už existuje.')

    user.tests.append(Test(name=name))

    db.session.add(user)
    db.session.commit()

    return redirect('/tests')


@app.route('/tests')
@login_required
def tests():
    user = User.query.filter_by(id=session['id']).first()

    submits = Submit.query.filter_by(taker=user).all()

    incomplete = [x.test for x in submits if x.score is None]
    complete = [x.test for x in submits if x.score is not None]

    created = Test.query.filter_by(creator=user).all()

    return render_template('tests.html', incomplete=incomplete,
                           complete=complete, created=created)


"""
user accounts
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        return render_template('login.html', error='Chybí uživatelské jméno.')

    if not password:
        return render_template('login.html', error='Chybí heslo.')

    user = User.query.filter_by(username=username).first()

    if not user:
        return render_template('login.html', error='Uživatel neexistuje.')

    if not check_password_hash(user.password, password):
        return render_template('login.html', error='Špatné heslo.')

    session['id'] = user.id

    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')

    if not username:
        return render_template('register.html',
                               error='Chybí uživatelské jméno.')

    if not name:
        return render_template('register.html', error='Chybí jméno.')

    if not password:
        return render_template('register.html', error='Chybí heslo.')

    if not confirmation:
        return render_template('register.html', error='Chybí heslo podruhé.')

    if ' ' in username or ',' in username:
        return render_template('register.html',
                               error='Uživatelské jméno nesmí obsahovat\
                               čárky ani mezery.')

    if ',' in name:
        return render_template('register.html',
                               error='Jméno nesmí obsahovat čárky.')

    if User.query.filter_by(username=username).first():
        return render_template('register.html',
                               error='Takové uživatelské jméno už existuje.')

    if password != confirmation:
        return render_template('register.html',
                               error='Hesla nejsou stejná')

    user = User(username=username, name=name,
                password=generate_password_hash(password))

    db.session.add(user)
    db.session.commit()

    return redirect('/login')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(id=session['id']).first()

    if request.method == 'GET':
        return render_template('profile.html', user=user)

    # changing password
    old = request.form.get('old')
    new = request.form.get('new')
    confirmation = request.form.get('confirmation')

    if not old:
        return render_template('profile.html', user=user,
                               error='Chybí staré heslo.')

    if not new:
        return render_template('profile.html', user=user,
                               error='Chybí nové heslo.')

    if not confirmation:
        return render_template('profile.html', user=user,
                               error='Chybí nové heslo podruhé.')

    if not check_password_hash(user.password, old):
        return render_template('profile.html', user=user,
                               error='Špatné staré heslo.')

    if new != confirmation:
        return render_template('profile.html', user=user,
                               error='Nová hesla nejsou stejná')

    user.password = generate_password_hash(new)

    db.session.add(user)
    db.session.commit()

    return redirect('/')
