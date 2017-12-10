from functools import wraps
from app import app

from flask import session, url_for, redirect, request

__author__ = 'lbvene'


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function

'''@requires_login
def my_function(x, y):
    print("Hello, world!")
    return x+y

# when this gets called, decorated_function()
#   is really in place for 'my_function()'
print(my_function(2, 4))
'''

def requires_admin_permissions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return decorated_function
