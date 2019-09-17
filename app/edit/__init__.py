from flask import Blueprint

edit = Blueprint("edit", __name__)

from . import views
