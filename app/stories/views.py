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
from app.models import Post, PostEdit, PostTag, Tag
from app.stories import stories
from app.db_helpers import put_obj, delete_obj
from flask_login import login_required, current_user
from datetime import datetime
from app import db


@posts.route('/stories', methods=['GET', 'POST'])
def all_posts():
    # TODO: Render the correct template - archive.html instead of postTab.html
    """
    Route for seperate post tab that shows all stories in the db.
    Displays all stories in a paginated fashion.
    :return: renders 'postTab.html', passes in post_feed as all stories in Post table (ordered by creation_time)
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    posts_feed = pagination.items

    page_posts = []
    """
    page_posts is a list of dictionary containing attributes of stories
    page_posts is used because tags cannot be accessed through stories
    """

    for post in posts_feed:
        post_tags = PostTag.query.filter_by(post_id=post.id).all()
        tags = []
        for post_tag in post_tags:
            name = Tag.query.filter_by(id=post_tag.tag_id).first().name
            tags.append(name)
        story = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'time': post.creation_time,
            'edit_time': post.edit_time,
            'is_visible': post.is_visible,
            'is_edited': post.is_edited,
            'tags': tags
        }
        page_posts.append(story)
    return render_template('stories/postsTab.html', posts=page_posts, pagination=pagination)


@posts.route('/stories/edit/<int:id>', methods=['GET', 'POST'])
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
    post = Post.query.get_or_404(id)

    post_tags = PostTag.query.filter_by(post_id=post.id).all()
    tags = []
    for post_tag in post_tags:
        name = Tag.query.filter_by(id=post_tag.tag_id).first().name
        tags.append(name)
    story = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'time': post.creation_time,
        'edit_time': post.edit_time,
        'is_visible': post.is_visible,
        'is_edited': post.is_edited,
        'tags': tags
    }

    all_tags = Tag.query.all()

    if request.method == 'POST':
        data = request.form.copy()
        user = current_user.id

        # add in user id later, writing the old post history into PostEdit table
        post_edit = PostEdit(post_id=post.id, user_id=user, creation_time=post.creation_time,
                             edit_time=datetime.utcnow(),
                             type='Edit', title=post.title, content=post.content, reason=data['input_reason'],
                             version=post.version)
        put_obj(post_edit)

        new_title = data['input_title']
        new_content = data['editor1']
        new_is_edited = True
        new_version = post.version + 1
        new_edit_time = datetime.utcnow()
        post.title = new_title
        post.content = new_content
        post.is_edited = new_is_edited
        post.version = new_version
        post.edit_time = new_edit_time
        put_obj(post)
        tag_list = request.form.getlist('input_tags')
        for tag in tag_list:
            if tag not in story['tags']:
                post_tag = PostTag(post_id=post.id, tag_id=Tag.query.filter_by(name=tag).first().id)
                put_obj(post_tag)
        for tag in story['tags']:
            if tag not in tag_list:
                old_tag = Tag.query.filter_by(name=tag).first().id
                delete_post_tag = PostTag.query.filter_by(post_id=post.id, tag_id=old_tag).first()
                delete_obj(delete_post_tag)
        flash('The post has been edited.')
        return redirect(url_for('stories.all_posts'))
    return render_template('stories/edit_post.html', post=story, tags=all_tags, post_tags=tags)


@posts.route('/stories/delete/<int:id>', methods=['GET', 'POST'])
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
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form.copy()
        user = current_user.id

        post_edit = PostEdit(post_id=post.id, user_id=user, creation_time=post.creation_time, edit_time=datetime.utcnow(),
                             type='Delete', title=post.title,
                             content=post.content, reason=data['input_reason'], version=post.version)
        put_obj(post_edit)

        new_edit_time = datetime.utcnow()
        new_is_visible = False
        post.is_visible = new_is_visible
        post.edit_time = new_edit_time
        put_obj(post)

        flash('The post has been deleted.')
        return redirect(url_for('stories.all_posts'))
    return render_template('stories/delete_post.html', post=post)


@posts.route('/stories/<int:id>', methods=['GET', 'POST'])
def posts(id):
    # TODO: change post attributes to reflect new models.py
    """
    Route used to show a post on its own single page
    :param id: Unique identifier for post (post_id).
    Views a single post on its own page
    :return: renders 'post.html', passes in post information
    """
    post = Post.query.get_or_404(id)
    """
        page_posts is a list of dictionary containing attributes of stories
        page_posts is used because tags cannot be accessed through stories
    """
    post_tags = PostTag.query.filter_by(post_id=post.id).all()
    tags = []
    for post_tag in post_tags:
        name = Tag.query.filter_by(id=post_tag.tag_id).first().name
        tags.append(name)
    story = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'time': post.creation_time,
        'edit_time': post.edit_time,
        'is_visible': post.is_visible,
        'is_edited': post.is_edited,
        'tags': tags
    }
    return render_template('stories/posts.html', posts=post, post=story)
