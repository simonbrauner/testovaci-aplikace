from flask import session, redirect

from functools import wraps

from config import db
from model import Test


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

        db.session.delete(submit)

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
