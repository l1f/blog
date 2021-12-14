from flask import jsonify

from ..data import Permission, User
from ..decorators import permission_required
from . import api


@api.route("/users")
@permission_required(Permission.ADMIN)
def user_index():
    users = User.query.order_by(User.id).all()
    return jsonify(users)


@api.route("/users/<user_id>")
@permission_required(Permission.ADMIN)
def user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.to_dict())


@api.route("/users/<id>", methods=["DELETE"])
@permission_required(Permission.ADMIN)
def confirm_user_delete(id):
    pass


@api.route("/users/<id>", methods=["DELETE"])
@permission_required(Permission.ADMIN)
def delete_user_by_id(id):
    return jsonify("cms/index.html")
