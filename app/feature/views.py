"""
View functions for story functionality
"""
from app.feature import feature
from app.feature.forms import FeaturedStoryForm, ModifyFeatureForm, RankFeatureForm
from app.feature.utils import create_featuredstory, update_featuredstory
from flask import render_template, request, flash, redirect, url_for
from app.models import Stories, FeaturedStories
from flask_login import login_required
from sqlalchemy import func


@feature.route('/', methods=['GET'])
@login_required
def listing():
    """
    View function for the feature page. The feature page contains all the featured stories.
    This function queries the database for all the featured stories.

    :return: renders the 'feature.html' template with featured story list
    """
    story_list = []
    featuredstory = FeaturedStories.query.filter_by().all()

    # for each featured story in all featured stories
    for each in featuredstory:
        story = Stories.query.filter_by(id=each.story_id).one()
        story_list.append((story, each))

    return render_template('feature/feature.html', story_list=story_list)


@feature.route('/rank', methods=['GET'])
@login_required
def rank():
    """
    View function for modifying the display of the Featured Stories in home page.
    This function allows user to change the ranking of the Feature Stories

    :return: renders the 'rank.html' template with the current ranking
    """
    form = RankFeatureForm(request.form)
    # NEED TO WORK ON THIS POST REQUEST. THE BUTTON DOES NOT WORK AT THE MOMENT
    # THE BUTTON FAILS
    if request.method == 'POST':
        print("hello")
        if request.form['submit'] == "Rerank this Featured Story":
            flash("Reranked Featured Stories!", category='success')
            return redirect(url_for('stories.catalog'))
        else:
            return redirect(url_for('main.index'))

    story_list = []
    featuredstory = FeaturedStories.query.filter_by(is_visible=True).order_by(FeaturedStories.rank.asc()).all()
    # for each featured story in all featured stories
    rank = 1
    for each in featuredstory:
        story = Stories.query.filter_by(id=each.story_id).one()
        update_featuredstory(story=story, rank=rank)
        rank = rank + 1
        story_list.append((story, each))

    return render_template('feature/rank.html', story_list=story_list, form=form)

@feature.route('/<story_id>', methods=['GET', 'POST'])
@login_required
def add(story_id):
    """
    View function for adding a story to featured stories.
    This function provides an interface for stories that are being featured for the first time.
    In POST request, if all the fields are validated, then it will redirect user to the home page

    :return: first time register a story to featured story renders 'add.html'
                if inputs are validated, redirect to main page 'main.index'
    """
    addFeatureForm = FeaturedStoryForm(request.form)
    story = Stories.query.filter_by(id=story_id).one_or_none()
    if request.method == 'POST':
        if addFeatureForm.validate_on_submit():
            new_quote = addFeatureForm.quote.data.strip("\"")
            create_featuredstory(story=story,
                                 left_right=addFeatureForm.left_right.data,
                                 quote=new_quote)
            flash("Story is now Featured!", category='success')
            return redirect(url_for('main.index'))
        else:
            for field, error in addFeatureForm.errors.items():
                flash(addFeatureForm.errors[field][0], category='danger')
            return render_template('feature/add.html', form=addFeatureForm, story=story)

    feature = FeaturedStories.query.filter_by(story_id=story_id).one_or_none()
    if feature is not None:
        update_featuredstory(story=story, is_visible=True)
        flash("Story is now Featured!", category='success')
        return redirect(url_for('main.index'))
    return render_template('feature/add.html', form=addFeatureForm)


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

    featurestory = FeaturedStories.query.filter_by(story_id=story_id).one_or_none()
    if featurestory is None:
        flash("This story does not exist in Featured Story", category='danger')
        redirect(url_for('main.index'))
    form = ModifyFeatureForm(request.form, left_right=featurestory.left_right, quote=featurestory.quote,
                             is_visible=featurestory.is_visible)
    story = Stories.query.filter_by(id=story_id).one_or_none()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_quote = form.quote.data.strip("\"")
            update_featuredstory(story=story, left_right=form.left_right.data, quote=new_quote,
                                 is_visible=form.is_visible.data, rank=featurestory.rank)
            flash("Story is now Modified!", category='success')
            return redirect(url_for('main.index'))

    return render_template('feature/modify.html', story=story, form=form)
