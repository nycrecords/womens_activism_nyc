"""
stories blueprint
contains routes for viewing a page of stories, single story, edit and delete story
"""
from flask import Blueprint

stories = Blueprint('stories', __name__)

from app.stories import views