"""
modules used for post/views.py
flask: framework used for project
app: used to get db so we can perform SQLalchemy operations
app.models: used to get the Post and Comment table to view Posts and Comments
            used to get the PostEdit table to write post history to it
app.posts: used to get the posts blueprint for routes
app.posts.forms: used to get the CommentForm to create Comments
app.db_helpers: used as utility functions for SQLalchemy operations
flask_login: used login_required so that only
"""
from flask import render_template, request, current_app, flash, redirect, url_for
from app.models import Story, User, StoryTag, Tag, StoryEdit
from app.stories import stories
from app.db_helpers import put_obj, delete_obj
from flask_login import login_required, current_user
from datetime import datetime
from app import recaptcha


@stories.route('/shareastory', methods=['GET', 'POST'])
def shareastory(data=None):
    # TODO: rename this route and put it into stories/views.py
    tags = Tag.query.all()

    if data or request.method == 'POST':  # user pressed submit button
        data = request.form.copy()

        activist_first_name = data['activist_first_name']
        activist_last_name = data['activist_last_name']
        activist_start_date = data['input_birth']
        activist_end_date = data['input_death']
        content = data['editor1']
        activist_link = data['input_url_link']
        author_first_name = data['author_first_name']
        author_last_name = data['author_last_name']
        author_email = data['author_email']

        if activist_first_name == '':  # user has not submitted activist first name
            flash("Please enter a first name for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif activist_last_name == '':  # user has not submitted activist last name
            flash("Please enter a last name for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif activist_start_date == '':  # user has not submitted activist start date
            flash("Please enter a year of birth for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif activist_end_date == '':  # user has not submitted activist end date
            flash("Please enter a year of death for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif len(activist_end_date) == 5 and activist_end_date != 'Today':  # user submitted invalid activist end date
            flash("Please enter a valid year of death for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif len(request.form.getlist('input_tags')) == 0:  # user submitted no tags
            flash('Please choose at least one tag.')
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif content == '':  # user has not submitted content
            flash('Please enter a story.')
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email)
        elif recaptcha.verify() == False:  # user has not passed the recaptcha verification
            flash("Please complete reCAPTCHA.")
            return render_template('stories/share.html', tags=tags)
        else:  # user has successfully submitted

            if len(author_first_name) > 0 or len(author_last_name) > 0 or len(author_email) > 0:
                user = User(first_name=author_first_name, last_name=author_last_name, email=author_email)
                put_obj(user)

                story = Story(activist_start=activist_start_date, activist_end=activist_end_date,
                              activist_first=activist_first_name, activist_last=activist_last_name, content=content,
                              activist_url=activist_link, poster_id=user.id, is_edited=False, is_visible=True)
            else:
                story = Story(activist_start=activist_start_date, activist_end=activist_end_date,
                              activist_first=activist_first_name, activist_last=activist_last_name, content=content,
                              activist_url=activist_link, is_edited=False, is_visible=True)

            put_obj(story)

            tag_list = request.form.getlist('input_tags')
            for tag in tag_list:
                story_tag = StoryTag(story_id=story.id, tag_id=Tag.query.filter_by(name=tag).first().id)
                put_obj(story_tag)

            flash('Story submitted!')
            return redirect(url_for('main.index'))
    return render_template('stories/share.html', tags=tags)


@stories.route('/stories', methods=['GET', 'POST'])
def all_stories():
    # TODO: Render the correct template - archive.html instead of postTab.html
    """
    Route for seperate post tab that shows all stories in the db.
    Displays all stories in a paginated fashion.
    :return: renders 'postTab.html', passes in post_feed as all stories in Post table (ordered by creation_time)
    """
    page = request.args.get('page', 1, type=int)
    pagination = Story.query.order_by(Story.creation_time.desc()).paginate(
        page, per_page=current_app.config['STORIES_PER_PAGE'],
        error_out=True)
    stories_feed = pagination.items

    page_stories = []
    """
    page_posts is a list of dictionary containing attributes of stories
    page_posts is used because tags cannot be accessed through stories
    """

    for story in stories_feed:
        story_tags = StoryTag.query.filter_by(story_id=story.id).all()
        tags = []
        for story_tag in story_tags:
            name = Tag.query.filter_by(id=story_tag.tag_id).first().name
            tags.append(name)
        story = {
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'time': story.creation_time,
            'edit_time': story.edit_time,
            'is_visible': story.is_visible,
            'is_edited': story.is_edited,
            'tags': tags
        }
        page_stories.append(story)
    return render_template('stories/storiesTab.html', stories=page_stories, pagination=pagination)


@stories.route('/stories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    # TODO: change post attributes to reflect new models.py
    """
    :param(id) Query the db with id for the Post to display information in it
    :return template with ckeditor with post information to begin the edit
        on completion it will redirect to the stories page with feed of all stories
    Returns the confirmation page for editing a post(s).
    Admins can see both old and new edit(s) from PostEdit table if needed for Audits
    The latest post update lives in Post table
    All post history that cannot be seen by user lives in PostEdit table
    """
    story = Story.query.get_or_404(id)

    story_tags = StoryTag.query.filter_by(story_id=story.id).all()
    tags = []
    for story_tag in story_tags:
        name = Tag.query.filter_by(id=story_tag.tag_id).first().name
        tags.append(name)
    story = {
        'id': story.id,
        'title': story.title,
        'content': story.content,
        'time': story.creation_time,
        'edit_time': story.edit_time,
        'is_visible': story.is_visible,
        'is_edited': story.is_edited,
        'tags': tags
    }

    all_tags = Tag.query.all()

    if request.method == 'POST':
        data = request.form.copy()
        user = current_user.id

        # TODO: be able to edit activist name and years active
        # add in user id later, writing the old post history into PostEdit table
        story_edit = StoryEdit(story_id=story.id, user_id=user, creation_time=story.creation_time,
                             edit_time=datetime.utcnow(),
                             type='Edit', content=story.content, reason=data['input_reason'],
                             version=story.version)
        put_obj(story_edit)

        new_content = data['editor1']
        new_is_edited = True
        new_version = story.version + 1
        new_edit_time = datetime.utcnow()
        story.content = new_content
        story.is_edited = new_is_edited
        story.version = new_version
        story.edit_time = new_edit_time
        put_obj(story)
        tag_list = request.form.getlist('input_tags')
        for tag in tag_list:
            if tag not in story['tags']:
                story_tag = StoryTag(story_id=story.id, tag_id=Tag.query.filter_by(name=tag).first().id)
                put_obj(story_tag)
        for tag in story['tags']:
            if tag not in tag_list:
                old_tag = Tag.query.filter_by(name=tag).first().id
                delete_story_tag = StoryTag.query.filter_by(story_id=story.id, tag_id=old_tag).first()
                delete_obj(delete_story_tag)
        flash('The story has been edited.')
        return redirect(url_for('stories.all_stories'))
    return render_template('stories/edit_story.html', story=story, tags=all_tags, story_tags=tags)


@stories.route('/stories/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    # TODO: change post attributes to reflect new models.py
    """
    :param(id) Query the db with id for the Post to display information in it
    :return redirect to stories page with feed of all stories
    Takes a post and makes it not visible - "deleted" status
    Post lives on in Post table but is_visible = False and will not show up on feeds
    Admins can still see the "deleted" post(s)
    """
    story = Story.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form.copy()
        user = current_user.id

        # TODO: be able to edit activist name and years active
        story_edit = StoryEdit(story_id=story.id, user_id=user, creation_time=story.creation_time, edit_time=datetime.utcnow(),
                             type='Delete',
                             content=story.content, reason=data['input_reason'], version=story.version)
        put_obj(story_edit)

        new_edit_time = datetime.utcnow()
        new_is_visible = False
        story.is_visible = new_is_visible
        story.edit_time = new_edit_time
        put_obj(story)

        flash('The story has been deleted.')
        return redirect(url_for('stories.all_stories'))
    return render_template('stories/delete_story.html', story=story)


@stories.route('/stories/<int:id>', methods=['GET', 'POST'])
def stories(id):
    # TODO: change post attributes to reflect new models.py
    """
    Route used to show a post on its own single page
    :param id: Unique identifier for post (post_id).
    Views a single post on its own page
    :return: renders 'post.html', passes in post information
    """
    single_story = Story.query.get_or_404(id)
    """
        page_posts is a list of dictionary containing attributes of stories
        page_posts is used because tags cannot be accessed through stories
    """
    story_tags = StoryTag.query.filter_by(story_id=single_story.id).all()
    tags = []
    for story_tag in story_tags:
        name = Tag.query.filter_by(id=story_tag.tag_id).first().name
        tags.append(name)
    story = {
        'id': single_story.id,
        'title': single_story.title,
        'content': single_story.content,
        'time': single_story.creation_time,
        'edit_time': single_story.edit_time,
        'is_visible': single_story.is_visible,
        'is_edited': single_story.is_edited,
        'tags': tags
    }
    return render_template('stories/stories.html', story=story)
