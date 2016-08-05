from flask import render_template, request, current_app, flash, redirect, url_for
from .. import db
from ..models import Post, Comment
from . import posts
from .forms import CommentForm


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
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post_id=post.id, content=form.content.data, post=post)
        db.session.add(comment)
        db.session.commit()
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
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)



