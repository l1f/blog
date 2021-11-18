from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, current_user

from . import auth
from .forms import LoginForm

from ..models import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            red = request.args.get("next")
            if red is None or red.startswith("/"):
                red = url_for("blog.index")
            return redirect(red)
        flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)
