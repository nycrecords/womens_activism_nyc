"""
main blueprint
Contains the routes for the homepage where you can submit a post and viewing the most recents
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import views