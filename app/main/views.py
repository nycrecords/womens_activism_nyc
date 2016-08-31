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
def index():
    """
    query the database for a feed of most recent posts
    query the database for the list of possible tags - passed into drop down selectfield in html
    :return: renders template that displays a ckeditor where user can start writing their post.
        Second half of the page is a feed of most recent posts
    """
    visible_stories = len(Story.query.filter_by(is_visible=True).all())

    page = request.args.get('page', 1, type=int)
    pagination = Story.query.filter_by(is_visible=True).order_by(Story.creation_time.desc()).paginate(
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
            'content': story.content,
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
            current_story['image_link'] = story.image_link

        page_stories.append(current_story)

    missing_stories = 20000 - visible_stories

    stories = []
    for i in range(0, 8, 4):
        l = []
        for j in range(i, i + 4):
            try:
                l.append(page_stories[j])
            except IndexError:
                break
        stories.append(l)

    return render_template('index.html', stories=stories, pagination=pagination,
                           visible_stories=visible_stories, missing_stories=missing_stories)


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/guidelines', methods=['GET', 'POST'])
def guidelines():
    return render_template('guidelines.html')


@main.route('/catalog', methods=['GET', 'POST'])
def catalog(data=None):
    tags = []
    for i in range(0, len(Tag.query.all()), 5):
        l = []
        for j in range(i, i + 5):
            try:
                l.append(Tag.query.order_by('name asc').all()[j])
            except IndexError:
                break
        tags.append(l)

    sort_options = ['A-Z First Name', 'Z-A First Name', 'A-Z Last Name', 'Z-A Last Name']

    if data or request.method == 'POST':
        data = request.form.copy()

        tag_list = data.getlist('category_button')
        name_search = data['input_name_search']
        previous_sort_option = data.getlist('sort_option')

        if len(tag_list) > 0:
            unique_stories = []

            clauses = or_(*[StoryTag.tag_id == Tag.query.filter_by(name=tag).first().id for tag in
                            tag_list])  # creates filter for query in following line
            story_tags = StoryTag.query.filter(
                clauses).all()  # queries the StoryTag table to find all with above clauses

            if name_search != '':
                if len(previous_sort_option) > 0:  # tag_list, name_search, and previous_sort_option exist
                    stories = [Story.query.filter(
                            or_(Story.activist_first == name_search, Story.activist_last == name_search),
                            Story.id == story_tag.story_id).first() for story_tag in story_tags]
                    stories_dict = {i: stories.count(i) for i in stories}
                    for key, value in stories_dict.items():
                        if stories_dict[key] == len(tag_list):
                            unique_stories.append(key)
                    if previous_sort_option[0] == 'activist_first asc':
                        unique_stories.sort(key=lambda x: x.activist_first)
                    elif previous_sort_option[0] == 'activist_first desc':
                        unique_stories.sort(key=lambda x: x.activist_first, reverse=True)
                    elif previous_sort_option[0] == 'activist_last asc':
                        unique_stories.sort(key=lambda x: x.activist_last)
                    elif previous_sort_option[0] == 'activist_last desc':
                        unique_stories.sort(key=lambda x: x.activist_last, reverse=True)
                else:  # tag_list and name_search exist
                    stories = [Story.query.filter(
                        or_(Story.activist_first == name_search, Story.activist_last == name_search),
                        Story.id == story_tag.story_id).first() for story_tag in story_tags]
                    stories_dict = {i: stories.count(i) for i in stories}
                    for key, value in stories_dict.items():
                        if stories_dict[key] == len(tag_list):
                            unique_stories.append(key)
            else:
                if len(previous_sort_option) > 0:  # tag_list and previous_sort_option exist
                    stories = [Story.query.filter_by(id=story_tag.story_id).first() for story_tag in story_tags]
                    stories_dict = {i: stories.count(i) for i in stories}
                    for key, value in stories_dict.items():
                        if stories_dict[key] == len(tag_list):
                            unique_stories.append(key)
                    if previous_sort_option[0] == 'activist_first asc':
                        unique_stories.sort(key=lambda x: x.activist_first)
                    elif previous_sort_option[0] == 'activist_first desc':
                        unique_stories.sort(key=lambda x: x.activist_first, reverse=True)
                    elif previous_sort_option[0] == 'activist_last asc':
                        unique_stories.sort(key=lambda x: x.activist_last)
                    elif previous_sort_option[0] == 'activist_last desc':
                        unique_stories.sort(key=lambda x: x.activist_last, reverse=True)
                else:  # only tag_list exists
                    stories = [Story.query.filter_by(id=story_tag.story_id).first() for story_tag in story_tags]
                    stories_dict = {i: stories.count(i) for i in stories}
                    for key, value in stories_dict.items():
                        if stories_dict[key] == len(tag_list):
                            unique_stories.append(key)

        elif name_search != '':
            if len(previous_sort_option) > 0:  # name_search and previous_sort_option exist
                unique_stories = Story.query.filter(
                    or_(Story.activist_first == name_search, Story.activist_last == name_search)).order_by(
                    previous_sort_option[0]).all()
            else:  # only name_search exists
                unique_stories = Story.query.filter(
                    or_(Story.activist_first == name_search, Story.activist_last == name_search)).all()

        else:
            if len(previous_sort_option) > 0:  # only previous_sort_option exists
                unique_stories = Story.query.order_by(previous_sort_option[0]).all()
            else:  # none exist
                unique_stories = Story.query.order_by('id desc').all()

        page_stories = []

        for story in unique_stories:
            story_tags = StoryTag.query.filter_by(story_id=story.id).all()
            unique_tags = []
            for story_tag in story_tags:
                name = Tag.query.filter_by(id=story_tag.tag_id).first().name
                unique_tags.append(name)
            current_story = {
                'id': story.id,
                'activist_first': story.activist_first,
                'activist_last': story.activist_last,
                'activist_start': story.activist_start,
                'activist_end': story.activist_end,
                'content': story.content,
                'creation_time': story.creation_time,
                'edit_time': story.edit_time,
                'is_visible': story.is_visible,
                'is_edited': story.is_edited,
                'tags': unique_tags
            }
            if story.image_link is not None:
                current_story['image_link'] = story.image_link
            page_stories.append(current_story)

        stories = []
        for i in range(0, len(page_stories), 4):
            l = []
            for j in range(i, i + 4):
                try:
                    l.append(page_stories[j])
                except IndexError:
                    break
            stories.append(l)

        return render_template('catalog.html', tags=tags, stories=stories, tag_list=tag_list, name_search=name_search,
                               previous_sort_option=previous_sort_option, sort_options=sort_options)

    unique_stories = Story.query.order_by('id desc').all()

    page_stories = []

    for story in unique_stories:
        story_tags = StoryTag.query.filter_by(story_id=story.id).all()
        unique_tags = []
        for story_tag in story_tags:
            name = Tag.query.filter_by(id=story_tag.tag_id).first().name
            unique_tags.append(name)
        current_story = {
            'id': story.id,
            'activist_first': story.activist_first,
            'activist_last': story.activist_last,
            'activist_start': story.activist_start,
            'activist_end': story.activist_end,
            'content': story.content,
            'creation_time': story.creation_time,
            'edit_time': story.edit_time,
            'is_visible': story.is_visible,
            'is_edited': story.is_edited,
            'tags': unique_tags
        }
        if story.image_link is not None:
            current_story['image_link'] = story.image_link
        page_stories.append(current_story)

    stories = []
    for i in range(0, len(page_stories), 4):
        l = []
        for j in range(i, i + 4):
            try:
                l.append(page_stories[j])
            except IndexError:
                break
        stories.append(l)

    return render_template('catalog.html', tags=tags, stories=stories, sort_options=sort_options)


@main.route('/_get_tags', methods=['GET', 'POST'])
def get_tags():
    tag_list = request.get_data().decode('utf-8')
    tag_list = ast.literal_eval(tag_list)
    if len(tag_list) == 0:
        page_stories = []

        for story in Story.query.order_by('id desc').all():
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
                'content': story.content,
                'creation_time': story.creation_time,
                'edit_time': story.edit_time,
                'is_visible': story.is_visible,
                'is_edited': story.is_edited,
                'tags': tags
            }
            if story.image_link is not None:
                current_story['image_link'] = story.image_link
            page_stories.append(current_story)

        stories = []
        for i in range(0, len(Story.query.all()), 4):
            l = []
            for j in range(i, i + 4):
                try:
                    l.append(page_stories[j])
                except IndexError:
                    break
            stories.append(l)

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

        page_stories = []

        for story in unique_stories:
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
                'content': story.content,
                'creation_time': story.creation_time,
                'edit_time': story.edit_time,
                'is_visible': story.is_visible,
                'is_edited': story.is_edited,
                'tags': tags
            }
            if story.image_link is not None:
                current_story['image_link'] = story.image_link
            page_stories.append(current_story)

        page_stories.reverse()

        stories = []
        for i in range(0, len(page_stories), 4):
            l = []
            for j in range(i, i + 4):
                try:
                    l.append(page_stories[j])
                except IndexError:
                    break
            stories.append(l)

        return render_template('_filtered_stories.html', stories=stories)
