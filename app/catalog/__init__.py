from flask import Blueprint

catalog = Blueprint('catalog', __name__)

from . import views
