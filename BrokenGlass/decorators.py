from functools import wraps
from flask import session, redirect, url_for


def authenticated_resource(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if "id" in session:
            return function(*args, **kwargs)

        return redirect(url_for("login"))

    return decorated
