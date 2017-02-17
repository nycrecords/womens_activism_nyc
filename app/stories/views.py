"""
View functions for story functionality
"""
from flask import render_template, redirect, url_for, flash, request
from app.stories.forms import StoryForm
from app.stories import stories
from app.stories.utils import create_story, create_poster, validate_years, validate_poster
from app.models import Stories, Posters


@stories.route('/share', methods=['GET', 'POST'])
def share():
    """
    View function for creating a story
    :return: If the story form was fully validated, create a Story and Poster object to store in the database
    """
    form = StoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            poster_id = None

            # # extra validator for activist's years because it can't be done through WTForms built in
            if not validate_years(form.activist_start.data,
                              form.activist_start_BC.data,
                              form.activist_end.data,
                              form.activist_end_BC.data):
                flash('Error, please try again.')
                return render_template('stories/share_a_story.html', form=form)

            if form.poster_first.data or form.poster_last.data or form.poster_email.data:
                # extra validator for poster information because it can't be done through WTForms built in
                if not validate_poster(form.poster_first.data, form.poster_last.data):
                    flash('Error, please try again.')
                    return render_template('stories/share_a_story.html', form=form)
            poster_id = create_poster(poster_first=form.poster_first.data,
                                      poster_last=form.poster_last.data,
                                      poster_email=form.poster_email.data)

            create_story(activist_first=form.activist_first.data,
                         activist_last=form.activist_last.data,
                         activist_start=form.activist_start.data,
                         activist_start_BC=form.activist_start_BC.data,
                         activist_end=form.activist_end.data,
                         activist_end_BC=form.activist_end_BC.data,
                         tags=form.tags.data,
                         content=form.content.data,
                         activist_url=form.activist_url.data,
                         image_url=form.image_url.data,
                         video_url=form.video_url.data,
                         poster_id=poster_id)
            flash('Story submitted!', category='share_submitted_story')
            return redirect(url_for('stories.share'))
        flash('Error, please try again.')
    return render_template('stories/share_a_story.html', form=form)


@stories.route('/stories/<int:id>', methods=['GET', 'POST'])
def stories(id):
    story = Stories.query.filter_by(id=id).one()

    if story.is_visible:
        if story.poster_id:
            poster = Posters.query.filter_by(id=story.poster_id).first()
        else:
            poster = None
        return render_template('stories/single_view_story.html', story=story, poster=poster)
    else:
        return render_template("error/generic.html", status_code=404)
