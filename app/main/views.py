from flask import render_template
from app.main import main


@main.route('/', methods=['GET'])
def index():
    return render_template('main/home.html')


@main.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html')

@main.route('/contact', methods=['GET'])
def contact():
    return render_template('main/contact.html')