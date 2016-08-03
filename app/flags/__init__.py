# TODO: Module level docstring
from flask import Blueprint

flags = Blueprint('flags', __name__)

from . import views