from functools import wraps

from flask import abort, redirect, url_for
from flask_login import current_user

from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorator_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)


def redirect_if_logged_in():
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url_for("blog.index"))
            return f(*args, **kwargs)

        return decorator_function

    return decorator
