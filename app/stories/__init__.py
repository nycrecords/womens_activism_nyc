"""
stories blueprint
Contains the routes for creating a story, viewing an individual stories, viewing the stories catalog
"""
from flask import Blueprint

stories = Blueprint('stories', __name__)

from app.stories import views
