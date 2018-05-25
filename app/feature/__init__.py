from flask import Blueprint

feature = Blueprint('feature', __name__)

from . import views
