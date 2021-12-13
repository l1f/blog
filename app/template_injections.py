from .data import role


def inject_permissions():
    return dict(permissions=role.Permission)
