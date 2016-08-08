"""
auth blueprint
Contains routes for all User registration and authentication
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views