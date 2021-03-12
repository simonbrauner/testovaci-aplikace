from flask import session, redirect

from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function():
        if 'id' not in session:
            return redirect('/login')
        return f()
    return decorated_function
