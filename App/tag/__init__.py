from flask import Blueprint, app, render_template

tags = Blueprint('tags', __name__)

from . import views