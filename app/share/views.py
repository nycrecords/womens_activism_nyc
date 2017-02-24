from flask import render_template, redirect, url_for, flash, request
from app.share import share
from app.share.forms import StoryForm
from app.share.utils import create_story, create_poster, validate_years, validate_poster


@share.route('/', methods=['GET', 'POST'])
def new():
    """
    View function for creating a story
    :return: If the story form was fully validated, create a Story and Poster object to store in the database
    """
    form = StoryForm()
    story = {
        "activist_first": form.activist_first.data,
        "activist_last": form.activist_last.data,
        "activist_start": form.activist_start.data,
        "activist_end": form.activist_end.data,
        "content": form.content.data,
        "activist_url": form.activist_url.data,
        "image_url": form.image_url.data,
        "video_url": form.video_url.data,
        "poster_first": form.poster_first.data,
        "poster_last": form.poster_first.data,
        "poster_email": form.poster_email.data
    }
    if request.method == 'POST':
        tag_string = form.tags.data
        tags = tag_string.split(';')

        if form.validate_on_submit():
            # extra validator for activist's years because it can't be done through WTForms built in
            if not validate_years(form.activist_start.data,
                              form.activist_start_BC.data,
                              form.activist_end.data,
                              form.activist_end_BC.data):
                flash('Error, please try again.')
                return render_template('stories/share_a_story.html', form=form, story=story)

            if form.poster_first.data or form.poster_last.data or form.poster_email.data:
                # extra validator for poster information because it can't be done through WTForms built in
                if not validate_poster(form.poster_first.data, form.poster_last.data):
                    flash('Error, please try again.')
                    return render_template('stories/share_a_story.html', form=form, story=story)
                poster_id = create_poster(poster_first=form.poster_first.data,
                                          poster_last=form.poster_last.data,
                                          poster_email=form.poster_email.data)
            else:
                poster_id = None

            create_story(activist_first=form.activist_first.data,
                         activist_last=form.activist_last.data,
                         activist_start=form.activist_start.data,
                         activist_start_BC=form.activist_start_BC.data,
                         activist_end=form.activist_end.data,
                         activist_end_BC=form.activist_end_BC.data,
                         tags=tags,
                         content=form.content.data,
                         activist_url=form.activist_url.data,
                         image_url=form.image_url.data,
                         video_url=form.video_url.data,
                         poster_id=poster_id)
            flash('Story submitted!', category='share_submitted_story')
            return redirect(url_for('share.new'))
        flash('Error, please try again.')
    return render_template('share/share.html', form=form, story=story)