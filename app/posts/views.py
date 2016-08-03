# TODO: Module level docstring
from flask import render_template, request, current_app
from .. import db
from ..models import Post
from . import posts


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
    return render_template('postsTab.html', posts=posts_feed, pagination=pagination)


@posts.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    """
    :param id: Unique identifier for post (post_id).
    Views a single post on its own page
    :return: renders 'post.html', passes in post information
    """
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


