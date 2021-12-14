from flask import render_template
from flask_login import login_required

from ..data import Permission, User
from ..decorators import permission_required
from . import cms


@cms.route("/users")
@permission_required(Permission.ADMIN)
def user_index():
    users = User.query.order_by(User.id).all()
    return render_template("cms/users/index.html", users=users)


@cms.route("/users/<id>", methods=["DELETE"])
@permission_required(Permission.ADMIN)
def user_by_id(id):
    return render_template("cms/index.html")


@cms.route("/users/<id>", methods=["DELETE"])
@permission_required(Permission.ADMIN)
def delete_user_by_id(id):
    return render_template("cms/index.html")
