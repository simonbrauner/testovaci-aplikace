from flask import session, redirect

from functools import wraps

from model import Test


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
        if session['id'] != test.creator_id:
            return redirect('/')
        return f(test_id, *args, **kwargs)
    return decorated_function
