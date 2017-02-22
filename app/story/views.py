from . import story
from flask import render_template


@story.route('/', methods=['GET', 'POST'])
def share():
    return render_template('story/share.html')

@story.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('story/view.html')