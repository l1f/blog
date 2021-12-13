from typing import List

from flask import current_app, render_template

from ..models import User
from ..tasks.mail import send_async_email


def new_email(recipients: List[str], template_name: str, subject: str, **kwargs):
    return {
        "recipients": recipients,
        "subject": f"{current_app.config['BLOG_MAIL_SUBJECT_PREFIX']} - {subject}",
        "body_html": render_template(f"{template_name}.html", **kwargs),
        "body_txt": render_template(f"{template_name}.html", **kwargs),
        "sender": current_app.config["BLOG_MAIL_SENDER"],
    }


def send_confirm_account_email(user: User):
    token = user.generate_confirm_token()
    email = new_email(
        recipients=[user.email],
        subject="Confirm Your Account",
        template_name="auth/email/confirm",
        user=user,
        token=token,
    )
    send_async_email.delay(email)


def send_reset_password_mail(user: User):
    token = user.generate_password_reset_token()
    email = new_email(
        recipients=[user.email],
        subject="Reset Your Password",
        template_name="auth/email/reset_password",
        user=user,
        token=token,
    )
    send_async_email.delay(email)


def send_new_email_confirm_mail(user: User, new_email_address: str):
    token = user.generate_email_change_token(new_email_address)
    email = new_email(
        recipients=[user.email],
        subject="Confirm your email address",
        template_name="auth/email/change_email",
        user=user,
        token=token,
    )
    send_async_email.delay(email)


def send_new_email_confirmed(user: User):
    email = new_email(
        recipients=[user.email],
        subject="New email address confirmed",
        template_name="auth/email/email_confirmed",
        user=user,
    )
    send_async_email.delay(email)
