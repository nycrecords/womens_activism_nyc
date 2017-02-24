"""
View functions for story functionality
"""
from app.stories import stories
from flask import render_template
from app.models import Tags, Stories, Posters

@stories.route('/stories/<int:id>', methods=['GET', 'POST'])
def view_story(id):
    story = Stories.query.filter_by(id=id).one()

    if story.is_visible:
        if story.poster_id:
            poster = Posters.query.filter_by(id=story.poster_id).first()
        else:
            poster = None
        return render_template('stories/single_view_story.html', story=story, poster=poster)
    else:
        return render_template("error/generic.html", status_code=404)


@stories.route('/', methods=['GET'])
def catalog():
    return render_template(
        'stories/stories.html',
        tags=Tags.query.all()
    )
