from flask import Blueprint

story = Blueprint('story', __name__)

from app.story import views
