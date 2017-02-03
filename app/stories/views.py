from flask import render_template, redirect, url_for, flash, request
from app.stories.forms import StoryForm, MyForm
from app.stories import stories
from app.stories.utils import create_story, create_poster


@stories.route('/share', methods=['GET', 'POST'])
def index():
    form = StoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            poster_id = None

            if form.poster_first.data or form.poster_last.data or form.poster_email.data:
                poster_id = create_poster(poster_first=form.poster_first.data,
                                          poster_last=form.poster_last.data,
                                          poster_email=form.poster_email.data)

            create_story(activist_first=form.activist_first.data,
                         activist_last=form.activist_last.data,
                         activist_start=form.activist_start.data,
                         activist_start_BC=form.activist_start_BC.data,
                         activist_end=form.activist_end.data,
                         activist_end_BC=form.activist_start_BC.data,
                         tags=form.tags.data,
                         content=form.content.data,
                         activist_url=form.activist_url.data,
                         image_url=form.image_url.data,
                         video_url=form.video_url.data,
                         poster_id=poster_id)
            return redirect(url_for('.index'))
        flash('Error, please try again.')
    return render_template('stories/share_a_story.html', form=form)