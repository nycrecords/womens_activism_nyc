# TODO: Module level docstring
from flask import Blueprint

posts = Blueprint('posts', __name__)

from . import views