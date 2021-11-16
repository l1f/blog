import os
from flask_migrate import Migrate

from app import create_app, db

# from app.models import User, Role

app = create_app(os.getenv("BLOG_CONFIG") or "default")
migrate = Migrate(app, db)
