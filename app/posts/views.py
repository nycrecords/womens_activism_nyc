from flask import render_template, request, current_app
from .. import db
from ..models import Post
from . import posts


@posts.route('/posts', methods=['GET', 'POST'])
def all_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    posts=pagination.items
    return render_template('postsTab.html', posts=posts, pagination=pagination)


@posts.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


