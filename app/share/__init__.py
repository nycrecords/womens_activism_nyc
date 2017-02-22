from flask import Blueprint

share = Blueprint('share', __name__)

from . import views
