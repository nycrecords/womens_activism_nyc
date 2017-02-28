from flask import render_template, redirect, url_for, flash, request

from app.models import Tags
from app.share import share
from app.share.forms import StoryForm
from app.share.utils import create_story, create_user


@share.route('/', methods=['GET', 'POST'])
def new():
    """
    View function for creating a story
    :return: If the story form was fully validated, create a Story and Poster object to store in the database
    """
    form = StoryForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.user_first.data or form.user_last.data or form.user_email.data:
                user_guid = create_user(user_first=form.user_first.data,
                                        user_last=form.user_last.data,
                                        user_email=form.user_email.data)
            else:
                user_guid = None

            tag_string = form.tags.data
            tags = []
            for t in tag_string.split(','):
                tags.append(Tags.query.filter_by(id=t).one().name)

            create_story(activist_first=form.activist_first.data,
                         activist_last=form.activist_last.data,
                         activist_start=form.activist_start.data,
                         activist_end=form.activist_end.data,
                         tags=tags,
                         content=form.content.data,
                         activist_url=form.activist_url.data,
                         image_url=form.image_url.data,
                         video_url=form.video_url.data,
                         user_guid=user_guid)
            flash('Story submitted!', category='share_submitted_story')
            return redirect(url_for('share.new'))
        else:
            flash('Error, please try again.', category="danger")
            return render_template('share/share.html', form=form, tags=Tags.query.all())
    return render_template('share/share.html', form=form, tags=Tags.query.all())
