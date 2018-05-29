"""
Utility functions used for view functions involving featured stories
"""
from flask_login import current_user

from app.constants.event import ADD_FEATURED_STORY, HIDE_FEATURED_STORY, EDIT_FEATURED_STORY
from app.db_utils import update_object, create_object
from app.models import Events, FeaturedStories


def create_featured_story(story, left_right, quote):
    """
    A utility function to create a featured story.
    :param story: the story object you would like to create in Featured Story
    :param left_right: left or right side where the image will go
    :param quote: a famous quote that was once said by this activist
    :return: None
    """
    #
    current_featured_story = FeaturedStories.query.filter_by(is_visible=True).one_or_none()
    if current_featured_story is not None:
        update_object({"is_visible": False}, FeaturedStories, current_featured_story.id)

    featured_story = FeaturedStories(
        story_id=story.id,
        left_right=True if left_right == 'left' else False,
        is_visible=True,
        quote=quote,
    )

    create_object(featured_story)

    create_object(Events(
        story_id=story.id,
        user_guid=story.user_guid,
        _type=ADD_FEATURED_STORY,
        new_value=featured_story.val_for_events
    ))


def update_featured_story(featured_story, left_right, is_visible, quote):
    """
    A utility function to update a featured story.
    Updating attributes such as the following:
    :param featured_story:
    :param left_right: left or right side where the image will go
    :param is_visible: the visibility of the featured story
    :param quote: a famous quote that was once said by this activist

    :return: None
    """
    featured_story_fields = {
        "left_right",
        "is_visible",
        "quote"
    }

    featured_story_field_vals = {
        "left_right": left_right,
        "is_visible": is_visible,
        "quote": quote
    }

    old = {}
    new = {}

    for field in featured_story_fields:
        val = featured_story_field_vals[field]
        if val is not None:
            if val == '':
                featured_story_field_vals[field] = None  # null in db, not empty string
            cur_val = getattr(featured_story, field)
            new_val = featured_story_field_vals[field]
            if cur_val != new_val:
                old[field] = cur_val
                new[field] = new_val

    if new:
        if new.get('is_visible'):
            hide_current_featured_story()

        update_object(new, FeaturedStories, featured_story.id)

        create_object(Events(
            _type=EDIT_FEATURED_STORY,
            story_id=featured_story.story_id,
            user_guid=current_user.guid,
            previous_value=old,
            new_value=new
        ))


def hide_current_featured_story():
    """
    A utility function to hide the currently visible featured story (main page).
    Hiding does not *delete* the record from the table, but rather makes it invisible.

    :return: None
    """
    current_featured_story = FeaturedStories.query.filter_by(is_visible=True).one_or_none()
    if current_featured_story is not None:
        update_object({"is_visible": False}, FeaturedStories, current_featured_story.id)

        create_object(Events(
            _type=HIDE_FEATURED_STORY,
            story_id=current_featured_story.story_id,
            user_guid=current_user.guid,
            previous_value={"is_visible": True},
            new_value={"is_visible": False}
        ))
