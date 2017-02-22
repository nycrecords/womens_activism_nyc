"""
feedback blueprint
Contains the routes for sending general feedback about the site to an admin
"""
from flask import Blueprint

feedback = Blueprint('feedback', __name__)

from app.feedback import views
