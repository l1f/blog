from flask import current_app, render_template
from flask_mail import Message
from ..exstensions import mail, celery


@celery.task
def send_async_email(msg: Message):
    mail.send(msg)


def send_email(to: str, subject: str, template: str, **kwargs):
    app = current_app._get_current_object()
    msg = Message(f"{app.config['FLASKY_MAIL_SUBJECT_PREFIX']}{subject}",
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(f"{template}.txt", **kwargs)
    msg.html = render_template(f"{template}.html", **kwargs)
    send_async_email.delay(msg)
