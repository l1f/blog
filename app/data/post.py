from datetime import datetime

from .. import db


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
