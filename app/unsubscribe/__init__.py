from flask import Blueprint

unsubscribe = Blueprint('unsubscribe', __name__)

from app.unsubscribe import views