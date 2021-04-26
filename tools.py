"""
Testovací aplikace
Šimon Brauner
26.4.2021

tools.py

Helpful functions used in app.py.
"""


from flask import session, redirect

from functools import wraps
from random import choices
from string import ascii_letters as letters, digits

from config import db
from model import Test


def create_test_link():
    return ''.join(choices(letters + digits, k=40))


def clear_test(test):
    for question in test.questions:
        for answer in question.answers:
            db.session.delete(answer)

        db.session.delete(question)

    db.session.commit()


def delete_test(test):
    for submit in test.submits:
        for response in submit.responses:
            db.session.delete(response)

        taker = submit.taker

        db.session.delete(submit)

        # deleting anonymous accounts
        if not taker.username:
            db.session.delete(taker)

    clear_test(test)

    db.session.delete(test)

    db.session.commit()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function


def creator_only(f):
    @wraps(f)
    @login_required
    def decorated_function(test_id, *args, **kwargs):
        test = Test.query.filter_by(id=test_id).first()

        if not test or session['id'] != test.creator_id:
            return redirect('/')
        return f(test_id, *args, **kwargs)

    return decorated_function
