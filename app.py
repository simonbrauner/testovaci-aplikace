from flask import request, session
from flask import render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from json import loads

from config import app, db
from model import User, Test, Question, Answer
from tools import login_required, creator_only


@app.route('/settings/<int:test_id>')
@creator_only
def settings(test_id):
    test = Test.query.filter_by(id=test_id).first()
    questions = test.questions

    return render_template('settings.html', test=test,
                           questions=questions)


@app.route('/save_settings/<int:test_id>', methods=['POST'])
@creator_only
def save_settings(test_id):
    test = Test.query.filter_by(id=test_id).first()

    parts = request.form.get('parts')

    if parts:
        try:
            parts = int(parts)

            assert parts > 0
            assert parts <= len(test.questions)

            test.parts = parts
            db.session.add(test)

            db.session.commit()

        except ValueError:
            return redirect(f'/settings/{test_id}')

        except AssertionError:
            return redirect(f'/settings/{test_id}')

    return redirect('/')


@app.route('/save_test/<int:test_id>', methods=['POST'])
@creator_only
def save_test(test_id):
    test = Test.query.filter_by(id=test_id).first()

    # deleting old
    for question in test.questions:
        for answer in question.answers:
            db.session.delete(answer)

        db.session.delete(question)

    db.session.commit()

    # adding new
    test_json = request.form.get('test-json')
    test_dict = loads(test_json)

    for question_dict in test_dict['questions']:
        question = Question(name=question_dict['title'])

        for answer_dict in question_dict['answers']:
            question.answers.append(Answer(name=answer_dict['title'],
                                           correct=answer_dict['correct']))

        test.questions.append(question)

    db.session.add(test)

    db.session.commit()

    return redirect('/')


@app.route('/editor/<int:test_id>')
@creator_only
def editor(test_id):
    test = Test.query.filter_by(id=test_id).first()

    return render_template('editor.html', test=test)


@app.route('/new_test', methods=['POST'])
@login_required
def new_test():
    user = User.query.filter_by(id=session['id']).first()
    name = request.form.get('name')

    user.tests.append(Test(name=name))
    db.session.add(user)

    db.session.commit()

    return redirect('/')


@app.route('/')
@login_required
def index():
    tests = Test.query.all()
    return render_template('index.html', tests=tests)


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=session['id']).first()
    return render_template('profile.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return render_template('login.html', error='uzivatel neexistuje')

    if not check_password_hash(user.password, password):
        return render_template('login.html', error='spatne heslo')

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

    if len(username) > 128:
        return render_template('register.html',
                               error='uzivatelske jmeno je moc dlouhe')

    if len(name) > 128:
        return render_template('register.html',
                               error='jmeno je moc dlouhe')

    if len(password) > 128:
        return render_template('register.html',
                               error='heslo je moc dlouhe')

    if User.query.filter_by(username=username).first():
        return render_template('register.html',
                               error='takove uzivatelske jmeno uz existuje')

    if password != confirmation:
        return render_template('register.html',
                               error='hesla nejsou stejna')

    user = User(username=username, name=name,
                password=generate_password_hash(password))

    db.session.add(user)
    db.session.commit()

    return redirect('/login')
