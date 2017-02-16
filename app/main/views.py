from . import main
from flask import render_template


@main.route('/', methods=['GET'])
def index():
    return render_template('main/home.html')
