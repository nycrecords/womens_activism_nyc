"""
View functions for story functionality
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from app.constants.event import EDIT_FEATURED_STORY
from app.db_utils import create_object, update_object
from app.feature import feature
from app.feature.forms import FeaturedStoryForm, ModifyFeatureForm, RankFeatureForm
from app.feature.utils import create_featured_story, update_featured_story, hide_current_featured_story
from app.models import Events, FeaturedStories, Stories


@feature.route('/', methods=['GET'])
@login_required
def listing():
    """
    View function for the feature page. The feature page contains all the featured stories.
    This function queries the database for all the featured stories.

    :return: renders the 'feature.html' template with featured story list
    """
    featured_stories = FeaturedStories.query.filter_by().all()

    return render_template('feature/feature.html', featured_stories=featured_stories)


@feature.route('/<story_id>', methods=['GET', 'POST'])
@login_required
def set_featured_story(story_id):
    """
    View function for adding a story to featured stories.
    This function provides an interface for stories that are being featured for the first time.
    In POST request, if all the fields are validated, then it will redirect user to the home page

    :return: first time register a story to featured story renders 'add.html'
                if inputs are validated, redirect to main page 'main.index'
    """
    add_featured_form = FeaturedStoryForm(request.form)
    story = Stories.query.filter_by(id=story_id).one_or_none()

    if request.method == 'POST':
        if add_featured_form.validate_on_submit():
            new_quote = add_featured_form.quote.data.strip("\"")
            create_featured_story(story=story,
                                  left_right=add_featured_form.left_right.data,
                                  quote=new_quote)
            flash("Story is now Featured!", category='success')
            return redirect(url_for('main.index'))
        else:
            for field, error in add_featured_form.errors.items():
                flash(add_featured_form.errors[field][0], category='danger')
            return render_template('feature/add.html', form=add_featured_form, story=story)

    else:
        featured_story = FeaturedStories.query.filter_by(story_id=story_id).one_or_none()
        if featured_story is not None:
            hide_current_featured_story()
            update_object({"is_visible": True}, FeaturedStories, featured_story.id)
            create_object(Events(
                _type=EDIT_FEATURED_STORY,
                story_id=featured_story.story_id,
                user_guid=current_user.guid,
                previous_value={"is_visible": False},
                new_value={"is_visible": True}
            ))
            flash("Story is now Featured!", category='success')
            return redirect(url_for('main.index'))
        return render_template('feature/add.html', form=add_featured_form)


@feature.route('/modify/<story_id>', methods=['GET', 'POST'])
@login_required
def modify(story_id):
    """
    This view function is used for modifying/editing the featured story.
    Modifying attributes such as left/right image location, visibility, and quote.

    :param story_id: the story_id you would like to modify. this story_id must be in FeaturedStories table
    :return: renders 'modify.html' that contains the form for modifying existing featured story
                if all the form inputs are validated, it redirects users to the main page 'main.index'
    """
    featured_story = FeaturedStories.query.filter_by(story_id=story_id).one_or_none()
    form = ModifyFeatureForm(request.form, left_right=featured_story.left_right, quote=featured_story.quote,
                             is_visible=featured_story.is_visible)
    story = Stories.query.filter_by(id=story_id).one_or_none()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_quote = form.quote.data.strip("\"")
            update_featured_story(featured_story=featured_story,
                                  left_right=form.left_right.data,
                                  quote=new_quote,
                                  is_visible=form.is_visible.data)
            flash("Story is now Modified!", category='success')
            return redirect(url_for('main.index'))

    else:
        if featured_story is None:
            flash("This story does not exist in Featured Story", category='danger')
            return redirect(url_for('feature.listing'))
    return render_template('feature/modify.html', story=story, form=form)
