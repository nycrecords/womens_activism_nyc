from flask import render_template, redirect, url_for, current_app, flash, request
from .. import db
from ..models import *
from . import main
from .forms import PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(title=title, content=content, is_edited=False, is_visible=True)
        #print(db.func.current_timestamp())
        #print(datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash('Post submitted!')
        return redirect(url_for('.index'))
    #posts = Post.query.order_by(Post.creation_time.desc()).all()
    #return render_template('index.html', form=form, posts=posts)

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.creation_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=True)
    # need to change this config parameter if I want to change the default 20 posts per page

    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)


