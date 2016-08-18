"""
tags blueprint
contains all the
"""
from flask import Blueprint

tags = Blueprint('tags', __name__)

from . import views

# TODO: DOCSTRINGS
