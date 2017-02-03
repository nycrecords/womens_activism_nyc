from flask import render_template
from app.main import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')