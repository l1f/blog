from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import exc
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .role import Role, Permission
from ..app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is not None:
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permission: int) -> bool:
        return self.role is not None and self.role.has_permission(permission)

    def is_administrator(self) -> bool:
        return self.can(Permission.ADMIN)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_confirm_token(self, expiration=3600) -> str:
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps(("confirm", self.id)).decode("UTF-8")

    def confirm(self, token) -> bool:
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("UTF-8"))
        except exc.BadData:
            return False

        if data.get("confirm") != self.id:
            return False

        self.confirmed = True
        db.session(self)
        return True

    def generate_password_reset_token(self, expiration: int = 3600) -> str:
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token: str, new_password: str) -> bool:
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("UTF-8"))
        except exc.BadData:
            return False

        user = User.query.get(data.get("reset"))
        if user is None:
            return False

        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email: str, expiration: int = 3600) -> str:
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"change_email": self.id, "new_email": new_email}).decode("UTF-8")

    def change_email(self, token: str) -> bool:
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("UTF-8"))
        except exc.BadData:
            return False

        new_email = data.get("new_email")
        if new_email is None:
            return False

        if self.query.filter_by(email=new_email).first() is not None:
            return False

        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return f"<User {self.username}>"


class AnonymousUser(AnonymousUserMixin):
    @staticmethod
    def can(permissions):
        return False

    @staticmethod
    def is_administrator():
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
