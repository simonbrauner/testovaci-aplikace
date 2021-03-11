from flask import request, session
from flask import render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from tools import create_app, login_required
from model import User

app = create_app()

db = SQLAlchemy(app)


@app.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/profile')
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
