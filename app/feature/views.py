"""
View functions for story functionality
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from operator import attrgetter

from app.constants.event import EDIT_FEATURED_STORY
from app.db_utils import create_object, update_object
from app.feature import feature
from app.feature.forms import FeaturedStoryForm, ModifyFeatureForm
from app.feature.utils import create_featured_story, update_featured_story
from app.models import Events, FeaturedStories, Stories


@feature.route('/', methods=['GET'])
@login_required
def listing():
    """
    View function for the feature page. The feature page contains all the featured stories.
    This function queries the database for all the featured stories.

    :return: renders the 'feature.html' template with featured story list
    """
    featured_stories = sorted(FeaturedStories.query.filter_by(is_visible=True).all(), key=attrgetter('rank'))
    hidden_stories = FeaturedStories.query.filter_by(is_visible=False).all()

    return render_template('feature/feature.html', featured_stories=featured_stories, hidden_stories=hidden_stories)


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
    visible_stories = len(FeaturedStories.query.filter_by(is_visible=True).all())
    rank_choices = [(n, n + 1) for n in range(visible_stories)]
    if visible_stories < 4:
        rank_choices.append((visible_stories, visible_stories + 1))

    add_featured_form = FeaturedStoryForm(request.form)
    add_featured_form.rank.choices = rank_choices

    if request.method == 'POST':
        story = Stories.query.filter_by(id=story_id).one_or_none()
        if add_featured_form.validate_on_submit():
            if visible_stories == 4:
                flash("There cannot be more than 4 items on the carousel", category='danger')
                return redirect('feature/' + story_id)
            new_description = add_featured_form.description.data
            create_featured_story(story=story,
                                  left_right=add_featured_form.left_right.data,
                                  title=add_featured_form.title.data,
                                  description=new_description,
                                  rank=add_featured_form.rank.data)
            flash("Story is now Featured!", category='success')
            return redirect(url_for('main.index'))
        else:
            for field, error in add_featured_form.errors.items():
                flash(add_featured_form.errors[field][0], category='danger')
            return render_template('feature/add.html', form=add_featured_form, story=story)

    else:
        # Feature a story that has been featured before
        featured_story = FeaturedStories.query.filter_by(story_id=story_id).one_or_none()
        if featured_story is not None:
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
    Modifying attributes such as left/right image location, visibility, and description.

    :param story_id: the story_id you would like to modify. this story_id must be in FeaturedStories table
    :return: renders 'modify.html' that contains the form for modifying existing featured story
                if all the form inputs are validated, it redirects users to the main page 'main.index'
    """
    featured_story = FeaturedStories.query.filter_by(story_id=story_id).one_or_none()
    visible_stories = len(FeaturedStories.query.filter_by(is_visible=True).all())

    rank_choices = [(n, n + 1) for n in range(visible_stories)]
    default_rank = featured_story.rank
    if not featured_story.is_visible and visible_stories < 4:
        rank_choices.append((visible_stories, visible_stories + 1))
        default_rank = visible_stories

    form = ModifyFeatureForm(request.form,
                             left_right=featured_story.left_right,
                             title=featured_story.title,
                             description=featured_story.description,
                             is_visible=featured_story.is_visible,
                             rank=default_rank)
    form.rank.choices = rank_choices

    if request.method == 'POST':
        if form.validate_on_submit():
            if visible_stories > 4 and featured_story.is_visible and form.is_visible.data == 'True':
                # if not featured_story.is_visible and form.is_visible:
                flash("There cannot be more than 4 items on the carousel", category='danger')
                return redirect('feature/modify/' + story_id)
            update_featured_story(featured_story=featured_story,
                                  left_right=form.left_right.data,
                                  title=form.title.data,
                                  is_visible=form.is_visible.data,
                                  description=form.description.data,
                                  rank=form.rank.data)
            flash("Featured Story has been Modified!", category='success')
            return redirect(url_for('main.index'))
    else:
        if featured_story is None:
            flash("This story does not exist in Featured Story", category='danger')
            return redirect(url_for('feature.listing'))

    return render_template('feature/modify.html', form=form)
