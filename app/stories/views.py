from . import stories
from flask import render_template

from app.models import Tags


@stories.route('/', methods=['GET'])
def catalog():
    return render_template(
        'stories/stories.html',
        tags=Tags.query.all()
    )
