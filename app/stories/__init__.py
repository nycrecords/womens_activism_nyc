"""
stories blueprint
Contains the routes for creating a single story, viewing a feed of stories, as well as editing and deleting a story
"""
from flask import Blueprint

stories = Blueprint('stories', __name__)

from app.stories import views