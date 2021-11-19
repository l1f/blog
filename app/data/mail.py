from .. import db


class MailType:
    REGISTER = 1


class Mail(db.Model):
    __tablename__ = "mails"
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(64))
    type = db.Column(db.Integer)
