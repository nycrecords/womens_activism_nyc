"""
Modules needed for main/views.py
flask:
    used render_template to load templates
    used redirect to redirect to specific url
    used url_for to designate the specific url
    used current_app for config data variables
    used flash to send messages to the user
    used request to get information from the ckeditor html form in index.html
app.db_helpers:
    used to add and commit sessions for Post with the put_obj() function
app.models:
    used Post table to add of data every time user successfully submitted a post
    used Tag table to provide a list of tags to decide from when creating a post
app.main:
    used to import the main blueprint where routes are identified from
app:
    used recaptcha for verification purposes - prevent bot spam
"""
from flask import render_template, redirect, url_for, flash, request, current_app
from app.db_helpers import put_obj
from app.models import User, Story, Tag, StoryTag
from app.main import main
from sqlalchemy.sql import or_
import ast
from app import recaptcha


@main.route('/', methods=['GET', 'POST'])
def index(data=None):
    """
    query the database for a feed of most recent posts
    query the database for the list of possible tags - passed into drop down selectfield in html
    :param data: initialized as none because we want a blank form to appear when user first loads page
    :return: renders template that displays a ckeditor where user can start writing their post.
        Second half of the page is a feed of most recent posts
    """
    visible_stories = len(Story.query.filter_by(is_visible=True).all())

    page = request.args.get('page', 1, type=int)
    pagination = Story.query.order_by(Story.creation_time.desc()).paginate(
        page, per_page=current_app.config['STORIES_PER_PAGE'],
        error_out=True)
    stories = pagination.items[:8]

    page_stories = []


    for story in stories:
        story_tags = StoryTag.query.filter_by(story_id=story.id).all()
        tags = []
        for story_tag in story_tags:
            name = Tag.query.filter_by(id=story_tag.tag_id).first().name
            tags.append(name)
        current_story = {
            'id': story.id,
            'activist_first': story.activist_first,
            'activist_last': story.activist_last,
            'activist_start': story.activist_start,
            'activist_end': story.activist_end,
            'creation_time': story.creation_time,
            'edit_time': story.edit_time,
            'is_visible': story.is_visible,
            'is_edited': story.is_edited,
            'tags': tags
        }
        if story.image_link is not None:
            current_story['content'] = story.content[:50]
            current_story['image_link'] = story.image_link
        else:
            current_story['content'] = story.content[:150]
        page_stories.append(current_story)

    missing_stories = 20000 - visible_stories

    first_four = []
    last_four = []
    for i in range(0, 8):
        try:
            if i <= 3:
                first_four.append(page_stories[i])
            else:
                last_four.append(page_stories[i])
        except IndexError:
            break

    stories = []
    stories.append(first_four)
    stories.append(last_four)

    return render_template('index.html', stories=stories, pagination=pagination,
                           visible_stories=visible_stories, missing_stories=missing_stories)


@main.route('/about', methods=['GET', 'POST'])
def about():
    # TODO: rename this route
    return render_template('about.html')


@main.route('/catalog', methods=['GET', 'POST'])
def catalog():
    tags = Tag.query.all()

    stories = Story.query.all()

    return render_template('catalog.html', tags=tags, stories=stories)


@main.route('/_get_tags', methods=['GET', 'POST'])
def get_tags():
    tag_list = request.get_data().decode('utf-8')

    tag_list = ast.literal_eval(tag_list)

    if len(tag_list) == 0:

        stories = Story.query.all()

        return render_template('_filtered_stories.html', stories=stories)

    else:

        clauses = or_(*[StoryTag.tag_id == Tag.query.filter_by(name=tag).first().id for tag in

                        tag_list])  # creates filter for query in following line

        story_tags = StoryTag.query.filter(clauses).all()  # queries the StoryTag table to find all with above clauses

        stories = []

        for story_tag in story_tags:  # loops through all story_tags found and appends the related story to the stories list

            stories.append(Story.query.filter_by(id=story_tag.story_id).first())

        unique_stories = []

        stories_dict = {i: stories.count(i) for i in

                        stories}  # creates a dictionary showing the count that a story shows up for stories list

        for key, value in stories_dict.items():  # loops through dictionary and appends only the stories that show up

            # the same number of times as the number of tags chosen

            if stories_dict[key] >= len(tag_list):
                unique_stories.append(key)

        return render_template('_filtered_stories.html', stories=unique_stories)
