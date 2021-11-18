import os
from getpass import getpass
from flask_migrate import Migrate

from app import create_app, db
import app.models as models

app = create_app(os.getenv("BLOG_CONFIG") or "default")
migrate = Migrate(app, db)


@app.cli.command()
def upgrade():
    models.Role.insert_roles()


@app.cli.command()
def create_super_user():
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    u = models.User(username=username, email=email, password=password, confirmed=True)
    db.session.add(u)
    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, models=models)
