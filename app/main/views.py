from . import main
from flask import render_template


@main.route('/', methods=['GET'])
def index():
    return render_template('main/home.html')


@main.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html')