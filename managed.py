import os
from flask_migrate import Migrate

from app import create_app, db
import app.models as models

app = create_app(os.getenv("BLOG_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, models=models)
