"""
post blueprint
contains all the routes for viewing/editing/deleting posts
"""
from flask import Blueprint

posts = Blueprint('posts', __name__)

from app.posts import views