"""
Flags blueprint
Contains the routes for flagging a specific post/comment
"""
from flask import Blueprint

flags = Blueprint('flags', __name__)

from . import views
