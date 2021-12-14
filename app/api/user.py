from flask import jsonify

from ..data import Permission, User
from ..decorators import permission_required
from ..exstensions import db
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


@api.route("/users/<user_id>", methods=["DELETE"])
@permission_required(Permission.ADMIN)
def delete_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify("", 204)
