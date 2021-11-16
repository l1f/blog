from .. import db


class Permission:
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    # with lazy=dynamic the implicit query to query all users for a role, is not
    # automatically executed.
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.COMMENT],
            'Moderate': [Permission.COMMENT, Permission.MODERATE],
            'Writer': [Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }

        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def has_permission(self, permission: int) -> bool:
        return self.permissions & permission == permission

    def add_permission(self, permission: int):
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission: int):
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        self.permissions = 0

    def __repr__(self):
        return f"<Role {self.name}>"
