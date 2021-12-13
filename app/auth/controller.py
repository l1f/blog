from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..app import db
from ..common import (
    send_confirm_account_email,
    send_new_email_confirm_mail,
    send_new_email_confirmed,
    send_reset_password_mail,
)
from ..decorators import redirect_if_logged_in
from ..models import User
from . import auth
from .forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    LoginForm,
    PasswordResetForm,
    PasswordResetRequestForm,
    RegistrationForm,
)


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
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
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


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been updated.")
            return redirect(url_for("blog.index"))
        else:
            flash("Invalid password.")
    return render_template("auth/change_password.html", form=form)


@auth.route("/reset", methods=["GET", "POST"])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for("blog.index"))

    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            send_reset_password_mail(user)
        flash("An email with instructions to reset your password has been sent to you.")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password_request.html", form=form)


@auth.route("/reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for("blog.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("Your password has been updated.")
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("blog.index"))
    return render_template("auth/reset_password.html", form=form, token=token)


@auth.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            send_new_email_confirm_mail(current_user, new_email)
            flash(
                "An email with instructions to confirm your new email address has been sent to you."
            )
            return redirect(url_for("blog.index"))
        flash("Invalid email or password")
    return render_template("auth/change_email_address.html", form=form)


@auth.route("/change_email/<token>")
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        send_new_email_confirmed(current_user)
        flash("Your email address has been updated.")
    else:
        flash("Invalid request.")

    return redirect(url_for("blog.index"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("blog.index"))


@auth.route("/self")
@login_required
def self():
    return render_template("auth/self.html", user=current_user)
