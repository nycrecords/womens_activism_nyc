from flask import render_template
from app.main import main


@main.route('/', methods=['GET'])
def index():
    return render_template('main/home.html')
