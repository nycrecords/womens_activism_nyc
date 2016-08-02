from flask import render_template, redirect, url_for, current_app, flash, request
from .. import db
from ..models import *
from . import main
from .forms import PostForm, DeleteForm
import bleach


@main.route('/', methods=['GET', 'POST'])
def index(data=None):

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    # need to change this config parameter if I want to change the default 20 posts per page

    posts = pagination.items

    if data or request.method == 'POST':
        if request.form['input_title'] == '':
            if request.form['editor1'] == '':
                flash('Please enter a title.')
                flash('Please enter content.')
                return render_template('index.html', posts=posts, pagination=pagination)
            else:
                flash('Please enter a title.')
                return render_template('index.html', posts=posts, pagination=pagination)
        elif request.form['editor1'] == '':
            flash('Please enter content.')
            return render_template('index.html', posts=posts, pagination=pagination)
        else:
            title = request.form['input_title']
            content = request.form['editor1']
            post = Post(title=title, content=content, is_edited=False, is_visible=True)
            #print(db.func.current_timestamp())
            #print(datetime.utcnow())
            db.session.add(post)
            db.session.commit()
            flash('Post submitted!')
            return redirect(url_for('.index'))
    #posts = Post.query.order_by(Post.creation_time.desc()).all()
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    # if current_user != post.author and \
    #         not current_user.can(Permission.ADMINISTER):
    #     abort(403)
    form = PostForm()
    if form.validate_on_submit():
        posttags = PostTag.query.filter_by(post_id=id).all()
        for posttag in posttags:
            db.session.delete(posttag)
        comments = Comment.query.filter_by(post_id=id).all()
        for comment in comments:
            db.session.delete(comment)
        post.body = form.body.data
        post.title = form.title.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('main.index'))
    post = Post.query.filter_by(id=id).first()
    form.title.data = post.title
    form.content.data = strip_html(post.content)
    return render_template('edit_post.html', form=form, post=post)


@main.route('/delete/post/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """
    Return the confirmation page for deleting a post.

    Keyword arguments:
    id -- the post id
    """
    post = Post.query.get_or_404(id)
    # if current_user != post.author and not current_user.can(Permission.ADMINISTER) and not current_user.is_director():
    #     abort(403)
    form = DeleteForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=id).first()
        post.is_visible=False
        # posttags = PostTag.query.filter_by(post_id=id).all()
        # for posttag in posttags:
        #     db.session.delete(posttag)
        # comments = Comment.query.filter_by(post_id=id).all()
        # for comment in comments:
        #     db.session.delete(comment)
        # db.session.delete(post)
        db.session.commit()
        flash('The post has been deleted.')
        return redirect(url_for('.index'))
    return render_template('delete_post.html', form=form)


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