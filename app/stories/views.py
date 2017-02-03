from flask import render_template, redirect, url_for, flash
from .forms import StoryForm
from app.stories import stories
from app.models import Stories


@stories.route('/share', methods=['GET', 'POST'])
def index():
    form = StoryForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('stories/share_a_story.html', form=form)