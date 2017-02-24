from . import share
from flask import render_template


@share.route('/', methods=['GET', 'POST'])
def new():
    return render_template('share/share.html')
