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
from app import recaptcha


# @main.route('/simon', methods=['GET', 'POST'])
# # TODO: Delete this route, we don't need it anymore - any changes made by simon needs to be implemented into index.html
# def simonindex(data=None):
#     page = request.args.get('page', 1, type=int)
#     pagination = Story.query.order_by(Story.creation_time.desc()).paginate(
#         page, per_page=current_app.config['POSTS_PER_PAGE'],
#         error_out=True)
#     stories = pagination.items
#
#     page_posts = []
#
#     for post in stories:
#         post_tags = PostTag.query.filter_by(post_id=post.id).all()
#         tags = []
#         for post_tag in post_tags:
#             name = Tag.query.filter_by(id=post_tag.tag_id).first().name
#             tags.append(name)
#         story = {
#             'id': post.id,
#             'activist_first': post.activist_first,
#             'activist_last': post.activist_last,
#             'activist_start': post.activist_start,
#             'activist_end': post.activist_end,
#             'creation_time': post.creation_time,
#             'edit_time': post.edit_time,
#             'content': post.content,
#             'is_visible': post.is_visible,
#             'is_edited': post.is_edited,
#             'tags': tags
#         }
#         page_posts.append(story)
#
#     return render_template('new_index.html', stories=page_posts, pagination=pagination)
@main.route('/', methods=['GET', 'POST'])
# TODO: Delete this route, we don't need it anymore - any changes made by simon needs to be implemented into index.html
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
    # TODO: rename this route
    return render_template('about.html')


@main.route('/catalog', methods=['GET', 'POST'])
def catalog():
    # TODO: rename this route and put it into stories/views.py
    # TODO: edit catalog.html to have the contents of postTab.html and then delete postTab.html
    tags = Tag.query.all()
    return render_template('catalog.html', tags=tags)
