from . import home
from flask import current_app


@home.route("")
def index():
    return ""
