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
from app.models import Post, Comment, PostEdit, PostTag, Tag
from app.posts import posts
from app.posts.forms import CommentForm
from app.db_helpers import put_obj
from flask_login import login_required
from datetime import datetime


@posts.route('/posts', methods=['GET', 'POST'])
def all_posts():
    """
    Route for seperate post tab that shows all posts in the db.
    Displays all posts in a paginated fashion.
    :return: renders 'postTab.html', passes in post_feed as all posts in Post table (ordered by creation_time)
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    posts_feed = pagination.items

    page_posts = []

    for post in posts_feed:
        id = post.id
        title = post.title
        content = post.content
        just_now = post.just_now()
        time = post.creation_time
        comment_count = post.comments.count()

        post_tags = PostTag.query.filter_by(post_id=post.id).all()
        tags = []
        for post_tag in post_tags:
            name = Tag.query.filter_by(id=post_tag.tag_id).first().name
            tags.append([post_tag.tag_id, name])
        page_posts.append([id, title, content, just_now, time, comment_count, tags])
    return render_template('posts/postsTab.html', posts=page_posts, pagination=pagination)


@posts.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    :param(id) Query the db with id for the Post to display information in it
    :return template with ckeditor with post information to begin the edit
        on completion it will redirect to the posts page with feed of all posts
    Returns the confirmation page for editing a post(s).
    Admins can see both old and new edit(s) from PostEdit table if needed for Audits
    The latest post update lives in Post table
    All post history that cannot be seen by user lives in PostEdit table
    """
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form.copy()

        # add in user id later, writing the old post history into PostEdit table
        post_edit = PostEdit(post_id=post.id, creation_time=post.creation_time, edit_time=datetime.utcnow(), type='Edit'
                             , title=post.title, content=post.content, reason=data['input_reason'], version=post.version
                             )
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
        flash('The post has been edited.')
        return redirect(url_for('posts.all_posts'))
    return render_template('posts/edit_post.html', post=post)


@posts.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    :param(id) Query the db with id for the Post to display information in it
    :return redirect to posts page with feed of all posts
    Takes a post and makes it not visible - "deleted" status
    Post lives on in Post table but is_visible = False and will not show up on feeds
    Admins can still see the "deleted" post(s)
    """
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form.copy()

        # add in user id later, setting post.is_visible = False
        post_edit = PostEdit(post_id=post.id, creation_time=post.creation_time, edit_time=datetime.utcnow(),
                             type='Delete', title=post.title,
                             content=post.content, reason=data['input_reason'], version=post.version)
        put_obj(post_edit)

        new_edit_time = datetime.utcnow()
        new_is_visible = False
        post.is_visible = new_is_visible
        post.edit_time = new_edit_time
        put_obj(post)

        flash('The post has been deleted.')
        return redirect(url_for('posts.all_posts'))
    return render_template('posts/delete_post.html', post=post)


@posts.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    """
    Route used to show a post on its own single page
    :param id: Unique identifier for post (post_id).
    Views a single post on its own page
    :return: renders 'post.html', passes in post information
    """
    post = Post.query.get_or_404(id)
    page_posts = []

    id = post.id
    title = post.title
    content = post.content
    just_now = post.just_now()
    time = post.creation_time
    comment_count = post.comments.count()

    post_tags = PostTag.query.filter_by(post_id=post.id).all()
    tags = []
    for post_tag in post_tags:
        name = Tag.query.filter_by(id=post_tag.tag_id).first().name
        tags.append([post_tag.tag_id, name])
    page_posts.append([id, title, content, just_now, time, comment_count, tags])

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post_id=post.id, content=form.content.data, post=post)
        put_obj(comment)
        flash('Comment Submited!')
        return redirect(url_for('posts.posts', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.creation_time.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=True)
    comments = pagination.items
    return render_template('posts/posts.html', posts=page_posts, form=form,
                           comments=comments, pagination=pagination)
