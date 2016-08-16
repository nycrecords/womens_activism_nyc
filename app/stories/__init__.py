"""
post blueprint
contains all the routes for viewing/editing/deleting posts
"""
from flask import Blueprint

stories = Blueprint('stories', __name__)

from app.stories import views