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

        video_url = story.video_url

        # format the video link for the frontend
        if story.video_url:
            video_url = story.video_url
            if "youtube.com/watch?v=" in video_url:  # if the link is a youtube link convert it to an embed
                split = video_url.split("watch?v=", 1)
                video_url = "https://www.youtube.com/embed/{}".format(split[1])
                story.video_url = video_url
            elif "youtu.be/" in video_url:  # if the link is a short youtube link convert it to an embed
                split = video_url.split("youtu.be/", 1)
                video_url = "https://www.youtube.com/embed/{}".format(split[1])
                story.video_url = video_url
            elif "vimeo" in video_url:  # if the link is a vimeo link convert it to an embed
                split = video_url.split("vimeo.com/", 1)
                video_url = "https://player.vimeo.com/video/{}".format(split[1])
                story.video_url = video_url
        return render_template('stories/view.html', story=story, poster=poster)
    else:
        return render_template("error/generic.html", status_code=404)


@stories.route('/', methods=['GET'])
def catalog():
    return render_template(
        'stories/stories.html',
        tags=Tags.query.all()
    )
