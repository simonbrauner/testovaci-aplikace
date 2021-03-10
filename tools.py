from flask import Flask, session, redirect


def create_app():
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with open('secret_key.txt', 'r') as file:
        app.secret_key = file.read()

    return app


def login_required(f):
    def decorated_function():
        if 'id' not in session:
            return redirect('/login')
        return f()
    return decorated_function
