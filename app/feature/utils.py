"""
Utility functions used for view functions involving featured stories
"""
import uuid
from flask import current_app
from app.constants.event import ADD_FEATURED_STORY, DELETE_FEATURED_STORY, EDIT_FEATURED_STORY
from app.models import Stories, Users, Events, Flags, FeaturedStories
from app.db_utils import update_object, create_object

def find_max_rank():
    """
    A function that finds the largest number in FeaturedStories table
    :return: largest number in rank's column in Featured Stories
    """
    feature = FeaturedStories.query.order_by(FeaturedStories.rank.desc()).first()
    new_rank = 1
    if feature.rank is not None:
        new_rank = feature.rank + 1

    return new_rank


def create_featuredstory(story, left_right, quote):
    """
    A utility function to create a featured story.
    :param story: the story object you would like to create in Featured Story
    :param left_right: left or right side where the image will go
    :param quote: a famous quote that was once said by this activist
    :return: None
    """
    # taking the largest rank value in the FeaturedStories table

    new_rank = find_max_rank()

    featuredStory = FeaturedStories(
        story_id=story.id,
        left_right=True if left_right == 'left' else False,
        is_visible=True,
        quote=quote,
        rank=new_rank
    )

    create_object(featuredStory)

    create_object(Events(
        story_id=story.id,
        user_guid=story.user_guid,
        _type=ADD_FEATURED_STORY,
        new_value=featuredStory.val_for_events
    ))

    # Create the elasticsearch story doc
    if current_app.config['ELASTICSEARCH_ENABLED']:
        story.es_create()


def update_featuredstory(story, left_right=None, quote=None, is_visible=None, rank=None):
    """
    A utility function to update a featured story.
    Updating attributes such as the following:
    :param story: the story object you would like to update in Featured Story
    :param left_right: left or right side where the image will go
    :param quote: a famous quote that was once said by this activist
    :param is_visible: the visibility of the featured story
    :param rank: the rank of the Featured Stories in the home page
    :return: None
    """

    featuredStory = FeaturedStories.query.filter_by(story_id=story.id).one()
    old_featuredStory_json = featuredStory.val_for_events
    if left_right is not None:
        featuredStory.left_right = left_right
    if quote is not None:
        featuredStory.quote = quote
    if is_visible is not None:
        featuredStory.is_visible = is_visible
    if rank is None:
        rank = find_max_rank()
    featuredStory.rank = rank

    update_object(featuredStory)

    create_object(Events(
        story_id=story.id,
        user_guid=story.user_guid,
        _type=EDIT_FEATURED_STORY,
        previous_value=old_featuredStory_json,
        new_value=featuredStory.val_for_events,
    ))

    # Create the elasticsearch story doc
    if current_app.config['ELASTICSEARCH_ENABLED']:
        story.es_create()


def remove_featuredstory(story_id):
    """
    A utility function to hide a story from featured story module (main page).
    Hiding does not *delete* the record from the table, but rather makes it invisible.
    :param story_id: the story id you would like to hide from the featuredstories table
    :return: None
    """
    story = Stories.query.filter_by(id=story_id).one()
    featuredStory = FeaturedStories.query.filter_by(story_id=story_id).one()
    old_json = featuredStory.val_for_events
    featuredStory.is_visible = False
    featuredStory.rank = 0
    update_object(featuredStory)
    create_object(Events(
        story_id=story_id,
        user_guid=story.user_guid,
        _type=DELETE_FEATURED_STORY,
        previous_value=old_json,
        new_value=featuredStory.val_for_events
    ))

    # Create the elasticsearch story doc
    if current_app.config['ELASTICSEARCH_ENABLED']:
        story.es_create()
