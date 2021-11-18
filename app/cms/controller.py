from flask import render_template
from flask_login import login_user, current_user, login_required

from ..decorators import permission_required
from ..models import Permission
from . import cms


@cms.route("/")
def index():
    return render_template("cms/index.html")


@cms.before_request
@login_required
@permission_required(Permission.WRITE)
def before_request():
    """
    It should only be determined whether the current user is logged in
    and has the appropriate authorization to access the backend.
    """
    pass
