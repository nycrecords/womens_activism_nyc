from . import story
from flask import render_template


@story.route('/', methods=['GET', 'POST'])
def share():
    return render_template('story/share.html')

@story.route('/catalog', methods=['GET', 'POST'])
def catalog():
    return render_template('story/catalog.html')