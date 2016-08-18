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


@main.route('/', methods=['GET', 'POST'])
def index():
    visible_stories = len(Story.query.filter_by(is_visible=True).all())

    page = request.args.get('page', 1, type=int)
    pagination = Story.query.order_by(Story.creation_time.desc()).paginate(
        page, per_page=current_app.config['STORIES_PER_PAGE'],
        error_out=True)
    stories = pagination.items

    page_stories = []

    for story in stories:
        story_tags = StoryTag.query.filter_by(story_id=story.id).all()
        tags = []
        for story_tag in story_tags:
            name = Tag.query.filter_by(id=story_tag.tag_id).first().name
            tags.append(name)
        story = {
            'id': story.id,
            'activist_first': story.activist_first,
            'activist_last': story.activist_last,
            'activist_start': story.activist_start,
            'activist_end': story.activist_end,
            'creation_time': story.creation_time,
            'edit_time': story.edit_time,
            'content': story.content,
            'is_visible': story.is_visible,
            'is_edited': story.is_edited,
            'tags': tags
        }
        page_stories.append(story)

    return render_template('new_index.html', stories=page_stories, pagination=pagination, visible_stories=visible_stories)


@main.route('/about', methods=['GET', 'POST'])
def about():
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
        story_tags = StoryTag.query.filter(clauses).all()  # queries the PostTag table to find all with above clauses
        stories = []
        for story_tag in story_tags:  # loops through all post_tags found and appends the related post to the posts list
            stories.append(Story.query.filter_by(id=story_tag.post_id).first())
        unique_stories = []
        stories_dict = {i: stories.count(i) for i in
                      stories}  # creates a dictionary showing the count that a post shows up for posts list
        for key, value in stories_dict.items():  # loops through dictionary and appends only the posts that show up
                                                # the same number of times as the number of tags chosen
            if stories_dict[key] >= len(tag_list):
                unique_stories.append(key)
        return render_template('_filtered_stories.html', stories=unique_stories)
