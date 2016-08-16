"""
stories blueprint
contains all the routes for viewing/editing/deleting stories
"""
from flask import Blueprint

stories = Blueprint('stories', __name__)

from app.stories import views