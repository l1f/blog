from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, current_user, login_required

from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm

from ..decorators import redirect_if_logged_in
from ..app import db
from ..models import User
from ..common import send_confirm_account_email


@auth.route("/login", methods=["GET", "POST"])
@redirect_if_logged_in()
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_page = request.args.get("next")
            if next_page is None or not next_page.startswith("/"):
                next_page = url_for("blog.index")
            return redirect(next_page)
        flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
@redirect_if_logged_in()
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        send_confirm_account_email(user)
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for(".unconfirmed"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>", methods=["GET", "POST"])
@login_required
def confirm_account(token: str):
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account.")
    else:
        flash("The confirmation link is invalid or has expired")
    return redirect(url_for("blog.index"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    send_confirm_account_email(current_user)
    flash("A new confirmation email has been sent to you by email.")
    return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("blog.index"))
    return render_template("auth/unconfirmed.html")


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('blog.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.before_request
def before_request():
    if current_user.is_authenticated and request.blueprint != "auth" and request.endpoint != "static":
        return redirect(url_for("auth.unconfirmed"))
