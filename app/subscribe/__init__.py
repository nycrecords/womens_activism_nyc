"""
stories blueprint
Contains the routes for creating a story, viewing an individual stories, viewing the stories catalog
"""
from flask import Blueprint

subscribe = Blueprint("subscribe", __name__)

from app.subscribe import views
