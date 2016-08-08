from flask import render_template, request, current_app, flash, redirect, url_for
from .. import db
from ..models import Post, Comment
from . import posts
from .forms import CommentForm


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
    return render_template('posts/post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)



# @posts.route('/edit/<int:id>', method=['GET','POST'])
# def edit(id):
#     post = Post.query.get_or_404(id)
#     if request.method == 'POST':
#         data = request.form.copy()
#         new_title = data['input_title']
#         new_content = data['editor1']
#         post_id = post.id
#         reason = data['input_reason']
#         type = 'edit'
#         post.is_edited = True
#         postedit = PostEdit(post_id=post_id, content=new_content, reason=reason, type=type)
#         db.session.add(postedit)
#         db.session.add(post)
#         db.session.commit()
#         flash('The post has been updated')
#         return redirect(url_for('main.index'))
#     return render_template('edit_post.html', post=post)

