from typing import List
from dataclasses import dataclass
from flask import current_app, render_template

from ..models import User
from ..tasks.mail import send_async_email


@dataclass
class Email:
    recipients: List[str]
    body_html: str
    body_txt: str
    subject: str
    sender: str


def new_email(recipients: List[str], template_name: str, subject: str, **kwargs):
    return {
        "recipients": recipients,
        "subject": f"{current_app.config['BLOG_MAIL_SUBJECT_PREFIX']} - {subject}",
        "body_html": render_template(f"{template_name}.html", **kwargs),
        "body_txt": render_template(f"{template_name}.html", **kwargs),
        "sender": current_app.config["BLOG_MAIL_SENDER"]
    }


def send_confirm_account_email(user: User):
    print("Send confirm mail")
    token = user.generate_confirm_token()
    print("Generate Token")
    email = new_email(
        recipients=[user.email],
        subject=f"{current_app.config['BLOG_MAIL_SUBJECT_PREFIX']} - Confirm Your Account",
        template_name="auth/email/confirm",
        user=user,
        token=token
    )
    print(email)
    send_async_email.delay(email)
