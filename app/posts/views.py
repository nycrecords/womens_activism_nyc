from flask import render_template, current_app, flash, request, redirect, url_for
# from .. import db
from app.models import Post, PostEdit
from app.posts import posts
from app.posts.forms import DeleteForm
import bleach
from app.models import db
from app.db_helpers import put_obj


@posts.route('/posts', methods=['GET', 'POST'])
def all_posts():
    """
    Shows all post with the page buttons on the bottom of the page.

    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    posts=pagination.items
    return render_template('postsTab.html', posts=posts, pagination=pagination)


@posts.route('/posts/<int:id>', methods=['GET', 'POST'])
def single(id):
    """
    shows the social media sites/buttons and the flagging button
    also the creation times of the post
    """
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@posts.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """
    Returns the confirmation page for editing a post(s).
    Admins can see both old and new edit(s)

    id -- the Post id=most recent posts & PostEdit id= old posts
    """
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form.copy()
        # add in user id later
        post_edit = PostEdit(post_id=post.id, type='Edit', title=post.title,
                             content=post.content, reason=data['input_reason'], version=post.version)
        put_obj(post_edit)

        new_title = data['input_title']
        new_content = data['editor1']
        new_is_edited = True
        new_version = post.version + 1

        post.title = new_title
        post.content = new_content
        post.is_edited = new_is_edited
        post.version = new_version

        put_obj(post)

        return redirect(url_for('main.index', id=post.id, is_edited=True))
    return render_template('edit_post.html', post=post, is_edited=True)


@posts.route('/delete/post/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """
    Return the confirmation page for deleting a post(s).
    Admins can still see the "deleted" post(s)

    Keyword arguments:
    id -- the post id
    """
    post = Post.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=id).first()
        post.is_visible = False
        db.session.commit()
        flash('The post has been deleted.')
        return redirect(url_for('.index'))
    return render_template('delete_post.html', form=form)

# must email the admin to who deleted and what what they deleted

def strip_html(html_str):
    """
    a wrapper for bleach.clean() that strips ALL tags from the input
    :param html_str: string that needs to be stripped
    :return: a bleached string
    """
    tags = []
    attr = {}
    styles = []
    strip = True

    return bleach.clean(html_str,
                       tags=tags,
                       attributes=attr,
                       styles=styles,
                       strip=strip)



