"""
Modules needed for stories/views.py
flask:
    used render_template to load templates
    used redirect to redirect to specific url
    used url_for to designate the specific url
    used current_app for config data variables
    used flash to send messages to the user
    used request to query the db or html for information
app.models:
    used Story table to call in the information pertaining to a specific story
    used User table to associate information about user_id to specific post edit or delete
    used StoryTag table to call in information that associated posts with their attached tags
    used Tag table to call in all the tags to populate drop down menu during story creation
    used StoryEdit table to write old story history and metadata for audit purposes
app.stories:
    used to import the stories blueprint where routes are identified from
app.db_helpers:
    used put_obj(obj) to add and commit sessions for Story
    used delete_obj(obj) to delete tags associated with a Story in the edit route
flask_login:
    used login_required to limit edit and delete routes so that only verified users can see them
    used current_user to grab information about user_id so that it can be associated with a story edit or delete
datetime:
    used datetime to keep timestamps of when edits and deletes to stories were made
app:
    used recaptcha for verification that the story was not shared by a bot
app.send_email:
    send_email() function defined in app/send_email.py used to send email to recipient, formats subject title and email content
"""
from datetime import datetime

import requests
from flask import render_template, current_app, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app.db_helpers import put_obj, delete_obj
from app.models import Story, User, StoryTag, Tag, StoryEdit
from app.send_email import send_email
from app.stories import stories


@stories.route('/share', methods=['GET', 'POST'])
def share(data=None):
    """
    route where user is prompted to enter information about the woman that inspires them
        Required fields are activist first and last name, activist start and end date, tag, recaptcha
        Optional fields, located in the html _share.html are activist_link, activist_media, and information about the
            poster themselves
    :param data: initialized as none because we want the html text fields to be blank/have placeholders
    :return: renders template where user can share their story "post" flashes success message if completed
     renders template with information retained in session if user has not completed a required field
    """
    tags = []
    for i in range(0, len(Tag.query.all()), 5):
        l = []
        for j in range(i, i + 5):
            try:
                l.append(Tag.query.order_by('name asc').all()[j])
            except IndexError:
                break
        tags.append(l)

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
        image_link = data['image_link']
        video_link = data['video_link']
        tag_list = data.getlist('category_button')

        if video_link and video_link != '':
            valid_video = requests.get(video_link)
            valid_video = (valid_video.status_code == 200)
            if "youtube" not in video_link and "youtu.be" not in video_link and "vimeo" not in video_link:
                valid_video = False
        else:
            valid_video = True

        if image_link and image_link != '':
            if (image_link[-3:].lower() == 'jpg') or (image_link[-3:].lower() == 'png') or (image_link[-4:].lower() == 'jpeg'):
                valid_image = requests.get(image_link)
                valid_image = (valid_image.status_code == 200)
            else:
                valid_image = False
        else:
            valid_image = True

        if activist_first_name == '':  # user has not submitted activist first name
            flash("Please enter a first name for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link, video_link=video_link)
        elif activist_last_name == '':  # user has not submitted activist last name
            flash("Please enter a last name for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link, video_link=video_link)
        # elif activist_start_date == '':  # user has not submitted activist start date
        #     flash("Please enter a year of birth for women's activist.")
        #     return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
        #                            activist_last_name=activist_last_name, activist_start_date=activist_start_date,
        #                            activist_end_date=activist_end_date, content=content, activist_link=activist_link,
        #                            author_first_name=author_first_name, author_last_name=author_last_name,
        #                            author_email=author_email, image_link=image_link, video_link=video_link)
        # elif activist_end_date == '':  # user has not submitted activist end date
        #     flash("Please enter a year of death for women's activist.")
        #     return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
        #                            activist_last_name=activist_last_name, activist_start_date=activist_start_date,
        #                            activist_end_date=activist_end_date, content=content, activist_link=activist_link,
        #                            author_first_name=author_first_name, author_last_name=author_last_name,
        #                            author_email=author_email, image_link=image_link, video_link=video_link)
        elif len(activist_end_date) == 5 and activist_end_date != 'Today':  # user submitted invalid activist end date
            flash("Please enter a valid year of death for women's activist.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link, video_link=video_link)
        elif activist_end_date < activist_start_date:
            flash("Please enter realistic years.")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link, video_link=video_link)
        elif len(tag_list) == 0:  # user submitted no tags
            flash('Please choose at least one tag.')
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link, video_link=video_link)
        elif content == '':  # user has not submitted content
            flash('Please enter a story.')
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link, video_link=video_link)
        elif not valid_video:
            flash("Invalid video link. Please check your video link")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link)
        elif not valid_image:
            flash("Invalid image link. Please check your image")
            return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
                                   activist_last_name=activist_last_name, activist_start_date=activist_start_date,
                                   activist_end_date=activist_end_date, content=content, activist_link=activist_link,
                                   author_first_name=author_first_name, author_last_name=author_last_name,
                                   author_email=author_email, image_link=image_link)
        # elif recaptcha.verify() == False:  # user has not passed the recaptcha verification
        #     flash("Please complete reCAPTCHA.")
        #     return render_template('stories/share.html', tags=tags, activist_first_name=activist_first_name,
        #                            activist_last_name=activist_last_name, activist_start_date=activist_start_date,
        #                            activist_end_date=activist_end_date, content=content, activist_link=activist_link,
        #                            author_first_name=author_first_name, author_last_name=author_last_name,
        #                            author_email=author_email, image_link=image_link)
        else:  # user has successfully submitted
            if len(author_first_name) > 0 or len(author_last_name) > 0 or len(author_email) > 0:
                # user entered information about themselves
                user = User(first_name=author_first_name, last_name=author_last_name,
                            email=author_email)  # creates user
                put_obj(user)  # adds user into database

                story = Story(activist_start=activist_start_date, activist_end=activist_end_date,
                              activist_first=activist_first_name, activist_last=activist_last_name, content=content,
                              activist_url=activist_link, poster_id=user.id, is_edited=False, is_visible=True,
                              image_link=image_link, video_link=video_link, creation_time=datetime.utcnow())
            else:  # user only entered the basic/required information
                story = Story(activist_start=activist_start_date, activist_end=activist_end_date,
                              activist_first=activist_first_name, activist_last=activist_last_name, content=content,
                              activist_url=activist_link, is_edited=False, is_visible=True,
                              image_link=image_link, video_link=video_link, creation_time=datetime.utcnow())

            if "youtube.com/embed/" in video_link:  # if the link is a youtube embed leave it the way it is
                story.video_link = video_link

            elif "youtube.com/watch?v=" in video_link:  # if the link is a youtube link convert it to an embed
                split = video_link.split("watch?v=", 1)
                video_link = "https://www.youtube.com/embed/{}".format(split[1])
                story.video_link = video_link

            elif "youtu.be/" in video_link:  # if the link is a short youtube link convert it to an embed
                split = video_link.split("youtu.be/", 1)
                video_link = "https://www.youtube.com/embed/{}".format(split[1])
                story.video_link = video_link

            elif "vimeo" in video_link:  # if the link is a vimeo link convert it to an embed
                split = video_link.split("vimeo.com/", 1)
                video_link = "https://player.vimeo.com/video/{}".format(split[1])
                story.video_link = video_link

            if image_link == '':  # if image_link is blank set it to None
                print("image null")
                image_link = None
                story.image_link = image_link

            if video_link == '':  # if video_link is blank set it to None
                print("video null")
                video_link = None
                story.video_link = video_link

            put_obj(story)  # adds story into the database

            for tag in tag_list:  # loops through all tags chosen
                story_tag = StoryTag(story_id=story.id,
                                     tag_id=Tag.query.filter_by(name=tag).first().id)  # creates StoryTag relation
                put_obj(story_tag)  # adds storytag into database

            flash('Story submitted!')
            return redirect(url_for('stories.share'))
    return render_template('stories/share.html', tags=tags)


@stories.route('/stories', methods=['GET', 'POST'])
def all_stories():
    """
    Route that displays all the stories stored in the db (visible)
    Displays all stories in a paginated fashion.
    :return: renders 'storiesTab.html', passes in page_stories which is list of story dictionary with information
        pertaining to each story (ordered by creation_time)
    """
    page = request.args.get('page', 1, type=int)
    pagination = Story.query.order_by(Story.creation_time.desc()).paginate(
        page, per_page=current_app.config['STORIES_PER_PAGE'],
        error_out=True)
    stories_feed = pagination.items

    page_stories = []
    """
    page_stories is a list of dictionary containing attributes of stories
    page_stories is used because tags cannot be accessed through stories
    tags is accessed only by looping through the StoryTag table
    """
    for story in stories_feed:
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
            'tags': tags,
            'image_link': story.image_link,
            'video_link': story.video_link
        }
        page_stories.append(story)

    return render_template('stories/storiesTab.html', stories=page_stories, paganation=pagination)


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
    all_tags = Tag.query.all()

    story_tags = StoryTag.query.filter_by(story_id=story.id).all()
    tags = []
    for story_tag in story_tags:
        name = Tag.query.filter_by(id=story_tag.tag_id).first().name
        tags.append(name)
    """
    single_story is a dictionary that incorporates information from the single story and tags
    """
    single_story = {
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
        'tags': tags,
        'image_link': story.image_link,
        'video_link': story.video_link

    }

    if request.method == 'POST':
        data = request.form.copy()
        user_id = current_user.id
        user_first = User.query.filter_by(id=user_id).first().first_name
        user_last = User.query.filter_by(id=user_id).first().last_name

        story_edit = StoryEdit(story_id=story.id, user_id=user_id, creation_time=story.creation_time,
                               edit_time=datetime.utcnow(), type='Edit', activist_first=story.activist_first,
                               activist_last=story.activist_last, activist_start=story.activist_start,
                               activist_end=story.activist_end, activist_url=story.activist_url,
                               poster_id=story.poster_id, content=story.content,
                               reason=data['input_reason'], version=story.version,
                               image_link=story.image_link, video_link=story.video_link)
        put_obj(story_edit)

        new_activist_first = data['input_first']
        new_activist_last = data['input_last']
        new_activist_start = data['input_start']
        new_activist_end = data['input_end']
        new_activist_url = data['input_url']
        new_content = data['editor1']
        new_is_edited = True
        new_version = story.version + 1
        new_edit_time = datetime.utcnow()
        new_image_link = data['image_link']
        new_video_link = data['video_link']

        story.activist_first = new_activist_first
        story.activist_last = new_activist_last
        story.activist_start = new_activist_start
        story.activist_end = new_activist_end
        story.activist_url = new_activist_url
        story.content = new_content
        story.is_edited = new_is_edited
        story.version = new_version
        story.edit_time = new_edit_time
        story.image_link = new_image_link
        story.video_link = new_video_link

        if new_image_link != '' and new_video_link != '':  # if both image and video is filled out flash a message
            flash("You have both an Image link and Video link. Please only fill out one.")
            return render_template('stories/edit_story.html', tags=all_tags, story_tags=single_story['tags'],
                                   story=story)

        if "youtube.com/embed/" in story.video_link:  # if the link is already an embed link leave it the way it is
            pass

        elif "youtube.com/watch?v=" in story.video_link:  # if the link is a youtube link convert it to an embed
            split = story.video_link.split("watch?v=", 1)
            new_embed = "https://www.youtube.com/embed/{}".format(split[1])
            story.video_link = new_embed

        elif "youtu.be" in story.video_link:  # if the link is a short youtube link convert it to an embed
            split = story.video_link.split("youtu.be/", 1)
            new_embed = "https://www.youtube.com/embed/{}".format(split[1])
            story.video_link = new_embed

        elif "vimeo" in story.video_link:  # if the link is a vimeo link conver it to an embed
            split = story.video_link.split("vimeo.com/", 1)
            new_embed = "https://player.vimeo.com/video/{}".format(split[1])
            story.video_link = new_embed

        if story.image_link == '':  # if image_link is blank set it to None
            story.image_link = None

        if story.video_link == '':  # if video_link is blank set it to None
            story.video_link = None

        put_obj(story)

        tag_list = request.form.getlist('input_tags')
        new_tags = tag_list
        old_tags = single_story['tags']
        for tag in tag_list:
            if tag not in single_story['tags']:
                story_tag = StoryTag(story_id=story.id, tag_id=Tag.query.filter_by(name=tag).first().id)
                put_obj(story_tag)
        for tag in single_story['tags']:
            if tag not in tag_list:
                old_tag = Tag.query.filter_by(name=tag).first().id
                delete_story_tag = StoryTag.query.filter_by(story_id=story.id, tag_id=old_tag).first()
                delete_obj(delete_story_tag)
        flash('The story has been edited.')

        send_email(to=current_app.config['WOMENS_ADMIN'], subject='Edit Made on a Story',
                   template='mail/email_edit', story_edit=story_edit, story=story,
                   old_tags=old_tags, new_tags=new_tags, user_first=user_first, user_last=user_last)
        return redirect(url_for('stories.all_stories'))
    return render_template('stories/edit_story.html', story=story, tags=all_tags, story_tags=single_story['tags'])


@stories.route('/stories/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Takes a story and makes it not visible - "deleted" status
    Story lives on in Story table but is_visible = False and will not show up on feeds
    The Edit is also in StoryEdit table for auditing purposes (reason, who deleted, etc)
    :param(id) Query the db with id for the Story to display information in the delete_story.html
    :return redirect to stories page with feed of all stories
    """
    story = Story.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form.copy()
        user_id = current_user.id
        user_first = User.query.filter_by(id=user_id).first().first_name
        user_last = User.query.filter_by(id=user_id).first().last_name

        story_edit = StoryEdit(story_id=story.id, user_id=user_id, creation_time=story.creation_time,
                               edit_time=datetime.utcnow(), type='Delete', activist_first=story.activist_first,
                               activist_last=story.activist_last, activist_start=story.activist_start,
                               activist_end=story.activist_end, activist_url=story.activist_url,
                               poster_id=story.poster_id, content=story.content,
                               reason=data['input_reason'], version=story.version)
        put_obj(story_edit)

        new_edit_time = datetime.utcnow()
        new_is_visible = False
        story.is_visible = new_is_visible
        story.edit_time = new_edit_time
        put_obj(story)

        flash('The story has been deleted.')

        send_email(to=current_app.config['WOMENS_ADMIN'], subject='Delete Made on a Story',
                   template='mail/email_delete', story_edit=story_edit, story=story, user_first=user_first,
                   user_last=user_last)
        return redirect(url_for('stories.all_stories'))
    return render_template('stories/delete_story.html', story=story)


@stories.route('/stories/<int:id>', methods=['GET', 'POST'])
def stories(id):
    """
    Route used to show a story on its own single page
    :param id: Unique identifier for story (story_id).
    Views a single story on its own page
    :return: renders 'stories.html', passes in post information
    """
    single_story = Story.query.get_or_404(id)
    """
    story is a dictionary that incorporates information from the single story and tags
    """
    story_tags = StoryTag.query.filter_by(story_id=single_story.id).all()
    tags = []
    for story_tag in story_tags:
        name = Tag.query.filter_by(id=story_tag.tag_id).first().name
        tags.append(name)
    story = {
        'id': single_story.id,
        'activist_first': single_story.activist_first,
        'activist_last': single_story.activist_last,
        'activist_start': single_story.activist_start,
        'activist_end': single_story.activist_end,
        'creation_time': single_story.creation_time,
        'edit_time': single_story.edit_time,
        'content': single_story.content,
        'is_visible': single_story.is_visible,
        'is_edited': single_story.is_edited,
        'tags': tags,
        'image_link': single_story.image_link,
        'video_link': single_story.video_link,
    }

    if single_story.poster_id:
        poster = User.query.filter_by(id=single_story.poster_id).first()
    else:
        poster = None

    return render_template('stories/stories.html', story=story, poster=poster)
