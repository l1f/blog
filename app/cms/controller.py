from flask import render_template

from . import cms


@cms.route("/")
def index():
    return "none"
