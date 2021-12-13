from flask_mail import Message

from ..exstensions import celery, mail


@celery.task
def send_async_email(email_data):
    message = Message(
        recipients=email_data["recipients"],
        subject=email_data["subject"],
        body=email_data["body_txt"],
        html=email_data["body_html"],
        sender=email_data["sender"],
    )
    mail.send(message)
